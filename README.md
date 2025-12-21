# NBP CLI

![banana](banana.png)

CLI tool for generating and editing images using Google's Gemini 3 Pro image generation model.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)

3. Create a `.env` file:
```bash
GEMINI_API_KEY=your-api-key-here
```

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

## Global Installation

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
alias nbp='uv run --project /path/to/project nbp'
```

Then use from anywhere:
```bash
nbp "your prompt here"
```
