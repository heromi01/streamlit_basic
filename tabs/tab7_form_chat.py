import streamlit as st

# ========================================================
# 7. 폼(Form) & 챗봇 UI 모듈
# ========================================================
def render_tab7():
    """st.form 일괄 제출 패턴 및 st.chat_message/st.chat_input 대화형 인터페이스"""
    st.subheader("7. 폼 양식(Form) & 챗봇 대화 인터페이스 (Chat UI)")
    st.markdown("매번 페이지가 재실행되는 것을 방지하는 **일괄 폼(Form)**과 최신 LLM 서비스 필수 요소인 **대화형 챗봇 UI**입니다.")

    # (1) st.form & st.form_submit_button (일괄 제출 폼)
    st.markdown("#### (1) 일괄 제출 양식 (`st.form` & `st.form_submit_button`)")
    st.caption("기본 Streamlit은 위젯 값을 바꿀 때마다 전체 코드가 다시 실행되지만, `st.form`으로 묶으면 '제출' 버튼을 누를 때까지 실행을 보류합니다.")

    # clear_on_submit=False: 제출 후에도 입력값 유지
    with st.form("user_registration_form", clear_on_submit=False):
        st.markdown("**회원 가입 신청 양식**")
        # 각 입력 위젯에 고유 key를 부여하여 상태 충돌을 방지합니다.
        form_name = st.text_input("신청자 성함", value="이순신", key="tab7_form_name")
        form_role = st.selectbox("지원 직무", options=["프론트엔드", "백엔드", "데이터 엔지니어", "AI 연구원"], key="tab7_form_role")
        form_experience = st.slider("경력 (연차)", min_value=0, max_value=20, value=3, key="tab7_form_exp")
        form_agree = st.checkbox("제출 약관에 동의합니다", value=True, key="tab7_form_agree")

        # 폼 내부 전용 제출 버튼 (이 버튼을 눌러야만 전체 폼 데이터가 한 번에 전송됨)
        form_submitted = st.form_submit_button("가입 신청 제출하기", type="primary")

    if form_submitted:
        st.success(f"신청 완료! [성함: {form_name}, 직무: {form_role}, 경력: {form_experience}년]")

    st.divider()

    # (2) 대화형 챗봇 UI (st.chat_message & st.chat_input)
    st.markdown("#### (2) AI 챗봇 대화형 UI (`st.chat_message` & `st.chat_input`)")
    st.caption("사용자(`user`)와 인공지능 어시스턴트(`assistant`) 간의 대화 말풍선 인터페이스입니다.")

    # 세션 상태(st.session_state)를 통한 대화 기록 유지
    if "tab7_chat_messages" not in st.session_state:
        st.session_state.tab7_chat_messages = [
            {"role": "user", "content": "Streamlit으로 만든 챗봇 화면이 궁금해요!"},
            {"role": "assistant", "content": "`st.chat_message`를 사용하면 아바타 아이콘과 함께 깔끔한 말풍선이 생성됩니다! 아래 채팅 입력창도 테스트해보세요."}
        ]

    # 대화 기록 순차 출력
    for msg in st.session_state.tab7_chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 하단 채팅 입력 위젯 (고유 key 부여)
    chat_prompt = st.chat_input("챗봇에게 메시지를 입력해보세요...", key="tab7_chat_input")
    if chat_prompt:
        st.session_state.tab7_chat_messages.append({"role": "user", "content": chat_prompt})
        st.session_state.tab7_chat_messages.append({"role": "assistant", "content": f"입력하신 메시지를 확인했습니다: **{chat_prompt}**"})
        st.rerun()

    st.divider()

    # (3) 파일 업로드 및 데이터 다운로드
    st.markdown("#### (3) 파일 업로드와 다운로드 (`st.file_uploader`, `st.download_button`)")
    st.caption("로컬 파일을 서버로 전송받거나 생성된 데이터를 사용자 컴퓨터로 다운로드합니다.")

    # type: 허용할 확장자
    uploaded_file = st.file_uploader("분석할 파일을 선택하세요", type=["txt", "csv"], key="tab7_file_up")
    if uploaded_file:
        st.write(f"업로드 완료 -> 파일명: **{uploaded_file.name}** (크기: {uploaded_file.size} bytes)")

    sample_memo = "이 파일은 Streamlit download_button 예제에서 생성된 텍스트입니다."
    st.download_button(
        label="샘플 메모 파일 다운로드 (.txt)",
        data=sample_memo,
        file_name="sample_streamlit_memo.txt",
        mime="text/plain",
        key="tab7_btn_download"
    )

