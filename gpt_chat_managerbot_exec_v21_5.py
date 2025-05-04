
import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="매니저봇 애순", page_icon="🧕", layout="centered")

st.markdown("## 🧕 사장님, 안녕하세요!")
st.markdown("설계사 사장님들의 질문에 친절하게 응답하는 **충청호남본부 전용 매니저봇**입니다.")

st.image("managerbot_character.png", width=180)

# 질문 입력 UI
user_input = st.chat_input("애순이에게 무엇이든 물어보세요")

# Q&A 데이터 로딩
def load_qa_data():
    try:
        with open("qa_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

qa_data = load_qa_data()

# GPT 호출
def ask_gpt(message):
    try:
        response = requests.post(
            "http://localhost:8000/managerbot",
            json={"message": message},
            timeout=10
        )
        return response.json()["response"]
    except Exception as e:
        return f"애순이가 지금은 답변을 드릴 수 없어요. (서버 오류일 수 있어요.)"

# Q&A 매칭 함수
def get_answer_from_qa(user_q):
    for pair in qa_data:
        if pair["question"].strip() in user_q:
            return pair["answer"]
    return None

# 입력 처리
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # 우선 Q&A에서 매칭 시도
    matched_answer = get_answer_from_qa(user_input)
    if matched_answer:
        with st.chat_message("assistant"):
            st.markdown(matched_answer)
    else:
        # GPT에게 질문 전달
        answer = ask_gpt(user_input)
        with st.chat_message("assistant"):
            st.markdown(answer)
