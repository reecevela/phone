import openai
import os
from dotenv import load_dotenv

class Bot:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_suggestion(self, conversation):
        print("Conversation:", conversation)
        combined = [{"role": "user", "content": "You are Ruby, wise-cracking, witty, charming. Answer in sentences."}] + conversation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens = 512,
            messages=combined
        )
        return response['choices'][0]['message']['content']
    
    def summarize(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Shorten the following text."},
                {"role": "user", "content": text},
            ]
        )
        return response['choices'][0]['message']['content']
    
    def raw_api_call(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Answer as concisely as possible."},
                {"role": "user", "content": text}
            ]
        )
        return response
