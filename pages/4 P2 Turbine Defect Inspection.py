import streamlit as st

st.title("Project Summary")
st.markdown('''
            This project is composed of two parts. The first part is performing LiDAR data and 360 image data collection.  
            The LiDAR data is collected by Faro Focus Scanner and 360 image data is collected by insta360 Titan camera. 
            The data were collected in 2024, which can be used for future studies. 
            If the data is collected during every maintenance, the differences among data can indicate the damage expansion based on location depth information. 
            Therefore, the damage can be monitored.''')

            # FARO
            # 360 camera
            
st.markdown('''The second part is building a damage detection system from previous inspection images. 
            The previous inspection images were distributed in the previous inspection log from the year 2013 to 2023. 
            The goal of the damage detection system is to automate the localization and quantification of damage on turbine blade images to reduce human efforts and errors. 
            To train the machine learning model, it needs a large amount of training set with labels. 
            However, the raw image contained in inspection logs has some noise from a training perspective, and only 60 images can be. 
            Therefore, this study applied state-of-the-art synthetic image generation methods to increase the training set and enhance model performance.
            The damage detection model was trained and provided for future inference. The inference process is demonstrated in the User Guide.
            ''')

            # data
            # pred
