from flask import Flask, request, jsonify
from transformers import pipeline
from langdetect import detect
import sqlite3
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDFss

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize NLP pipelines
sentiment_pipeline = pipeline('sentiment-analysis')
summarizer_pipeline = pipeline('summarization')

# Database setup
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY, text TEXT, sentiment TEXT, summary TEXT, category TEXT, language TEXT)''')
    conn.commit()
    conn.close()

@celery.task
def process_feedback_task(feedback_texts):
    results = []
    for feedback in feedback_texts:
        language = detect(feedback)
        sentiment = sentiment_pipeline(feedback)[0]['label']
        summary = summarizer_pipeline(feedback, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
        category = "General"  # Placeholder for keyword extraction logic
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute("INSERT INTO feedback (text, sentiment, summary, category, language) VALUES (?, ?, ?, ?, ?)",
                  (feedback, sentiment, summary, category, language))
        conn.commit()
        conn.close()
        results.append({'feedback': feedback, 'sentiment': sentiment, 'summary': summary, 'category': category, 'language': language})
    return results

@app.route('/process-feedback', methods=['POST'])
def process_feedback():
    data = request.json.get('feedback', [])
    task = process_feedback_task.delay(data)
    return jsonify({'task_id': task.id}), 202

@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_feedback_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'error': str(task.info)}
    return jsonify(response)

def generate_pdf(feedback_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Feedback Summary Report", ln=True, align='C')
    for item in feedback_data:
        pdf.cell(200, 10, txt=f"Feedback: {item['feedback']}", ln=True)
        pdf.cell(200, 10, txt=f"Sentiment: {item['sentiment']}", ln=True)
        pdf.cell(200, 10, txt=f"Summary: {item['summary']}", ln=True)
        pdf.cell(200, 10, txt="---", ln=True)
    pdf_file = "feedback_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

def send_email_report(email, pdf_file):
    msg = MIMEText("Your feedback summary report is attached.")
    msg['Subject'] = "Feedback Summary Report"
    msg['From'] = "your_email@example.com"  # Replace with your email
    msg['To'] = email

    with open(pdf_file, "rb") as attachment:
        part = MIMEText(attachment.read(), "base64")
        part.add_header('Content-Disposition', 'attachment', filename=pdf_file)
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")  # Replace with your email credentials
        server.send_message(msg)

@app.route('/send-report', methods=['POST'])
def send_report():
    data = request.json
    email = data.get('email')
    feedback = data.get('feedback')

    pdf_file = generate_pdf(feedback)
    try:
        send_email_report(email, pdf_file)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
