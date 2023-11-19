import os
import glob
import pandas
import streamlit as st

# saving directory path
directory_path = f"files\\"

# finding all folders in directory
folder_dir = os.listdir(directory_path)
csv_file_names = [dir for dir in folder_dir]

# making a radio button based on directory file names which are csv files name
selected_file = st.sidebar.radio("Select CSV file to display", csv_file_names)

# checking for every file which one is selected
for csv_file in csv_file_names:
    if selected_file == csv_file:
        st.header("CSV file veiwer")
        st.info(f"File Name : {csv_file}")
        # based on selected day diplaying images
        csv_files = glob.glob(f"files/*.csv")
        if len(csv_files) == 0:
            st.warning("Nothing to show here")
        else:
            dataframe = pandas.read_csv(f"files/{csv_file}")
            st.dataframe(dataframe)