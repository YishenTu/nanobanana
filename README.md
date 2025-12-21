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
nbp "a futuristic city at sunset" -a 16:9 -s 2K -o city.png

# Edit an existing image
nbp "add a hat and sunglasses" -e input.png -o output.png
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `nbp_TIMESTAMP.png` |
| `-a, --aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `9:21` | `1:1` |
| `-s, --size` | `1K`, `2K`, `4K` | `1K` |
| `-e, --edit` | Edit an existing image (provide input path) | - |

## Global Installation

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
alias nbp='uv run --project /path/to/project nbp'
```

Then use from anywhere:
```bash
nbp "your prompt here"
```
