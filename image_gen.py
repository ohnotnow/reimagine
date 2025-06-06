import replicate
import uuid
import os

IMAGE_DIR = "images"
DEFAULT_MODEL = "black-forest-labs/flux-kontext-pro"
DEFAULT_ASPECT_RATIO = "9:16"

def generate_image(prompt: str, model=DEFAULT_MODEL, aspect_ratio: str = DEFAULT_ASPECT_RATIO, output_file: str = ""):
    input = {
        "prompt": prompt,
        "output_format": "jpg",
        "aspect_ratio": aspect_ratio
    }

    output = replicate.run(
        model,
        input=input
    )

    if not output_file:
        # make a random file name
        output_file = f"{uuid.uuid4()}.jpg"

    output_file = os.path.join(IMAGE_DIR, output_file)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    with open(output_file, "wb") as file:
        file.write(output.read())

    return output_file


if __name__ == "__main__":
    prompt = input("Enter a prompt: ")
    generate_image(prompt, output_file="output.jpg")
