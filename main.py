from pathlib import Path
import os
import subprocess
from llm import get_llm_response
from image_gen import generate_image
import random
# Artists and Styles for Diffusion Model Prompts

# Visual Artists
artists = [
    "Van Gogh", "Picasso", "Monet", "Da Vinci", "Michelangelo", "Rembrandt",
    "Dali", "Warhol", "Pollock", "Matisse", "Cezanne", "Renoir", "Degas",
    "Hokusai", "Frida Kahlo", "Georgia O'Keeffe", "Basquiat", "Banksy",
    "Rothko", "Kandinsky", "Mondrian", "Magritte", "Escher", "Caravaggio",
    "Botticelli", "Raphael", "Toulouse-Lautrec", "Gauguin", "Manet",
    "Klimt", "Schiele", "Bacon", "Hockney", "Hopper", "Wyeth"
]

# Art Styles and Movements
art_styles = [
    "impressionist", "cubist", "surrealist", "abstract expressionist",
    "pop art", "art nouveau", "baroque", "renaissance", "romantic",
    "realist", "minimalist", "fauvism", "dadaism", "pointillism",
    "expressionist", "futurist", "constructivist", "art deco",
    "photorealistic", "hyperrealistic", "watercolor", "oil painting",
    "digital art", "concept art", "street art", "graffiti style",
    "comic book style", "anime style", "manga style", "ukiyo-e"
]

# Film Directors (for cinematic styles)
directors = [
    "Kubrick", "Hitchcock", "Scorsese", "Tarantino", "Spielberg",
    "Wes Anderson", "Tim Burton", "David Lynch", "Ridley Scott",
    "Christopher Nolan", "Akira Kurosawa", "Wong Kar-wai",
    "Terrence Malick", "Denis Villeneuve", "Coen Brothers",
    "Paul Thomas Anderson", "Darren Aronofsky", "Guillermo del Toro"
]

# Photography Styles
photo_styles = [
    "film noir", "golden hour", "blue hour", "high contrast",
    "black and white", "sepia", "vintage", "polaroid", "35mm film",
    "macro photography", "wide angle", "telephoto", "bokeh",
    "street photography", "portrait photography", "landscape photography"
]

# Digital/Modern Styles
digital_styles = [
    "cyberpunk", "steampunk", "vaporwave", "synthwave", "pixel art",
    "low poly", "isometric", "neon", "glitch art", "holographic",
    "matte painting", "concept art", "game art", "3D render"
]

# Combined list for easy random selection
all_styles = artists + art_styles + directors + photo_styles + digital_styles

# Example usage:
# import random
# selected_style = random.choice(all_styles)
# prompt = f"a beautiful landscape in the style of {selected_style}"

def download_video(url: str) -> str:
    # download the video from the url
    # save the video to the local filesystem
    # return the path to the video
    pass

def summarize_video(url: str) -> str:
    # pass the video to the gemini api to summarize the video
    # we should get back a summarised transcript of the video
    prompt = f"""
    Could you please transcribe this video visually?  I would like a markdown numbered list of each scene you describe.

If the video has text/subtitles/overlays you do not need to mention those - I am purely interested in the visual description of each scene.

Please describe each scene as a stand-alone description, do not relate it to previous or forthcoming scenes.

For example, do not use phrases like 'The man continues on his walk', or 'The woman ...' - use 'A man walks' or 'A woman ...'.

Another example, do not describe the scene in multiple steps such as 'A hand with pink nail polish removes the basket from a black air fryer and then removes the crisper plate from the basket.' should be written as 'A hand with pink nail polish is reaching in to a black air fryer to remove the crisper plate.'

Very similar scenes should just be combined or skipped.  If there are two somewhat differing scenes (ie, just a change of focus or angle) there is no need to make it count as a different scene.

Each scene you describe should stand on it's own as a description of the scene with no prior assumptions of continuity on the readers part - the user should be able to perfectly imagine the scene based purely on your visual description.

Please add no other chat or text - just respond with the list of scene descriptions.

Thank you!"""
    pass

