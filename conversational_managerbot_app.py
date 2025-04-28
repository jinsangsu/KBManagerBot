
import streamlit as st

# 초기 세션 설정
if "step" not in st.session_state:
    st.session_state.step = 0
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "subquestion" not in st.session_state:
    st.session_state.subquestion = ""

st.title("💬 매니저봇 대화형 챗봇 (MVP)")

# Step 0: 키워드 입력
if st.session_state.step == 0:
    user_input = st.text_input("무엇이 궁금하신가요?", "")
    if user_input:
        # 아주 간단한 키워드 분류
        if "자동" in user_input:
            st.session_state.topic = "자동이체"
            st.session_state.step = 1
        elif "무이자" in user_input or "할부" in user_input:
            st.session_state.topic = "무이자"
            st.session_state.step = 1
        elif "카드" in user_input and "등록" in user_input:
            st.session_state.topic = "타인카드"
            st.session_state.step = 1
        elif "스캔" in user_input:
            st.session_state.topic = "스캔"
            st.session_state.step = 1
        elif "승환" in user_input:
            st.session_state.topic = "승환계약"
            st.session_state.step = 1
        elif "배서" in user_input or "계약자" in user_input:
            st.session_state.topic = "장기배서"
            st.session_state.step = 1
        else:
            st.write("조금만 더 구체적으로 입력해 주세요. 예: '자동이체 계좌 변경'")

# Step 1: 유도 질문
if st.session_state.step == 1:
    topic = st.session_state.topic
    st.subheader(f"📌 [{topic}] 관련하여 어떤 부분이 궁금하신가요?")
    if topic == "자동이체":
        options = ["신규 계좌 등록", "가족 명의 계좌", "자동이체 해지", "은행 변경", "기타"]
    elif topic == "무이자":
        options = ["무이자 가능 여부", "조건", "카드사 목록", "기타"]
    elif topic == "타인카드":
        options = ["구비서류", "가족카드", "미성년 자녀 카드", "기타"]
    elif topic == "스캔":
        options = ["장기계약", "장기배서", "자동이체", "지금(즉시이체)", "고객서류"]
    elif topic == "승환계약":
        options = ["청약화면 확인법", "계약상태 기준", "기타"]
    elif topic == "장기배서":
        options = ["계약자/피보험자 다름", "수익자 동의", "증권 제출 생략", "기타"]
    else:
        options = []

    subq = st.radio("선택해 주세요:", options)
    if subq:
        st.session_state.subquestion = subq
        st.session_state.step = 2

# Step 2: 응답 출력
if st.session_state.step == 2:
    topic = st.session_state.topic
    sub = st.session_state.subquestion
    st.success(f"📌 질문: [{topic}] - {sub}")
    
    # 간단한 답변 매핑
    if topic == "자동이체" and sub == "가족 명의 계좌":
        st.write("- 예금주 신분증
- 계약자 신분증
- 가족관계증명서(3개월 이내)")
    elif topic == "타인카드" and sub == "구비서류":
        st.write("- 계약자 신분증
- 카드 소유주 신분증")
    elif topic == "스캔" and sub == "자동이체":
        st.write("📎 자동이체 스캔은 '입출금 스캔'으로 분류해 주세요.")
    elif topic == "승환계약" and sub == "청약화면 확인법":
        st.write("청약화면 팝업에서 승환 여부를 확인할 수 있습니다.")
    elif topic == "장기배서" and sub == "계약자/피보험자 다름":
        st.write("- 계약자 신분증
- 수익자 신분증
- 증권 원본 제출 시 수익자 동의 생략 가능")
    else:
        st.info("이 항목에 대한 답변은 곧 추가 예정입니다.")
