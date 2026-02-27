#!/usr/bin/env python3
"""Nano Banana Pro - CLI for Gemini image generation."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project directory
load_dotenv(Path(__file__).parent / ".env")

from google import genai
from google.genai import types
from PIL import Image

MAX_REFERENCE_IMAGES = 14
FLASH_HIGH_FIDELITY_REFERENCE_HINT = 10
PRO_HIGH_FIDELITY_REFERENCE_HINT = 6


def get_client() -> genai.Client:
    """Get authenticated Gemini client."""
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
    return genai.Client()


def load_image(path: str):
    """Load an image from disk and return an in-memory copy."""
    try:
        with Image.open(path) as image:
            return image.copy()
    except Exception as exc:
        print(f"Error: Failed to open image '{path}': {exc}", file=sys.stderr)
        sys.exit(1)


def build_config(
    *,
    aspect_ratio: str | None,
    size: str,
    grounded: bool,
    image_search: bool,
    thinking_level: str | None,
) -> types.GenerateContentConfig:
    """Build shared generation config for both generate and edit flows."""
    image_config_kwargs = {"image_size": size}
    if aspect_ratio:
        image_config_kwargs["aspect_ratio"] = aspect_ratio

    config_kwargs = {
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": types.ImageConfig(**image_config_kwargs),
    }

    if grounded or image_search:
        search_types = types.SearchTypes()
        if grounded:
            search_types.web_search = types.WebSearch()
        if image_search:
            search_types.image_search = types.ImageSearch()

        config_kwargs["tools"] = [
            types.Tool(
                google_search=types.GoogleSearch(
                    search_types=search_types,
                )
            )
        ]

    if thinking_level:
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level=thinking_level.capitalize(),
            include_thoughts=False,
        )

    return types.GenerateContentConfig(**config_kwargs)


def validate_reference_count(references: list[str] | None, use_pro: bool) -> None:
    """Validate documented reference-image limits before calling the API."""
    if not references:
        return

    ref_count = len(references)
    model_name = "Gemini 3 Pro" if use_pro else "Gemini 3.1 Flash"

    if ref_count > MAX_REFERENCE_IMAGES:
        print(
            f"Error: {model_name} supports up to {MAX_REFERENCE_IMAGES} reference images. "
            f"Received {ref_count}.",
            file=sys.stderr,
        )
        sys.exit(1)

    high_fidelity_hint = (
        PRO_HIGH_FIDELITY_REFERENCE_HINT if use_pro else FLASH_HIGH_FIDELITY_REFERENCE_HINT
    )
    if ref_count > high_fidelity_hint:
        print(
            f"Warning: {model_name} may reduce high-fidelity matching above "
            f"{high_fidelity_hint} reference images (received {ref_count}).",
            file=sys.stderr,
        )


def iter_response_parts(response):
    """Yield response parts across SDK response shapes."""
    response_parts = getattr(response, "parts", None)
    if response_parts:
        yield from response_parts
        return

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        parts = getattr(content, "parts", None) or []
        yield from parts


def finish_reasons(response) -> list[str]:
    """Collect finish reasons for better error reporting."""
    reasons: list[str] = []
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        reason = getattr(candidate, "finish_reason", None)
        if reason is not None:
            reasons.append(str(reason))
    return reasons


def save_image(response, output: str | None) -> str:
    """Extract and save image from response."""
    output_path = output or f"nanobanana_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    saw_parts = False

    for part in iter_response_parts(response):
        saw_parts = True
        if getattr(part, "text", None):
            print(f"Gemini: {part.text}")

        # Thinking interim images should not be treated as final output.
        if getattr(part, "thought", False):
            continue

        if getattr(part, "inline_data", None) is not None:
            try:
                image = part.as_image()
            except Exception as exc:
                print(f"Warning: Failed to decode image output: {exc}", file=sys.stderr)
                continue

            image.save(output_path)
            print(f"Image saved to: {output_path}")
            return output_path

    if not saw_parts:
        reasons = finish_reasons(response)
        if reasons:
            print(
                f"Error: Model returned no content parts (finish reasons: {', '.join(reasons)}).",
                file=sys.stderr,
            )
        else:
            print("Error: Model returned no content parts.", file=sys.stderr)
        sys.exit(1)

    reasons = finish_reasons(response)
    if reasons:
        print(f"Error: No image was generated (finish reasons: {', '.join(reasons)}).", file=sys.stderr)
    else:
        print("Error: No image was generated.", file=sys.stderr)
    sys.exit(1)


def generate_image(
    prompt: str,
    output: str | None = None,
    aspect_ratio: str | None = None,
    size: str = "1K",
    grounded: bool = False,
    image_search: bool = False,
    references: list[str] | None = None,
    use_pro: bool = False,
    thinking_level: str | None = None,
) -> str:
    """Generate an image using Gemini and save it."""
    client = get_client()

    contents = [prompt]
    if references:
        for ref_path in references:
            contents.append(load_image(ref_path))

    model_name = "gemini-3-pro-image-preview" if use_pro else "gemini-3.1-flash-image-preview"

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=build_config(
            aspect_ratio=aspect_ratio or "1:1",
            size=size,
            grounded=grounded,
            image_search=image_search,
            thinking_level=thinking_level,
        ),
    )

    return save_image(response, output)


def edit_image(
    input_path: str,
    prompt: str,
    output: str | None = None,
    aspect_ratio: str | None = None,
    size: str = "1K",
    grounded: bool = False,
    image_search: bool = False,
    references: list[str] | None = None,
    use_pro: bool = False,
    thinking_level: str | None = None,
) -> str:
    """Edit an existing image using Gemini."""
    client = get_client()

    contents = [prompt, load_image(input_path)]
    if references:
        for ref_path in references:
            contents.append(load_image(ref_path))

    model_name = "gemini-3-pro-image-preview" if use_pro else "gemini-3.1-flash-image-preview"

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=build_config(
            aspect_ratio=aspect_ratio,
            size=size,
            grounded=grounded,
            image_search=image_search,
            thinking_level=thinking_level,
        ),
    )

    return save_image(response, output)


def main():
    parser = argparse.ArgumentParser(
        prog="nanobanana",
        description="Nano Banana - Generate and edit images with Gemini 3 Pro and 3.1 Flash",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nanobanana "a cat wearing a hat"                  Generate new image
  nanobanana "sunset over mountains" -a 16:9        Widescreen landscape
  nanobanana "portrait photo" -r 4K -o portrait.png High-res with custom output
  nanobanana "add sunglasses" -e photo.png          Edit existing image
  nanobanana "visualize today's weather in NYC" -s  Use Google Search grounding
  nanobanana "A detailed painting of a Timareta butterfly" -i Use Image Search grounding
  nanobanana "a cat in this style" --reference s.png Use reference image
  nanobanana "complex prompt" -t high               Use high thinking level
  nanobanana "a dog" -p                             Use 3 Pro model
        """,
    )
    parser.add_argument(
        "prompt",
        help="Text prompt for generation or edit instruction",
    )
    parser.add_argument(
        "-e", "--edit",
        metavar="FILE",
        help="Edit existing image instead of generating new",
    )
    parser.add_argument(
        "-ref", "--reference",
        nargs="+",
        metavar="FILE",
        help="One or more reference images to guide generation",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Output path (default: nanobanana_TIMESTAMP.png)",
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        default=None,
        metavar="RATIO",
        choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1"],
        help="Aspect ratio (generate default: 1:1; edit default: keep input ratio)",
    )
    parser.add_argument(
        "-r", "--resolution",
        default="1K",
        metavar="RES",
        choices=["0.5K", "1K", "2K", "4K"],
        help="Resolution: 0.5K, 1K, 2K, 4K (default: 1K)",
    )
    parser.add_argument(
        "-s", "--search",
        action="store_true",
        help="Use Google Search grounding",
    )
    parser.add_argument(
        "-i", "--image-search",
        action="store_true",
        help="Use Google Image Search grounding",
    )
    parser.add_argument(
        "-p", "--pro",
        action="store_true",
        help="Use Gemini 3 Pro model instead of 3.1 Flash",
    )
    parser.add_argument(
        "-t", "--thinking",
        choices=["minimal", "high"],
        help="Thinking level (minimal or high)",
    )

    args = parser.parse_args()

    if args.pro:
        invalid_flags = []
        if args.resolution == "0.5K":
            invalid_flags.append("-r 0.5K")
        if args.aspect_ratio in {"1:4", "4:1", "1:8", "8:1"}:
            invalid_flags.append(f"-a {args.aspect_ratio}")
        if args.image_search:
            invalid_flags.append("-i")
        if args.thinking:
            invalid_flags.append(f"-t {args.thinking}")
            
        if invalid_flags:
            print(f"Error: The following options are not supported with the Gemini 3 Pro model: {', '.join(invalid_flags)}", file=sys.stderr)
            sys.exit(1)

    validate_reference_count(args.reference, args.pro)

    if args.edit:
        edit_image(
            input_path=args.edit,
            prompt=args.prompt,
            output=args.output,
            aspect_ratio=args.aspect_ratio,
            size=args.resolution,
            grounded=args.search,
            image_search=args.image_search,
            references=args.reference,
            use_pro=args.pro,
            thinking_level=args.thinking,
        )
    else:
        generate_image(
            prompt=args.prompt,
            output=args.output,
            aspect_ratio=args.aspect_ratio,
            size=args.resolution,
            grounded=args.search,
            image_search=args.image_search,
            references=args.reference,
            use_pro=args.pro,
            thinking_level=args.thinking,
        )


if __name__ == "__main__":
    main()