def generate_images(summary: str) -> list[str]:
    # we split the summary into sentences
    # we generate an image for each sentence
    # we return the list of image paths
    pass


def create_crossfade_video(image_files, output_file, pause_duration=2, fade_duration=1):
    # Calculate the total video duration
    total_duration = (pause_duration + fade_duration) * (len(image_files) - 1) + pause_duration

    filter_complex_parts = []
    for i in range(len(image_files) - 1):
        if i == 0:
            input1 = f"[0:v]"
        else:
            input1 = f"[x{i}]"
        input2 = f"[{i+1}:v]"
        output = f"[x{i+1}]" if i < len(image_files) - 2 else "[temp]"
        offset = (pause_duration + fade_duration) * i
        fade = f"{input1}{input2}xfade=transition=fade:duration={fade_duration}:offset={offset}{output};"
        filter_complex_parts.append(fade)

    # Properly connect the format filter to the final output
    filter_complex = ''.join(filter_complex_parts) + "[temp]format=yuv420p[v]"

    cmd = ['ffmpeg']
    # Add each image file with the total duration so they can all participate in crossfades
    for image_file in image_files:
        cmd.extend(['-loop', '1', '-t', str(total_duration), '-i', image_file])
    cmd += ['-filter_complex', filter_complex, '-map', '[v]', '-y', output_file]

    subprocess.run(cmd)

def generate_final_video(images: list[str], output_file: str) -> str:
    # we generate a video from the images with a cross-fade between each image
    # we return the path to the video
    create_crossfade_video(images, output_file, pause_duration=2, fade_duration=1)
    return output_file

def main(video_url: str) -> str:
    video_path = download_video(video_url)
    summary = summarize_video(video_path)
    images = generate_images(summary)
    final_video = generate_final_video(images)
    return final_video

if __name__ == "__main__":
    transcript_file = "recipethis.md"
    paragraphs = Path(transcript_file).read_text().split("\n")
    filenames = []
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        image_filename = f"recipethis_{i:02d}.jpg"
        filenames.append(os.path.join("images", image_filename))
        if os.path.exists(os.path.join("images", image_filename)):
            print(f"Image already exists: {image_filename}")
            continue
        print(f"Processing paragraph {i}: {paragraph}")
        print("-" * 20)
        print("Getting image prompt for paragraph")
        prompt = f"""
        You are a helpful assistant that generates image prompts for a Stable Diffusion image
        generator for a given paragraph describing a scene in a video.

        <scene-description>
        {paragraph}
        </scene-description>

        The image prompt should be a single sentence that captures the essence of the scene.
        The image prompt should include detailed descriptions as fitting a Stable Diffusion image prompt.
        The image prompt should be visually appealing and engaging.
        The image prompt should be artistic and creative.
        The image prompt should include a stylistic style to use when generating the image.

        Please respond with ONLY the image prompt, no other text.  Your response will be given directly
        to the Stable Diffusion image generator so any extra text will cause the image generator to fail.  Do not
        wrap the prompt in any xml or markdown tags.

        You MUST use one of the following styles, artists and movements:
        {", ".join(random.sample(all_styles, 5))}
        """
        response = get_llm_response(prompt, model="anthropic/claude-sonnet-4-20250514")
        image_prompt = response.choices[0].message.content
        print(f"Image prompt: {image_prompt}")
        print("-" * 20)
        print("Generating image for paragraph")
        image_file = generate_image(image_prompt, output_file=image_filename, model="google/imagen-4")
        print(f"Image generated: {image_file}")
        print("-" * 20)
        # break

    # final_video = generate_final_video(filenames, output_file="final_video.mp4")
    # print(f"Final video generated: {final_video}")

    # print(f"output_file: {output_file}")
