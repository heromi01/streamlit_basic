import streamlit as st
from styles import apply_custom_css

# ========================================================
# 1. 페이지 기본 설정
# ========================================================
st.set_page_config(
    page_title="Streamlit AI Studio & 위젯 랩",
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
            "📈 관리자 통계 분석실",
            "📚 Streamlit 위젯 랩"
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

elif menu == "📚 Streamlit 위젯 랩":
    from tabs.sidebar import render_sidebar
    from tabs.group_inputs import render_inputs_group
    from tabs.group_layouts import render_layouts_group
    from tabs.group_visualizations import render_visualizations_group
    from tabs.group_status_media import render_status_media_group

    # 위젯 랩 브랜딩 헤더
    st.markdown(
        """
        <div class="app-brand-header">
            <div>
                <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.02em;">📚 Streamlit 핵심 기능 & 위젯 랩</h2>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">
                    입력 위젯 • 레이아웃 및 컨테이너 • 시각화 차트 • 상태 알림 및 미디어 인터랙티브 학습
                </p>
            </div>
            <div class="brand-pill">
                <span class="status-dot"></span>
                <span>Interactive Docs</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 상위 탭 그룹 생성
    tab_group_inputs, tab_group_layouts, tab_group_charts, tab_group_status = st.tabs([
        "🎛️ 입력 위젯",
        "📐 레이아웃 & 컨테이너",
        "📊 데이터 & 시각화",
        "🎨 상태 알림 & 미디어"
    ])

    with tab_group_inputs:
        render_inputs_group()

    with tab_group_layouts:
        render_layouts_group()

    with tab_group_charts:
        render_visualizations_group()

    with tab_group_status:
        render_status_media_group()
