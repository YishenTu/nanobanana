# NBP CLI

![banana](banana.png)

CLI tool for generating and editing images using Google's Gemini 3 Pro image generation model.

## Installation

```bash
pip install nbp-cli
```

Then set your API key (get one from [Google AI Studio](https://aistudio.google.com/apikey)):

```bash
export GEMINI_API_KEY=your-api-key-here
```

Add the export to your `~/.zshrc` or `~/.bashrc` to persist it.

## Usage

```bash
# Generate a new image
nbp "a cute banana wearing sunglasses"

# With options
nbp "a futuristic city at sunset" -a 16:9 -r 2K -o city.png

# Edit an existing image
nbp "add a hat and sunglasses" -e input.png -o output.png

# Use Google Search grounding for real-time info
nbp "visualize today's weather in Tokyo" -s

# Use reference images for style or content guidance
nbp "a cute cat in this style" --reference style_image.png -o cat.png
nbp "a mix of these people" -ref person1.png person2.png
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `nbp_TIMESTAMP.png` |
| `-a, --aspect-ratio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | `1:1` |
| `-r, --resolution` | `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit an existing image (provide input path) | - |
| `-ref, --reference` | One or more reference images to guide generation | - |
| `-s, --search` | Use Google Search grounding (prompt should ask to "visualize") | - |

## Development

```bash
git clone https://github.com/YishenTu/nbp-cli.git
cd nbp-cli
uv sync
cp .env.example .env  # Add your GEMINI_API_KEY
uv run nbp "test prompt"
```

## Global Access

For global access, add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
alias nbp='uv run --project /path/to/nbp-cli nbp'
```

## Claude Code Skill

The skill is fully self-contained. Just copy and set API key!

**Requirements:** Python 3.12+ (pre-installed on most systems)

1. Copy the skill folder:
   ```bash
   cp -r skills/nanobanana-pro ~/.claude/skills/
   ```

2. Set your API key in `~/.zshrc` or `~/.bashrc`:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

That's it! Claude will automatically use this skill when you ask it to generate or edit images. Python dependencies auto-install on first run.
