
import streamlit as st
import json
from openai import OpenAI
from difflib import get_close_matches

api_key = "sk-uwPZs8OoY96kRj0ABC12345FAKEKEYEXAMPLE98765"

with open("매니저봇_QnA_챗봇포맷.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

if "messages" not in st.session_state:
    st.session_state.messages = []

def build_prompt(user_input):
    questions = [item["question"] for item in qa_data]
    matches = get_close_matches(user_input, questions, n=2, cutoff=0.4)

    matched_qas = []
    for q in matches:
        for item in qa_data:
            if item["question"] == q:
                matched_qas.append("Q: " + item["question"] + "\nA: " + item["answer"])

    reference = "\n\n".join(matched_qas) if matched_qas else "참고할 Q&A가 없습니다."

    return [
        {
            "role": "system",
            "content": (
                "당신은 KB손해보험의 '매니저봇'입니다. 질문자는 설계사이며, 당신은 그를 '사장님'이라고 존중어로 호칭합니다. "
                "답변은 친절하고 정확하며, 실제 매니저처럼 단정하게 설명해 주세요. "
                "내용이 명확하지 않으면 사장님께 되묻거나 유도 질문을 해도 좋습니다.\n\n"
                "다음은 참고할 수 있는 Q&A입니다:\n\n" + reference
            )
        },
        {"role": "user", "content": user_input}
    ]

st.title("💬 매니저봇 생성형 GPT 챗봇 (충호해 테스트용)")
st.caption("사장님, 질문해 보세요. 테스트용 매니저봇이 응답해 드립니다.")

user_input = st.text_input("✍️ 사장님의 질문:", key="user_input")

if user_input:
    client = OpenAI(api_key=api_key)
    messages = build_prompt(user_input)

    with st.spinner("매니저봇이 응답 중입니다..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append(("사장님", user_input))
        st.session_state.messages.append(("매니저봇", assistant_reply))

for speaker, content in st.session_state.messages:
    icon = "🧑‍💼" if speaker == "사장님" else "🤖"
    st.markdown(f"**{icon} {speaker}:** {content}")
