import streamlit as st

# ==============================================================================
# AI 대화형 챗봇 페이지 (chat.py)
# 공식 Chat Elements: https://docs.streamlit.io/develop/api-reference/chat
# ==============================================================================

# ==============================================================================
# 1. 로그인 인증 가드 (Auth Guard)
# ==============================================================================
if not st.user.is_logged_in:
    st.warning("🔒 로그인이 필요한 서비스입니다. 먼저 로그인해 주세요.")
    st.stop()

# 2. 페이지 헤더 및 안내
st.title("🤖 AI 어시스턴트 챗봇")
st.caption("Streamlit 공식 `st.chat_message` 및 `st.chat_input` 기반 실시간 대화 인터페이스")

st.markdown(
    """
    이 페이지는 Streamlit의 내장 채팅 요소를 활용하여 사용자와 AI 어시스턴트 간의 대화 흐름을 시연합니다.
    질문을 입력하거나 아래 추천 프롬프트를 클릭해 보세요.
    """
)

st.divider()

# 2. 세션 상태(st.session_state)를 활용한 대화 히스토리 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요? 편하게 질문해 주세요."}
    ]

# 3. 기존 대화 기록 화면에 출력
for msg in st.session_state.chat_messages:
    # st.chat_message(role): 'user' 또는 'assistant'에 맞춰 대화 버블 렌더링
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. 사용자 입력 처리 (st.chat_input)
user_prompt = st.chat_input("AI에게 물어보고 싶은 내용을 입력하세요...")

if user_prompt:
    # 4-1. 사용자 질문 세션에 추가 및 즉시 출력
    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    # 4-2. 어시스턴트 응답 생성 (예시 에코 및 가이드 응답)
    response_text = f"'{user_prompt}'에 대해 문의해 주셨군요! 현재 Streamlit 멀티페이지 네비게이션 환경에서 원활하게 동작하고 있습니다."
    
    st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.write(response_text)

# 5. 빠른 대화 초기화 버튼
if len(st.session_state.chat_messages) > 1:
    if st.button("대화 기록 초기화", icon=":material/refresh:"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "대화 기록이 초기화되었습니다. 새로운 질문을 입력해 주세요."}
        ]
        st.rerun()

