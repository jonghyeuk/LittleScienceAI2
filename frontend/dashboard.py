# 🔹 frontend/dashboard.py

import streamlit as st
import requests

st.set_page_config(page_title="LittleScienceAI", layout="centered")
st.title("🧬 LittleScienceAI 논문 주제 도우미")

backend_url = "http://localhost:8000"  # FastAPI 실행 주소

user_input = st.text_input("🔍 연구하고 싶은 과학 주제를 입력하세요:")

if st.button("주제 분석 시작"):
    with st.spinner("🔎 주제 정보 수집 중..."):
        res = requests.post(f"{backend_url}/query", json={"input_text": user_input})
        result = res.json()

        st.subheader("📘 주제 개요 및 정의")
        st.write(result["summary"])

        st.subheader("🔥 관련 사회적/과학적 이슈")
        st.write(result["issues"])

        st.subheader("📚 유사 논문 (ISEF 기반)")
        st.write(result["similar_titles"])

        st.session_state.references = result["similar_titles"]
        st.session_state.topic = user_input

if "references" in st.session_state:
    if st.button("✍️ 논문 형식으로 생성"):
        with st.spinner("논문 생성 중..."):
            res = requests.post(f"{backend_url}/generate-paper", json={
                "topic": st.session_state.topic,
                "references": st.session_state.references
            })
            paper = res.json()["inferred_paper"]
            st.subheader("📄 자동 생성된 논문")
            st.markdown(paper)
