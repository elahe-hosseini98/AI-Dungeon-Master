from config.openAI_config import client

def query_openAI(prompt, model):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                                {
                                "type": "text",
                                "text": prompt
                                }
                    ]
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to generate a response."
