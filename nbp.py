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
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            if output:
                output_path = output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"nbp_{timestamp}.png"

            image = part.as_image()
            image.save(output_path)
            print(f"Image saved to: {output_path}")
            return output_path

    print("Error: No image was generated.", file=sys.stderr)
    sys.exit(1)


def generate_image(
    prompt: str,
    output: str | None = None,
    aspect_ratio: str = "1:1",
    size: str = "1K",
) -> str:
    """Generate an image using Gemini and save it."""
    client = get_client()

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=size,
            ),
        ),
    )

    return save_image(response, output)


def edit_image(
    input_path: str,
    prompt: str,
    output: str | None = None,
    size: str = "1K",
) -> str:
    """Edit an existing image using Gemini."""
    client = get_client()

    # Load the input image
    input_image = Image.open(input_path)

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[input_image, prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                image_size=size,
            ),
        ),
    )

    return save_image(response, output)


def main():
    parser = argparse.ArgumentParser(
        prog="nbp",
        description="Nano Banana Pro - Generate and edit images with Gemini 3 Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nbp "a cat wearing a hat"                  Generate new image
  nbp "sunset over mountains" -a 16:9        Widescreen landscape
  nbp "portrait photo" -s 4K -o portrait.png High-res with custom output
  nbp "add sunglasses" -e photo.png          Edit existing image
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
        "-o", "--output",
        metavar="FILE",
        help="Output path (default: nbp_TIMESTAMP.png)",
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        default="1:1",
        metavar="RATIO",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"],
        help="Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4 (default: 1:1)",
    )
    parser.add_argument(
        "-s", "--size",
        default="1K",
        metavar="SIZE",
        choices=["1K", "2K", "4K"],
        help="Resolution: 1K, 2K, 4K (default: 1K)",
    )

    args = parser.parse_args()

    if args.edit:
        edit_image(
            input_path=args.edit,
            prompt=args.prompt,
            output=args.output,
            size=args.size,
        )
    else:
        generate_image(
            prompt=args.prompt,
            output=args.output,
            aspect_ratio=args.aspect_ratio,
            size=args.size,
        )


if __name__ == "__main__":
    main()
