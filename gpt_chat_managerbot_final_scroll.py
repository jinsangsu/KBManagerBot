
import streamlit as st
import json
from difflib import get_close_matches

# 세션 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# Q&A 데이터 로딩
with open("매니저봇_QnA_챗봇포맷.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# 매니저 말투 응답 생성
def manager_response(user_input):
    questions = [item["question"] for item in qa_data]
    match = get_close_matches(user_input, questions, n=1, cutoff=0.4)
    if match:
        matched_q = match[0]
        matched_item = next((item for item in qa_data if item["question"] == matched_q), None)
        response = f"사장님, 문의하신 내용은 아래와 같습니다:\n\n"
        response += f"📝 **{matched_item['question']}**\n\n"
        response += f"{matched_item['answer']}\n"
        if matched_item.get("attachment_required"):
            response += "\n📎 참고로, 관련 서류나 문서가 필요합니다."
        if matched_item.get("branch"):
            response += f"\n📍 관련 지점: {matched_item['branch']}"
        return response
    else:
        return "사장님, 질문 내용을 조금 더 구체적으로 말씀해 주시면 제가 더 정확히 안내드릴 수 있습니다."

# UI
st.title("💬 매니저봇 자유입력 챗봇 (MVP)")
st.markdown("진짜 매니저처럼 답해주는 대화형 챗봇입니다. 자유롭게 질문해 주세요.")

# 채팅 입력
with st.form("chat_input_form", clear_on_submit=True):
    user_input = st.text_input("사장님, 무엇이 궁금하신가요?", value="", key="chat_input")
    submitted = st.form_submit_button("질문하기")

if submitted and user_input:
    reply = manager_response(user_input)
    st.session_state.chat_history.append(("사장님", user_input))
    st.session_state.chat_history.append(("매니저봇", reply))

# 채팅 히스토리 출력
for speaker, message in st.session_state.chat_history:
    if speaker == "사장님":
        st.markdown(f"🧑‍💼 **{speaker}:** {message}")
    else:
        st.markdown(f"🤖 **{speaker}:** {message}")

# 하단 여백 (스크롤 유도)
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
