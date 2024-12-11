import os
import streamlit as st
import pandas as pd


st.title("User Guide")
st.markdown('''
            The app is built to facilitate data analysis of IoT sensors for condition monitoring of Hydro Power Stations. 

            The dataset of Mormon Flat (MF2) Dam from period October 2020 - October 2023 sampled at every 5 minutes is used to build this app.

            It comprises of 42 sensors and their details (like sensor name, unit of measurement, location) is given below in a table as **Sensors Description**.

            📥 You can download the data using the Google Drive link shared by me on email. Else, if you were not copied on the email, please request it either from me (mgupta70@asu.edu) or Russell Genet (Russell.Genet@srpnet.com).

            The data is in pickle (.pkl) format which you can upload in the main app page for analysis.

            Apart from sensor data, we engineered some time-based features like year, month, day, etc and some domain-based features like mode, running_time etc.
            
            ''')

# Sensors Description
st.markdown("### Sensors Description")
sensors_summary = pd.read_csv("data/sensors_description.csv")
st.write(sensors_summary)


# Placeholder for the video
video_placeholder = st.empty()

# Optional: Show a message or image as a placeholder
video_placeholder.markdown("### Video walkthrough of the app :film_projector:")
# VIDEO_URL = "https://www.youtube.com/watch?v=HcRm0ILFHzw&ab_channel=KTARNews"
# st.video(VIDEO_URL)
video_file = open('media/condition_monitoring.mp4', "rb")
video_bytes = video_file.read()

st.video(video_bytes)

st.markdown('''In order to use app for custom data, feel free to modify the app. The source code should be visible to everyone at SRP.''')

st.markdown(
    '''
    ------------------------------------------------------------------------------------
    :man-raising-hand: In case of any query or suggestion, just send an email to me ([Mohit Gupta](https://mgupta70.github.io)) at :email: mgupta70@asu.edu
    '''
)

