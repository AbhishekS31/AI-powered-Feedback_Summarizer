import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title('AI-Powered Feedback Summarizer')

feedback_input = st.text_area('Enter Feedback (one per line):', height=200)

if st.button('Process Feedback'):
    feedback_list = feedback_input.strip().split('\n')
    response = requests.post('http://localhost:5000/process-feedback', json={'feedback': feedback_list})
    task_id = response.json().get('task_id')
    st.write('Processing feedback...')

    # Polling task status
    while True:
        status_response = requests.get(f'http://localhost:5000/task-status/{task_id}')
        status = status_response.json().get('state')
        if status == 'SUCCESS':
            results = status_response.json().get('result')
            df = pd.DataFrame(results)
            st.dataframe(df)

            # Sentiment Distribution Chart
            fig = px.pie(df, names='sentiment', title='Sentiment Distribution')
            st.plotly_chart(fig)
            break
        elif status == 'FAILURE':
            st.error('Error in processing feedback.')
            break
