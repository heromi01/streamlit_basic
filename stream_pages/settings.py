import streamlit as st

# ==============================================================================
# 시스템 및 사용자 설정 페이지 (settings.py)
# 공식 Form Elements: https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
# ==============================================================================

# ==============================================================================
# 1. 로그인 인증 가드 (Auth Guard)
# ==============================================================================
if not st.user.is_logged_in:
    st.warning("🔒 로그인이 필요한 서비스입니다. 먼저 로그인해 주세요.")
    st.stop()

# 2. 페이지 헤더
st.title("⚙️ 시스템 및 계정 설정")
st.caption("사용자 환경설정, 알림 옵션 및 계정 상태 관리")

st.markdown(
    """
    이 페이지에서는 로그인된 계정의 프로필 정보 확인과 앱 전반의 환경설정을 변경할 수 있습니다.
    """
)

st.divider()

# 2. 로그인 계정 정보 요약 카드
st.subheader("👤 현재 로그인된 계정 정보")

if st.user.is_logged_in:
    col_a, col_b = st.columns(2)
    with col_a:
        st.text_input("계정 이름", value=getattr(st.user, "name", "인증 사용자"), disabled=True)
    with col_b:
        st.text_input("이메일 주소", value=getattr(st.user, "email", "-"), disabled=True)
else:
    st.info("현재 로컬 또는 익명 세션 상태입니다.")

st.divider()

# 3. 환경설정 폼 (st.form)
st.subheader("🛠️ 환경설정 폼 (st.form)")
st.caption("`st.form`을 사용하면 여러 위젯의 값을 한 번에 묶어서 제출할 수 있습니다.")

with st.form(key="user_settings_form"):
    # 3-1. 알림 설정 토글
    email_notify = st.toggle("이메일 알림 받기", value=True, help="새로운 공지사항 및 업데이트 알림을 수신합니다.")
    sound_effects = st.toggle("효과음 및 사운드 활성화", value=False)

    # 3-2. 테마 모드 선택
    theme_choice = st.selectbox(
        "기본 인터페이스 테마 선택",
        options=["시스템 기본값 (자동)", "라이트 모드 (Apple Clean)", "다크 모드 (Midnight)"],
        index=0
    )

    # 3-3. 폼 제출 버튼
    submit_btn = st.form_submit_button("설정 저장하기", icon=":material/save:", type="primary")

    if submit_btn:
        st.success(f"설정이 성공적으로 저장되었습니다! (테마: {theme_choice}, 이메일 알림: {'ON' if email_notify else 'OFF'})")

