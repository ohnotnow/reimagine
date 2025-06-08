from pathlib import Path
import os
import argparse
from llm import get_llm_response
from image_gen import generate_image
from morph import generate_morph_video
from styles import get_random_styles
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_prompt(name: str, variables: dict[str, str] = {}) -> str:
    """
    Get a prompt from the prompts directory and render it with the given variables.
    """
    env = Environment(
        loader=FileSystemLoader("prompts"),
        autoescape=select_autoescape()
    )
    template = env.get_template(f"{name}.jinja")
    return template.render(variables)


def summarize_video(url: str) -> str:
    # pass the video to the gemini api to summarize the video
    # we should get back a summarised transcript of the video
    prompt = get_prompt("summarise")
    pass

def generate_single_image(paragraph: str, output_filename: str, llm_model: str = "anthropic/claude-sonnet-4-20250514", image_model: str = "google/imagen-4") -> str:
    print("Getting image prompt for paragraph")
    prompt = get_prompt("image", {"paragraph": paragraph, "styles": get_random_styles(5)})
    response = get_llm_response(prompt, model=llm_model)
    image_prompt = response.choices[0].message.content
    print(f"Image prompt: {image_prompt}")
    print("-" * 20)
    print("Generating image for paragraph")
    image_file = generate_image(image_prompt, output_file=output_filename, model=image_model)
    print(f"Image generated: {image_file}")
    print("-" * 20)
    return image_file

def generate_images(paragraphs: list[str], prefix: str = "image", output_dir: str = "images", llm_model: str = "anthropic/claude-sonnet-4-20250514", image_model: str = "google/imagen-4") -> list[str]:
    filenames = []
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        image_filename = os.path.join(output_dir, f"{prefix}_{i:03d}.jpg")
        filenames.append(image_filename)
        if os.path.exists(image_filename):
            print(f"Image already exists: {image_filename}")
            continue
        print(f"Processing paragraph {i}: {paragraph}")
        print("-" * 20)
        generate_single_image(paragraph, image_filename, llm_model, image_model)
    return filenames

def generate_final_video(filenames: list[str], output_file: str, steps_per_morph: int = 50) -> str:
    print("Generating morph video")
    final_video = generate_morph_video(filenames, output_path=output_file, steps_per_morph=steps_per_morph)
    return final_video

def generate_video(transcript_file: str, output_file: str = "final_video.mp4", steps_per_morph: int = 50, llm_model: str = "anthropic/claude-sonnet-4-20250514", image_model: str = "google/imagen-4", max_scenes: int = 10) -> str:
    paragraphs = Path(transcript_file).read_text().split("\n")
    if len(paragraphs) > max_scenes:
        print(f"Shortening transcript to {max_scenes} scenes")
        prompt = get_prompt("reduce_scenes", {"original_scenes": Path(transcript_file).read_text()})
        shortened_transcript = get_llm_response(prompt, model=llm_model).choices[0].message.content
        paragraphs = shortened_transcript.split("\n")
        print(f"Shortened transcript to {len(paragraphs)} scenes")

    prefix = Path(transcript_file).stem
    filenames = generate_images(paragraphs, prefix=prefix, llm_model=llm_model, image_model=image_model)
    video_file = generate_final_video(filenames, output_file, steps_per_morph)
    print(f"Final video generated: {video_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_file", type=str, help="The transcript file to generate a video from")
    parser.add_argument("--output_file", type=str, help="The output file to save the video to", default="final_video.mp4")
    parser.add_argument("--steps_per_morph", type=int, help="The number of steps per morph", default=50)
    parser.add_argument("--llm-model", type=str, help="The LLM model to use", default="anthropic/claude-sonnet-4-20250514")
    parser.add_argument("--image-model", type=str, help="The image generation model to use", default="google/imagen-4")
    parser.add_argument("--max-scenes", type=int, help="The maximum number of scenes to generate", default=10)
    args = parser.parse_args()
    generate_video(args.transcript_file, args.output_file, args.steps_per_morph, args.llm_model, args.image_model)
