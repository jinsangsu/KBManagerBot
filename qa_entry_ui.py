
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="질문/답변 등록", page_icon="📝")

st.title("📝 매니저용 질문/답변 등록")
st.markdown("설계사님들이 자주 묻는 질문과 그에 대한 답변을 등록해 주세요.")
st.markdown("---")

qa_file = Path("qa_data.json")

# 기존 데이터 불러오기
if qa_file.exists():
    with open(qa_file, "r", encoding="utf-8") as f:
        qa_data = json.load(f)
else:
    qa_data = []

# 입력 폼
with st.form("qa_form", clear_on_submit=True):
    question = st.text_input("❓ 질문")
    answer = st.text_area("💬 답변", height=150)
    submitted = st.form_submit_button("등록하기")

    if submitted:
        if question.strip() == "" or answer.strip() == "":
            st.warning("질문과 답변 모두 입력해 주세요.")
        else:
            qa_data.append({
                "question": question.strip(),
                "answer": answer.strip()
            })
            with open(qa_file, "w", encoding="utf-8") as f:
                json.dump(qa_data, f, ensure_ascii=False, indent=2)
            st.success("✅ 질문과 답변이 성공적으로 저장되었습니다!")

# 등록된 Q&A 미리보기
if qa_data:
    st.markdown("### 📋 현재까지 등록된 질문/답변")
    for idx, item in enumerate(reversed(qa_data[-5:]), 1):
        st.markdown(f"**{idx}. {item['question']}**")
        st.markdown(f"🟢 {item['answer']}")
        st.markdown("---")
