# 🔹 app/services/scholar_api.py
import requests

def get_scholar_data(topic: str) -> str:
    # 실제 arXiv API 호출 or mock
    url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results=3"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "관련 학술 정보를 가져오는 데 실패했습니다."
