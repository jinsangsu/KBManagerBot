
import streamlit as st
import openai
import json

# GPT 호출용 함수
def ask_gpt(prompt, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        temperature=0.4
    )
    return response.choices[0].message.content

# Q&A 데이터 불러오기
with open("매니저봇_QnA_챗봇포맷.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# 시스템 프롬프트 생성
system_prompt = {
    "role": "system",
    "content": (
        "당신은 KB손해보험의 '매니저봇'입니다. "
        "질문자는 설계사이며, 당신은 그를 '사장님'이라고 존중어로 호칭합니다. "
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

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

st.title("💬 매니저봇 생성형 GPT 챗봇 (Beta)")
st.caption("사장님, 무엇이든 편하게 질문해 주세요. 매니저가 바로 응답해 드립니다.")

api_key = st.text_input("🔐 OpenAI API Key를 입력해 주세요", type="password")

user_input = st.text_input("✍️ 사장님의 질문:", key="user_input")

if user_input and api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("매니저봇이 답변 중입니다..."):
        reply = ask_gpt(st.session_state.messages, api_key)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 대화 히스토리 출력
for msg in st.session_state.messages[1:]:
    speaker = "🧑‍💼 사장님" if msg["role"] == "user" else "🤖 매니저봇"
    st.markdown(f"**{speaker}:** {msg['content']}")
