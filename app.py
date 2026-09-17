import streamlit as st
from styles import apply_custom_css

# ========================================================
# 1. 페이지 기본 설정
# ========================================================
st.set_page_config(
    page_title="Streamlit AI Studio & 통계 분석실",
    page_icon="⚡",
    layout="wide"
)

# 모던 디자인 시스템 전역 주입
apply_custom_css()

# 포털 통합 구동 플래그 (사이드바 중복 방지)
st.session_state["is_portal_mode"] = True

# ========================================================
# 2. 최상위 전역 로그인 게이트 (보안 차단)
# - 미인증 사용자는 사이드바 메뉴 및 모든 페이지 접근 원천 차단
# ========================================================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    from app2 import show_login_page
    show_login_page()
    # 로그인하기 전에는 아래 사이드바 및 대화 히스토리/통계 분석실 렌더링을 완전히 차단
    st.stop()

# ========================================================
# 3. 로그인 완료 후 사이드바 단일 통합 내비게이션
# ========================================================
if "current_menu" not in st.session_state:
    st.session_state["current_menu"] = "🤖 AI 멀티모달 챗봇"

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 0.5rem 0;">
            <h3 style="margin: 0; font-weight: 800; letter-spacing: -0.02em; color: #6366f1;">
                ⚡ AI Studio
            </h3>
            <p style="margin: 2px 0 0 0; font-size: 0.8rem; color: #888888;">
                Streamlit & OpenAI Integrated Hub
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 로그인 사용자 정보 표시 및 전체 로그아웃 버튼
    st.markdown(f"👤 접속자: **{st.session_state.get('login_user', '사용자')}**님")
    if st.button("🚪 전체 로그아웃", use_container_width=True, key="portal_logout_btn"):
        st.session_state.is_logged_in = False
        st.session_state.is_admin_authenticated = False
        st.session_state.login_user = ""
        st.rerun()

    st.divider()

    menu = st.radio(
        "메인 내비게이션",
        [
            "🤖 AI 멀티모달 챗봇",
            "📜 대화 히스토리 & 분석",
            "📈 관리자 통계 분석실"
        ],
        key="current_menu",
        label_visibility="collapsed"
    )
    st.markdown("---")

# ========================================================
# 4. 메뉴별 화면 라우팅 (인증된 사용자만 접근 가능)
# ========================================================
if menu == "🤖 AI 멀티모달 챗봇":
    from app2 import show_chat_page
    show_chat_page()

elif menu == "📜 대화 히스토리 & 분석":
    from app2_history import show_history_page
    show_history_page()

elif menu == "📈 관리자 통계 분석실":
    from admin_analytics import show_admin_analytics_page
    show_admin_analytics_page()
