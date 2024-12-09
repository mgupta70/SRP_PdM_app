import os
import streamlit as st


st.title("LiDAR & 360 Image Data Curation")
st.markdown('''This sectoin describes the scan plan of LiDAR and 360 image data collection process and the link to dataset.''')

st.image("media/point_cloud_top.png", caption="Fig 1. Collected Point Cloud Top View")
st.image("media/point_cloud_bottom.png", caption="Fig 2. Collected Point Cloud Bottom View")
st.image("media/360img.png", caption="Fig 3. Collected 360 Image Example")

st.markdown('''Following is the detailed scan plan for data collection.''')

from streamlit_pdf_viewer import pdf_viewer
pdf_viewer("media/turbine_scan_plan.pdf")



