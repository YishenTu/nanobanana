---
name: nanobanana
description: Generate or edit images using NanoBanana. Use when users request image generation or edit, want to create visual content, or mention nanobanana.
---

# NanoBanana Image Generation

NanoBanana is a CLI tool for generating and editing images using Google's Gemini 3.1 Flash and Gemini 3 Pro image generation models.

## When to use this skill

- User requests image generation
- User wants to create visual content from text prompts
- User wants to edit or modify an existing image
- User wants to use reference images for style or content guidance
- User mentions "nanobanana", "nano banana", or image generation
- User specifies image parameters like aspect ratio or resolution
- User wants to visualize real-time info (weather, stocks, current events)

## Command syntax

The script is bundled at `scripts/nanobanana.py` relative to this skill directory. Find the skill location:
- Global: `~/.claude/skills/nanobanana/scripts/nanobanana.py`
- Project: `.claude/skills/nanobanana/scripts/nanobanana.py`

Run with `python3` (dependencies auto-install on first run):

### Generate new image
```bash
python3 <skill_dir>/scripts/nanobanana.py "your prompt here" [options]
```

### Edit existing image
```bash
python3 <skill_dir>/scripts/nanobanana.py "edit instruction" -e /path/to/input.png -o output.png
```

### Generate with reference images
```bash
python3 <skill_dir>/scripts/nanobanana.py "your prompt" --reference ref1.png [ref2.png ...] -o output.png
```

## Options

| Flag | Description | Choices | Default |
|------|-------------|---------|---------|
| `-o, --output` | Output file path | Any path | `nanobanana_TIMESTAMP.png` |
| `-a, --aspect-ratio` | Image aspect ratio (generation and edit) | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1` | Generate: `1:1`; Edit: keep input ratio |
| `-r, --resolution` | Image resolution | `0.5K`, `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit existing image (provide input path) | Any image path | - |
| `-ref, --reference` | One or more reference images to guide generation (max 14 total; high-fidelity may drop above 10 on Flash / 6 on Pro) | Any image path(s) | - |
| `-s, --search` | Use Google Search grounding for real-time info | - | off |
| `-i, --image-search` | Use Google Image Search grounding (3.1 Flash only) | - | off |
| `-p, --pro` | Use Gemini 3 Pro model instead of 3.1 Flash | - | off |
| `-t, --thinking` | Thinking reasoning level (3.1 Flash only) | `minimal`, `high` | - |

## Examples

### Basic image generation
```bash
python3 <skill_dir>/scripts/nanobanana.py "a cute cat sitting on a windowsill"
```

### Widescreen landscape
```bash
python3 <skill_dir>/scripts/nanobanana.py "a beautiful mountain landscape at sunset" -a 16:9 -r 2K -o landscape.png
```

### Portrait image
```bash
python3 <skill_dir>/scripts/nanobanana.py "professional headshot portrait, studio lighting" -a 9:16 -o portrait.png
```

### High resolution
```bash
python3 <skill_dir>/scripts/nanobanana.py "detailed cyberpunk cityscape" -r 4K -o cityscape.png
```

### Edit an existing image
```bash
python3 <skill_dir>/scripts/nanobanana.py "add sunglasses and a hat" -e /path/to/photo.png -o edited.png
```

### Change background of image
```bash
python3 <skill_dir>/scripts/nanobanana.py "change background to a beach scene" -e input.png -o beach_version.png
```

### Edit with grounding, references, and style controls
```bash
python3 <skill_dir>/scripts/nanobanana.py "turn this into a retro travel poster" -e input.png -ref style.png -s -a 16:9 -t high -o poster.png
```

### Use reference images for style guidance
```bash
python3 <skill_dir>/scripts/nanobanana.py "a cute cat in this style" --reference style_image.png -o cat.png
```

### Use multiple reference images
```bash
python3 <skill_dir>/scripts/nanobanana.py "a mix of these people" -ref person1.png person2.png -o merged.png
```

### Google Search grounding (real-time info)
```bash
python3 <skill_dir>/scripts/nanobanana.py "visualize today's weather in Tokyo" -s
```

### Search grounding with options
```bash
python3 <skill_dir>/scripts/nanobanana.py "visualize the current stock price of AAPL as a chart" -s -a 16:9 -o aapl.png
```

### Image Search grounding
```bash
python3 <skill_dir>/scripts/nanobanana.py "A detailed painting of a Timareta butterfly" -i
```

### Use Gemini 3 Pro model
```bash
python3 <skill_dir>/scripts/nanobanana.py "a professional product photo of a perfume bottle" -p -r 4K -o product.png
```

### High thinking level for complex prompts
```bash
python3 <skill_dir>/scripts/nanobanana.py "A futuristic city built inside a giant glass bottle floating in space" -t high -o city.png
```

## Output

- Images are saved as PNG files
- Default filename: `nanobanana_YYYYMMDD_HHMMSS.png` (timestamped)
- Saved to current directory unless `-o` specifies a path

## Tips for better prompts

1. Be specific and descriptive
2. Include style keywords (e.g., "digital art", "photorealistic", "watercolor")
3. Mention lighting, mood, and composition
4. Specify camera angle or perspective if needed
5. For edits, be clear about what to change vs. preserve
6. For `-s` search mode, start prompt with "visualize" (e.g., "visualize today's weather...")
7. For reference images, describe how you want the reference used (e.g., "in this style", "similar to this")
8. For multiple images generation/editing, spawn multiple threads to generate/edit images in parallel
