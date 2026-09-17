import streamlit as st

def render_sidebar():
    """위젯 랩 전용 사이드바 보조 패널"""
    with st.sidebar:
        with st.expander("🛠️ 위젯 랩 설정 가이드", expanded=False):
            st.caption("사이드바 컴포넌트 실습 영역입니다.")
            theme_choice = st.selectbox(
                "프리뷰 테마",
                options=["기본(Default)", "다크(Dark)", "라이트(Light)"],
                key="sidebar_lab_theme"
            )
            font_scale = st.slider(
                "폰트 배율 예시",
                min_value=1.0,
                max_value=1.5,
                value=1.0,
                step=0.1,
                key="sidebar_lab_font"
            )
            st.caption(f"설정값: {theme_choice} / {font_scale}x")
