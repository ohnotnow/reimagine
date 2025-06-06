# Reimagine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Python CLI tool that transcribes a video’s visual scenes into prompts, generates corresponding images via Stable Diffusion, and morphs them into a final video montage.

## Features

- Downloads a video from a URL  
- Uses a vision‐focused LLM to summarize scenes  
- Generates Stable Diffusion image prompts per scene  
- Renders images with `image-gen` and compiles them into a video morph  
- Configurable via environment variables and CLI flags  

## Repository

```bash
git clone https://github.com/ohnotnow/reimagine.git
cd reimagine
```

## Prerequisites

- Git  
- Python 3.8+  
- `uv` CLI (for dependency management & execution)  
  Documentation: https://docs.astral.sh/uv/  

## Installation

### macOS & Linux (Ubuntu)

```bash
# (Optional) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install uv tool if not already installed
python3 -m pip install uv

# Install project dependencies
uv sync
```

### Windows (PowerShell)

```powershell
# (Optional) create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install uv tool if not already installed
python -m pip install uv

# Install project dependencies
uv sync
```

## Configuration

Environment variables:

- `GOOGLE_API_KEY` – required by the image generation component  
- `ANTHROPIC_API_KEY` – required for LLM calls  

Export them in your shell before running:

```bash
export GOOGLE_API_KEY="…"
export ANTHROPIC_API_KEY="…"
```

## Usage

```bash
uv run main.py -- <video_url>
```

Positional arguments:

  video_url    URL of the video to process

Example:

```bash
uv run main.py -- "https://example.com/my-video.mp4"
```

On success, a file named `final_video.mp4` will be emitted in the project root.

## Project Structure

```
├── image_gen.py        # wraps Stable Diffusion API calls
├── llm.py              # wraps LLM summarization calls
├── morph.py            # stitches images into a morph video
├── main.py             # entrypoint: download → summarize → image-gen → morph
├── requirements.txt    # pinned Python dependencies
└── images/             # intermediate generated frames
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
