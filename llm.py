from litellm import completion

def get_llm_response(prompt: str, model="openrouter/google/gemini-2.5-flash-preview-05-20"):
    response = completion(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response
