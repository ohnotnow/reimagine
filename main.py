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

def generate_single_image(paragraph: str, output_filename: str) -> str:
    print("Getting image prompt for paragraph")
    prompt = get_prompt("image", {"paragraph": paragraph, "styles": get_random_styles(5)})
    response = get_llm_response(prompt, model="anthropic/claude-sonnet-4-20250514")
    image_prompt = response.choices[0].message.content
    print(f"Image prompt: {image_prompt}")
    print("-" * 20)
    print("Generating image for paragraph")
    image_file = generate_image(image_prompt, output_file=output_filename, model="google/imagen-4")
    print(f"Image generated: {image_file}")
    print("-" * 20)
    return image_file

def generate_images(paragraphs: list[str], prefix: str = "image", output_dir: str = "images") -> list[str]:
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
        generate_single_image(paragraph, image_filename)
    return filenames

def generate_final_video(filenames: list[str], output_file: str, steps_per_morph: int = 50) -> str:
    print("Generating morph video")
    final_video = generate_morph_video(filenames, output_path=output_file, steps_per_morph=steps_per_morph)
    return final_video

def generate_video(transcript_file: str, output_file: str = "final_video.mp4", steps_per_morph: int = 50) -> str:
    paragraphs = Path(transcript_file).read_text().split("\n")
    prefix = Path(transcript_file).stem
    filenames = generate_images(paragraphs, prefix=prefix)
    video_file = generate_final_video(filenames, output_file, steps_per_morph)
    print(f"Final video generated: {video_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript_file", type=str, help="The transcript file to generate a video from")
    parser.add_argument("--output_file", type=str, help="The output file to save the video to", default="final_video.mp4")
    parser.add_argument("--steps_per_morph", type=int, help="The number of steps per morph", default=50)
    args = parser.parse_args()
    generate_video(args.transcript_file, args.output_file, args.steps_per_morph)
