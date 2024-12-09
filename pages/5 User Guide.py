import os
import streamlit as st

st.markdown('''Following is the user guide for utilizing a trained model to predict defects on turbine inspection images.''')
  
# Placeholder for the video
video_placeholder = st.empty()
video_placeholder.markdown("### Video walkthrough of Running Turbine Defect Detection System")
VIDEO_URL = "https://www.dropbox.com/scl/fi/ysy73t0rv1pw3dqzv1tqt/damage_detection_demo.mp4?rlkey=nr7nv5pmfy1efeeejc2q1c5p8&dl=0"
st.video(VIDEO_URL)

st.markdown('''In order to use app for custom data, feel free to modify the app. The source code should be visible to everyone at SRP.''')

st.markdown(
    '''
    ------------------------------------------------------------------------------------
    :woman-raising-hand: In case of any query or suggestion, just send an email to me at :email: cwei32@asu.edu
    '''
)
