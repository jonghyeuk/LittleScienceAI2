# 🔹 app/services/nlp_processor.py
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def process_meaning(raw_text: str):
    summary = summarizer(raw_text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
    # 추가 이슈는 심플하게 구분 (임시)
    issues = [line.strip() for line in summary.split('.') if '문제' in line or '이슈' in line]
    return summary, issues
