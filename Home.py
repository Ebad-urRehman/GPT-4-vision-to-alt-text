import os.path
import pandas
import streamlit as st
import pandas as pd
import requests
import time
import openai
import os
import requests
from pathlib import Path


# ------------------------------------------FUNCTIONS CODE-------------------------------------

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

def get_desktop_path():
    # Get the user's home directory
    home_dir = Path.home()

    # Define the "Desktop" directory based on the operating system
    desktop_dir = None
    if os.name == 'posix':
        desktop_dir = home_dir / 'Desktop'
    elif os.name == 'nt':
        desktop_dir = home_dir / 'Desktop'

    return desktop_dir

# -----------------------------Main File Code----------------------------

# finding current date and time
current_time = time.localtime()
day = time.strftime("%d", current_time)
month = time.strftime("%B", current_time)
year = time.strftime("%Y", current_time)
date = f"{day}-{month}-{year}"

st.markdown(f"<p style='text-align: right;'>{date}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>✨Image to SEO keywords✨</h1>", unsafe_allow_html=True)

urls_string = None

# creating input box styling
st.markdown(f"""
<style>
.stTextArea{{
        position: fixed;
        bottom: 0;
        z-index: 3;
        }}
    </style>
""", unsafe_allow_html=True)

url_list = []
response_list = []
i = 1


txt_file = st.file_uploader("Enter a text file here", type=['txt'])


# file uploaded is in bytes
if txt_file:
    # finding file name of text file
    file_name = txt_file.name
    # removing extension from file name
    file_name = file_name[:-4]
    st.info(file_name)

    urls_byte_format = txt_file.read()

    # converting bytes to string
    urls_string = urls_byte_format.decode('utf-8')

    # handling for when text file is empty
    if urls_string is not None:

        # Split the string into a list of urls by a \n character
        url_list = urls_string.split("\n")

        # displaying urls on screen
        # if url_list:
        #     for url in url_list:
        #         st.info(url)

        # message dictionary to be passed to openai
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Pretend you're an SEO expert. Create an optimized alt text for the image. Don't Explain any extra thing and always split one images alt by other via \n\n",
                    },
                ],
            }
        ]
        # appending new links to message dictionary so that can be send to gpt-4-vision-model
        for url in url_list:
            # this functions uses requests library to check if image urls are valid or not
            check_image = is_valid_image_url(url)
            if check_image:
                new_dict ={
                    "type": "image_url",
                    "image_url": {
                        "url": f"{url}",
                    },
                }
                messages[0]['content'].append(new_dict)



                # making a chatbot object and calling function to return alt texts
                seo_bot = functions.Chatbot()

                response = seo_bot.get_seo_optimized_words(messages)
                if response:
                    response_list.append(response)

                    # displaying alt text on screen
                    # st.info(response)
            else:
                # displaying error one time
                if i == 1:
                    st.info(f"An error occurred: Some of the urls are not valid image urls")
                    i += 1

    else:
        st.warning("Text File is empty")



    if response_list and url_list:
        data = [url_list, response_list]
        dataframe = pandas.DataFrame(data).transpose()
        # mentioning name of columns
        dataframe.columns = ["Image URL", "Suggested alt text"]
        desktop_path = functions.get_desktop_path()
        if os.path.exists(f"{desktop_path}/GPT-4-Alt-text-CSV-Files/{file_name}.csv"):
            if file_name[-1].isdigit():
                lastdigit = file_name[-1]
                lastdigit = int(lastdigit)
                lastdigit += 1
                file_name[-1] = lastdigit

        # writing data to csv file
        dataframe.to_csv(f"files/{file_name}.csv", index=False)








