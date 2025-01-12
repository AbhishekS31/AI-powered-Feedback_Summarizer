import streamlit as st
import requests

st.title('AI-Powered Feedback Summarizer')

feedback_input = st.text_area('Enter Feedback (one per line):', height=200)

if st.button('Process Feedback'):
    feedback_list = feedback_input.split('\n')
    response = requests.post('http://localhost:5000/process-feedback', json={'feedback': feedback_list})
    if response.status_code == 200:
        summaries = response.json()
        for item in summaries:
            st.write(f"Feedback: {item['feedback']}")
            st.write(f"Sentiment: {item['sentiment']}")
            st.write(f"Summary: {item['summary']}")
            st.write('---')
    else:
        st.error('Error processing feedback.')

