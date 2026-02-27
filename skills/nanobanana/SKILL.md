---
name: nanobanana
description: Generate or edit images using NanoBanana. Use when users request image generation or edit, want to create visual content, or mention nanobanana.
---

# NanoBanana Image Generation

CLI tool for generating and editing images using Google's Gemini 3.1 Flash and Gemini 3 Pro models.

## When to use this skill

- User requests image generation or editing
- User wants to create visual content or visualize real-time info
- User mentions "nanobanana" or image generation
- User specifies image parameters like aspect ratio or resolution

## Command

```bash
nanobanana "prompt" [options]
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o` | Output file path | `nanobanana_TIMESTAMP.png` |
| `-a` | Aspect ratio (`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`) | `1:1` (gen) / keep (edit) |
| `-r` | Resolution (`0.5K`, `1K`, `2K`, `4K`) | `1K` |
| `-e` | Edit existing image (input path) | - |
| `-ref` | Reference image(s) for style guidance (max 14) | - |
| `-s` | Google Search grounding for real-time info | off |
| `-i` | Google Image Search grounding (Flash only) | off |
| `-p` | Use Gemini 3 Pro model | off |
| `-t` | Thinking level: `minimal`, `high` (Flash only) | - |

## Examples

```bash
# Generate
nanobanana "a cute cat sitting on a windowsill"
nanobanana "mountain landscape at sunset" -a 16:9 -r 2K -o landscape.png
nanobanana "cyberpunk cityscape" -r 4K -p -o cityscape.png

# Edit
nanobanana "add sunglasses and a hat" -e photo.png -o edited.png
nanobanana "change background to beach" -e input.png -o beach.png

# Reference images
nanobanana "a cute cat in this style" -ref style.png -o cat.png

# Search grounding (real-time info)
nanobanana "visualize today's weather in Tokyo" -s

# Complex: edit with grounding, reference, and style
nanobanana "turn this into a retro travel poster" -e input.png -ref style.png -s -a 16:9 -t high -o poster.png
```

## Tips

1. Be specific: include style keywords, lighting, mood, composition
2. For edits, be clear about what to change vs. preserve
3. For `-s` search mode, start prompt with "visualize"
4. For multiple images, spawn parallel threads to generate/edit concurrently
