import streamlit as st

# ==============================================================================
# 메인 허브 대시보드 (stream_pages/main.py)
# 공식 st.user 속성 참조: https://docs.streamlit.io/develop/api-reference/user/st.user
# ==============================================================================

# ==============================================================================
# 1. 로그인 인증 가드 (Auth Guard)
# 공식 문서: https://docs.streamlit.io/develop/api-reference/user
# ==============================================================================
if not st.user.is_logged_in:
    st.warning("🔒 로그인이 필요한 서비스입니다. 먼저 로그인해 주세요.")
    st.stop()

# 2. 페이지 헤더
st.title("🏠 메인 허브 대시보드")
st.caption("Google OAuth 2.0으로 인증된 사용자 전용 통합 포털")

st.markdown("### 👋 환영합니다!")
st.markdown("이곳은 Streamlit의 **멀티페이지 내비게이션 시스템**으로 구축된 통합 AI 스튜디오 포털입니다.")

st.divider()

# 2. st.user 공식 API 프로필 정보 렌더링
st.subheader("📋 사용자 인증 프로필 (`st.user`)")

if st.user.is_logged_in:
    st.success(f"현재 접속 계정: **{st.user.name}** (`{st.user.email}`)")
    
    with st.expander("🔍 OIDC 토큰 클레임 전체 데이터 (`st.user.to_dict()`)"):
        st.json(st.user.to_dict())

st.divider()

# 3. 서비스 바로가기 (st.switch_page 시연)
st.subheader("🚀 서비스 바로가기 (`st.switch_page`)")
st.caption("사이드바 메뉴 외에도 화면 내 버튼을 통해 원하는 페이지로 즉시 전환할 수 있습니다.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🤖 AI 챗봇", icon=":material/chat:", use_container_width=True):
        st.switch_page(r"stream_pages\chat.py")

with col2:
    if st.button("📊 통계 분석실", icon=":material/bar_chart:", use_container_width=True):
        st.switch_page(r"stream_pages\analytics.py")

with col3:
    if st.button("🧭 내비 가이드", icon=":material/explore:", use_container_width=True):
        st.switch_page(r"stream_pages\navigation.py")

with col4:
    if st.button("⚙️ 환경 설정", icon=":material/settings:", use_container_width=True):
        st.switch_page(r"stream_pages\settings.py")
