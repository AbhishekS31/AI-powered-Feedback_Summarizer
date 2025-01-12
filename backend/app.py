from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load sentiment analysis and summarization pipelines
sentiment_pipeline = pipeline('sentiment-analysis')
summarizer_pipeline = pipeline('summarization')

@app.route('/process-feedback', methods=['POST'])
def process_feedback():
    data = request.json.get('feedback', [])
    summaries = []
    for feedback in data:
        sentiment = sentiment_pipeline(feedback)[0]
        summary = summarizer_pipeline(feedback, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
        summaries.append({
            'feedback': feedback,
            'sentiment': sentiment['label'],
            'summary': summary
        })
    return jsonify(summaries)

if __name__ == '__main__':
    app.run(debug=True)
