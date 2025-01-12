import streamlit as st
import requests

st.title('AI-Powered Feedback Summarizer')

feedback_input = st.text_area('Enter Feedback (one per line):', height=200)
user_email = st.text_input('Enter your email to receive the summary report:')

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
            st.write('Feedback processing complete!')

            # Trigger email sending
            email_response = requests.post('http://localhost:5000/send-report', json={'email': user_email, 'feedback': results})
            if email_response.status_code == 200:
                st.success('Summary report sent to your email!')
            else:
                st.error('Failed to send the email. Please try again.')
            break
        elif status == 'FAILURE':
            st.error('Error in processing feedback.')
            break
