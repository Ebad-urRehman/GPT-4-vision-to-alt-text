import openai
import os
import requests

class Chatbot:
    def get_seo_optimized_words(self, messages):
        my_api_key = os.getenv("OPEN AI KEY")
        client = openai.OpenAI(api_key=my_api_key)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    my_chatbot = Chatbot()

