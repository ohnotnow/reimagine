# Reimagine

**Version**: 0.1.0
**License**: MIT (see LICENSE)

Reimagine is a Python CLI tool that transforms a text transcript (e.g., a video transcription or scene descriptions) into a dynamic, morphing video montage. It uses a large-language model (Litellm) to craft Stable Diffusion prompts, generates images via Replicate, then stitches those images together with optical-flow–based morph transitions using OpenCV.

The idea is to let the LLM's and image-generation model 're-imagine' the original video.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

---

## Quick Start

```bash
# 1. Clone the repo
git clone git@github.com:ohnotnow/reimagine.git
cd reimagine

# 2. Install dependencies
uv sync

# 3. Configure API keys (see below)
export REPLICATE_API_TOKEN="your_replicate_token"
export ANTHROPIC_API_KEY="your_litellm_key"
# or OPENAI_API_KEY, OPENROUTER_API_KEY, etc

# 4. Run Reimagine on a transcript
uv run main.py path/to/your_transcript.md \
    --output_file my_video.mp4 \
    --steps_per_morph 50
```

---

## Prerequisites

- Python ≥ 3.13
- [uv CLI](https://docs.astral.sh/uv/getting-started/installation/) (for dependency management & execution)
- Replicate account & API token
- (Optional) Anthropic or OpenAI API token for Litellm

---

## Installation

1. Ensure `uv` is installed and on your `PATH`.
2. Clone the repo:
   ```bash
   git clone git@github.com:ohnotnow/reimagine.git
   cd reimagine
   ```
3. Install Python dependencies:
   ```bash
   uv sync
   ```
4. Copy or set environment variables:
   ```bash
   export REPLICATE_API_TOKEN="YOUR_REPLICATE_API_TOKEN"
   export LITELLM_API_KEY="YOUR_LITELLM_API_KEY"
   ```
5. (Optional) Adjust Jinja templates in `prompts/` or add new ones.

---

## Usage

```bash
uv run main.py <transcript_file> [--output_file OUTPUT] [--steps_per_morph N] [--llm-model MODEL_NAME] [--image-model MODEL_NAME] [--max-scenes NUMBER]
```

Arguments:

- `<transcript_file>`
  Path to a plain-text transcript (one scene or paragraph per line).
- `--output_file` (default: `final_video.mp4`)
  Path to write the resulting MP4 video.
- `--steps_per_morph` (default: `50`)
  Number of intermediate frames per image transition - bigger means a slower/gentler image transition.
- `--llm-model` (default: `anthropic/claude-sonnet-4-20250514`)
  Which LLM to call to do the image prompt generation.  Uses LiteLLM format, eg 'openai/gpt-4.1', 'openrouter/google/gemini-2.5-pro'
- `--image-model` (default: `google/imagen-4`)
  Which image generator to use via the [Replicate API](https://replicate.com/)
- `--max-scenes` (default: 10)
  The maximum number of scenes to generate an image for.  If the initial transcript has more than this - then calls out to the LLM model to consolodate them

---

## Configuration

- **Models**
  - LLM: default in code is `anthropic/claude-sonnet-4-20250514`. Override in `get_llm_response()`.
  - Image: default Replicate model is `black-forest-labs/flux-kontext-pro`. Override in `generate_image()`.
- **Prompts**
  - Templates live in `prompts/*.jinja`. Use Jinja2 syntax to add new templates or variables.
- **Styles**
  - Customize visual styles by editing `styles.py`.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
