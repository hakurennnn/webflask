import streamlit as st
from viewfinder import facial_emotion_analysis

# Render the app header
st.markdown("<h1>Facial Emotion Analysis</h1>", unsafe_allow_html=True)

# Add a button to start the facial emotion analysis
if st.button("Start Facial Emotion Analysis"):
    facial_emotion_analysis()
