---
name: nanobanana-pro-image-generation
description: Generate or edit images using NanoBanana Pro. Use when users request image generation or edit, want to create visual content, or mention nbp/nano banana pro.
---

# NBP - Nano Banana Pro Image Generation

NanoBanana Pro (NBP) is a CLI tool for generating and editing images using Google's Gemini 3 Pro image generation model.

## When to use this skill

- User requests image generation
- User wants to create visual content from text prompts
- User wants to edit or modify an existing image
- User wants to use reference images for style or content guidance
- User mentions "nbp", "nano banana pro", or image generation
- User specifies image parameters like aspect ratio or resolution
- User wants to visualize real-time info (weather, stocks, current events)

## Command syntax

### Generate new image
```bash
zsh -i -c 'nbp "your prompt here" [options]'
```

### Edit existing image
```bash
zsh -i -c 'nbp "edit instruction" -e /path/to/input.png -o output.png'
```

### Generate with reference images
```bash
zsh -i -c 'nbp "your prompt" --reference ref1.png [ref2.png ...] -o output.png'
```

## Options

| Flag | Description | Choices | Default |
|------|-------------|---------|---------|
| `-o, --output` | Output file path | Any path | `nbp_TIMESTAMP.png` |
| `-a, --aspect-ratio` | Image aspect ratio (new images only) | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | `1:1` |
| `-r, --resolution` | Image resolution | `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit existing image (provide input path) | Any image path | - |
| `-ref, --reference` | One or more reference images to guide generation | Any image path(s) | - |
| `-s, --search` | Use Google Search grounding for real-time info | - | off |

## Examples

### Basic image generation
```bash
zsh -i -c 'nbp "a cute cat sitting on a windowsill"'
```

### Widescreen landscape
```bash
zsh -i -c 'nbp "a beautiful mountain landscape at sunset" -a 16:9 -r 2K -o landscape.png'
```

### Portrait image
```bash
zsh -i -c 'nbp "professional headshot portrait, studio lighting" -a 9:16 -o portrait.png'
```

### High resolution
```bash
zsh -i -c 'nbp "detailed cyberpunk cityscape" -r 4K -o cityscape.png'
```

### Edit an existing image
```bash
zsh -i -c 'nbp "add sunglasses and a hat" -e /path/to/photo.png -o edited.png'
```

### Change background of image
```bash
zsh -i -c 'nbp "change background to a beach scene" -e input.png -o beach_version.png'
```

### Use reference images for style guidance
```bash
zsh -i -c 'nbp "a cute cat in this style" --reference style_image.png -o cat.png'
```

### Use multiple reference images
```bash
zsh -i -c 'nbp "a mix of these people" -ref person1.png person2.png -o merged.png'
```

### Google Search grounding (real-time info)
```bash
zsh -i -c 'nbp "visualize today'\''s weather in Tokyo" -s'
```

### Search grounding with options
```bash
zsh -i -c 'nbp "visualize the current stock price of AAPL as a chart" -s -a 16:9 -o aapl.png'
```

## Output

- Images are saved as PNG files
- Default filename: `nbp_YYYYMMDD_HHMMSS.png` (timestamped)
- Saved to current directory unless `-o` specifies a path

## Tips for better prompts

1. Be specific and descriptive
2. Include style keywords (e.g., "digital art", "photorealistic", "watercolor")
3. Mention lighting, mood, and composition
4. Specify camera angle or perspective if needed
5. For edits, be clear about what to change vs. preserve
6. For `-s` search mode, start prompt with "visualize" (e.g., "visualize today's weather...")
7. For reference images, describe how you want the reference used (e.g., "in this style", "similar to this")

## Requirements

- `GEMINI_API_KEY` environment variable must be set
- Get your API key at: https://aistudio.google.com/apikey
