from os import path

import streamlit as st
import pandas as pd
import time
import functions

# finding current date and time
current_time = time.localtime()
day = time.strftime("%d", current_time)
month = time.strftime("%B", current_time)
year = time.strftime("%Y", current_time)
date = f"{day}-{month}-{year}"

st.markdown(f"<p style='text-align: right;'>{date}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>✨Image to SEO keywords✨</h1>", unsafe_allow_html=True)


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

url_list = None
response = None

# side bar
selected_role = st.sidebar.selectbox("Select Role", ["Default Role", "Custom Role"])
split_by = st.sidebar.selectbox("How urls are seperated by each other", ["Enter", "Space", "Comma (, )", "Custom Character"])

# action upon side bar role selection
if selected_role == "Default Role":
    role = "Pretend you're an SEO expert. Create an optimized alt text for the image. Don't Explain any extra thing and always split one images alt by other via \n\n"
elif selected_role == "Custom Role":
    st.sidebar.text_input("Enter Custom Role")

# check by which characters urls are separated
if split_by == "Enter":
    split_by_char = "\n"
elif split_by == "Space":
    split_by_char = " "
elif split_by == "Comma":
    split_by_char = ", "
else:
    st.sidebar.text_input("Character or string which separates urls")

# ask from user how he want to save the file
save_choice = st.sidebar.selectbox("Select an option to save csv file", ["Save with date", "Save with name", "Append to an old file"])
if save_choice == "Save with name":
    file_name = st.sidebar.text_input("Enter name of the text file")
elif save_choice == "Save with date":
    file_name = date
elif save_choice == "Append to an old file":
    pass

url_string = st.text_area("Enter multiple urls here")

# Split the string into a list of URLs using whitespace characters
if url_string:
    url_list = url_string.split(f"{split_by_char}")

# message dictionary to be passed to openai
    messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{role}",
                        },
                    ],
                }
            ]

if url_list:
    for url in url_list:
        new_dict ={
                    "type": "image_url",
                    "image_url": {
                     "url": f"{url}",
                    },
                   }
        messages[0]['content'].append(new_dict)



seo_bot = functions.Chatbot()





if url_list is not None:
    response = seo_bot.get_seo_optimized_words(messages)

    response_list = response.split("\n\n")

    # displaying alt text on screen
    st.info(response)





