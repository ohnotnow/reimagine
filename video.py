from google import genai
from google.genai import types
import os
import requests
import json

def summarise_youtube_video(url: str, prompt: str, model: str = 'gemini-2.5-pro-preview-06-05') -> str:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model=model,
        contents=types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri=url)
                ),
                types.Part(text=prompt)
            ]
        )
    )
    return response.text

def tester():
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "google/gemini-2.5-pro-preview-05-06",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is this video about?"
                        },
                        {
                            "type": "youtube_url",
                            "youtube_url": {
                                "url": "https://www.youtube.com/watch?v=YuOnfQd-aTw"
                            }
                        }
                    ]
                }
            ]
        })
    )
    print(response.json())

if __name__ == "__main__":
    tester()
