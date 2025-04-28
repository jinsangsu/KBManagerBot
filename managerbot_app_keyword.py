
import streamlit as st
import json
from difflib import get_close_matches

st.set_page_config(page_title="매니저봇 Q&A", layout="wide")

# 데이터 불러오기
with open("매니저봇_QnA_챗봇포맷.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# 키워드 기반 룰셋 (간단 버전)
keyword_map = {
    "자동이체": "자동이체시 타인 계좌로 등록은 어떻게 하나요?",
    "타인카드": "타인카드 등록 시 구비서류는 무엇인가요?",
    "무이자": "자동차 카드 무이자 할부는 어떻게 되나요?",
    "스캔": "이건 스캔은 장기에서 하나요?",
    "배서": "장기 변경배서 시 계약자와 피보험자가 틀린 경우 필요한 서류는 무엇인가요?",
    "승환": "이 계약건은 승환계약인가요?",
    "계약": "이 계약건은 승환계약인가요?"
}

st.title("📌 매니저봇 - 설계사 Q&A 응답 시스템")
st.markdown("설계사분들이 자주 묻는 질문을 자유롭게 입력해 주세요. 가장 유사한 질문을 찾아 자동으로 답변해 드립니다.")

user_input = st.text_input("질문을 입력하세요", "")

if user_input:
    matched_item = None

    # 1. 키워드 우선 매칭
    for keyword, mapped_question in keyword_map.items():
        if keyword in user_input:
            matched_item = next((item for item in qa_data if item["question"] == mapped_question), None)
            break

    # 2. 유사도 기반 매칭 (백업)
    if not matched_item:
        questions = [item["question"] for item in qa_data]
        match = get_close_matches(user_input, questions, n=1, cutoff=0.4)
        if match:
            matched_item = next(item for item in qa_data if item["question"] == match[0])

    # 출력
    if matched_item:
        st.success(f"📌 관련 질문: {matched_item['question']}")
        st.markdown(f"**✅ 답변:** {matched_item['answer']}")
        if matched_item["attachment_required"]:
            st.info("📎 관련 서류나 문서 첨부가 필요합니다.")
        st.caption(f"📍 관련 지점: {matched_item['branch']}")
    else:
        st.warning("죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다. 다시 표현을 바꿔서 질문해 주세요.")
