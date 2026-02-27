# Nano Banana CLI

![banana](banana.png)

CLI tool for generating and editing images using Google's Gemini 3 Pro and Gemini 3.1 Flash image generation models.

## Installation

```bash
pip install nanobanana
```

Then set your API key (get one from [Google AI Studio](https://aistudio.google.com/apikey)):

```bash
export GEMINI_API_KEY=your-api-key-here
```

Add the export to your `~/.zshrc` or `~/.bashrc` to persist it.

## Usage

```bash
# Generate a new image
nanobanana "a cute banana wearing sunglasses"

# With options
nanobanana "a futuristic city at sunset" -a 16:9 -r 2K -o city.png

# Edit an existing image
nanobanana "add a hat and sunglasses" -e input.png -o output.png

# Edit with grounding, references, aspect ratio, and thinking
nanobanana "turn this into a retro travel poster" -e input.png -ref style.png -s -a 16:9 -t high -o poster.png

# Use Google Search grounding for real-time info
nanobanana "visualize today's weather in Tokyo" -s

# Use Google Image Search grounding explicitly
nanobanana "A detailed painting of a Timareta butterfly" -i

# Use reference images for style or content guidance
nanobanana "a cute cat in this style" --reference style_image.png -o cat.png
nanobanana "a mix of these people" -ref person1.png person2.png

# Enable High Thinking reasoning for difficult visual generation prompts
nanobanana "A futuristic city built inside a giant glass bottle floating in space" -t high

# Fall back to Gemini 3 Pro instead of default Gemini 3.1 Flash
nanobanana "a dog flying a kite" -p
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `nanobanana_TIMESTAMP.png` |
| `-a, --aspect-ratio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1` | Generate: `1:1`; Edit: keep input ratio |
| `-r, --resolution` | `0.5K`, `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit an existing image (provide input path) | - |
| `-ref, --reference` | One or more reference images to guide generation (max 14 total; high-fidelity may drop above 10 on Flash / 6 on Pro) | - |
| `-s, --search` | Use Google Search grounding | - |
| `-i, --image-search` | Use Google Image Search grounding | - |
| `-p, --pro` | Use the Gemini 3 Pro model instead of 3.1 Flash | - |
| `-t, --thinking` | Thinking reasoning level (`minimal` or `high`) | - |

## Development

```bash
git clone https://github.com/YishenTu/nanobanana.git
cd nanobanana
uv sync
cp .env.example .env  # Add your GEMINI_API_KEY
uv run nanobanana "test prompt"
```

## Global Access

For global access, add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
alias nanobanana='uv run --project /path/to/nanobanana nanobanana'
```

## Claude Code Skill

The skill is fully self-contained. Just copy and set API key!

**Requirements:** Python 3.12+ (pre-installed on most systems)

1. Copy the skill folder:
   ```bash
   cp -r skills/nanobanana ~/.claude/skills/
   ```

2. Set your API key in `~/.zshrc` or `~/.bashrc`:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

That's it! Claude will automatically use this skill when you ask it to generate or edit images. Python dependencies auto-install on first run.
