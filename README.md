# AI-Powered Feedback Summarizer

This project provides a web-based solution for processing and summarizing customer feedback using Natural Language Processing (NLP) techniques. It utilizes Flask for the backend, Streamlit for the frontend, and Celery for asynchronous task processing.

## Features

- **Feedback Processing**: Accepts multiple feedbacks at once and processes them for sentiment analysis and summarization.
- **Language Detection**: Automatically detects the language of the feedback.
- **Asynchronous Processing**: Uses Celery to handle feedback processing tasks asynchronously.
- **PDF Report Generation**: Summarized feedback is converted into a downloadable PDF report.
- **Email Report Sending**: Sends the generated PDF summary report to the user via email.
- **Frontend Integration**: A simple user interface created using Streamlit for easy interaction.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
6. [Tasks and Celery](#tasks-and-celery)
7. [Email Configuration](#email-configuration)
8. [License](#license)

---

## Requirements

Before running the application, ensure you have the following dependencies installed:

### Backend (Flask + Celery + Redis)

```bash
pip install flask transformers langdetect celery smtplib fpdf redis
```

### Frontend
```bash
pip install streamlit requests
```
