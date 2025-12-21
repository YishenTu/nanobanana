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
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `nbp_TIMESTAMP.png` |
| `-a, --aspect-ratio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | `1:1` |
| `-r, --resolution` | `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit an existing image (provide input path) | - |
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

To use NBP as a [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills), copy the skill to your skills directory:

```bash
cp -r skills/nanobanana-pro ~/.claude/skills/
```

Claude will automatically use this skill when you ask it to generate or edit images. Requires Global Access(alias setup) to work.
