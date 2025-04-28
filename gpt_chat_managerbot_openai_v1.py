
import streamlit as st
import json
from openai import OpenAI

# Q&A 데이터 로딩
with open("매니저봇_QnA_챗봇포맷.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 시스템 메시지 초기화
system_prompt = {
    "role": "system",
    "content": (
        "당신은 KB손해보험의 '매니저봇'입니다. 질문자는 설계사이며, 당신은 그를 '사장님'이라고 존중어로 호칭합니다. "
        "답변은 친절하고 정확하며, 실제 매니저처럼 단정하게 설명해 주세요. "
        "가능하면 아래 Q&A를 참고해 해당 내용에 기반해 응답하세요. "
        "내용이 명확하지 않으면 사장님께 되묻거나 유도 질문을 해도 좋습니다.\n\n"
        "다음은 참고할 수 있는 Q&A입니다:\n\n" +
        "\n".join([
            f"Q: {item['question']}\nA: {item['answer']}" +
            (f" (관련 지점: {item['branch']})" if item.get("branch") else "") +
            (f" [서류 필요]" if item.get("attachment_required") else "")
            for item in qa_data
        ])
    )
}

# Streamlit UI
st.title("💬 매니저봇 생성형 GPT 챗봇 (최신 버전)")
st.caption("자연스럽게 대화하세요. 사장님의 질문을 매니저처럼 응대합니다.")

api_key = st.text_input("🔐 OpenAI API Key를 입력해 주세요", type="password")

user_input = st.text_input("✍️ 사장님의 질문:", key="user_input")

if api_key and user_input:
    client = OpenAI(api_key=api_key)

    if len(st.session_state.messages) == 0:
        st.session_state.messages.append(system_prompt)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("매니저봇이 응답 중입니다..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# 대화 히스토리 출력
for msg in st.session_state.messages[1:]:  # system prompt 제외
    speaker = "🧑‍💼 사장님" if msg["role"] == "user" else "🤖 매니저봇"
    st.markdown(f"**{speaker}:** {msg['content']}")
