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

# ========================================================
# 2. 사이드바 단일 통합 내비게이션
# ========================================================
if "current_menu" not in st.session_state:
    st.session_state["current_menu"] = "🤖 AI 멀티모달 챗봇"

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1rem 0;">
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
# 3. 메뉴별 화면 라우팅
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
