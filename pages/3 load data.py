import streamlit as st
import pandas as pd
import io

# File uploader for a single .pkl file
uploaded_file = st.file_uploader("Upload a .pkl file", type='pkl', accept_multiple_files=False)

if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    try:
        # Load the DataFrame from the uploaded file
        df = pd.read_pickle(uploaded_file)

        # Display the DataFrame
        st.write(df)

    except Exception as e:
        st.error(f"Error loading the file: {e}")


