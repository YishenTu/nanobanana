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


def get_client() -> genai.Client:
    """Get authenticated Gemini client."""
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
    return genai.Client()


def save_image(response, output: str | None) -> str:
    """Extract and save image from response."""
    output_path = ""
    for part in response.candidates[0].content.parts:
        if part.text:
            print(f"Gemini: {part.text}")
        if part.inline_data is not None:
            if output:
                output_path = output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"nanobanana_{timestamp}.png"

            image = part.as_image()
            image.save(output_path)
            print(f"Image saved to: {output_path}")
            return output_path

    if not output_path:
        print("Error: No image was generated.", file=sys.stderr)
        sys.exit(1)
    return output_path


def generate_image(
    prompt: str,
    output: str | None = None,
    aspect_ratio: str = "1:1",
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
            contents.append(Image.open(ref_path))

    config_kwargs = {
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=size,
        ),
    }

    if grounded or image_search:
        search_types = types.SearchTypes()
        if grounded:
            search_types.web_search = types.WebSearch()
        if image_search:
            search_types.image_search = types.ImageSearch()
            
        config_kwargs["tools"] = [
            types.Tool(google_search=types.GoogleSearch(
                search_types=search_types
            ))
        ]

    if thinking_level:
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level=thinking_level.capitalize(),
            include_thoughts=False
        )

    model_name = "gemini-3-pro-image-preview" if use_pro else "gemini-3.1-flash-image-preview"

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    return save_image(response, output)


def edit_image(
    input_path: str,
    prompt: str,
    output: str | None = None,
    size: str = "1K",
    use_pro: bool = False,
) -> str:
    """Edit an existing image using Gemini."""
    client = get_client()

    # Load the input image
    input_image = Image.open(input_path)

    model_name = "gemini-3-pro-image-preview" if use_pro else "gemini-3.1-flash-image-preview"

    response = client.models.generate_content(
        model=model_name,
        contents=[input_image, prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                image_size=size,
            ),
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
        default="1:1",
        metavar="RATIO",
        choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1"],
        help="Aspect ratio (default: 1:1)",
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
        if args.aspect_ratio in ["1:4", "4:1", "1:8", "8:1"]:
            invalid_flags.append(f"-a {args.aspect_ratio}")
        if args.image_search:
            invalid_flags.append("-i")
        if args.thinking:
            invalid_flags.append(f"-t {args.thinking}")
            
        if invalid_flags:
            print(f"Error: The following options are not supported with the Gemini 3 Pro model: {', '.join(invalid_flags)}", file=sys.stderr)
            sys.exit(1)

    if args.edit:
        edit_image(
            input_path=args.edit,
            prompt=args.prompt,
            output=args.output,
            size=args.resolution,
            use_pro=args.pro,
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
