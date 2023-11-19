import openai
import streamlit as st
import os
import requests

class Chatbot:
    def get_seo_optimized_words(self, messages):
        try:
            my_api_key = os.getenv("OPEN AI KEY")
            client = openai.OpenAI(api_key=my_api_key)
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=300,
            )
            return response.choices[0].message.content

        except Exception as e:
            # Handle the exception here
            st.info(f"An error occurred: Make sure that all urls in text file are valid image urls")
            st.warning(f"ERROR Details are \n: {e}")
            return None


def is_valid_image_url(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('content-type')
        if content_type:
            return True
        else:
            return False
    except requests.RequestException:
        return False

if __name__ == "__main__":
    my_chatbot = Chatbot()

