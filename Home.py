import os.path

import pandas
import streamlit as st
import functions
import pandas as pd
import requests
import time

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
            check_image = functions.is_valid_image_url(url)
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
        if os.path.exists(f"files/{file_name}.csv"):
            if file_name[-1].isdigit():
                lastdigit = file_name[-1]
                lastdigit = int(lastdigit)
                lastdigit += 1
                file_name[-1] = lastdigit

        # writing data to csv file
        dataframe.to_csv(f"files/{file_name}.csv", index=False)




