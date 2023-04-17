import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_troubleshooting_suggestion(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, specialized in troubleshooting."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']
