import streamlit as st

# ========================================================
# 좌측 사이드바 패널 분리 모듈
# ========================================================
def render_sidebar():
    """좌측 사이드바 설정 영역"""
    st.sidebar.header("⚙️ 사이드바 환경설정")

    # 테마 선택 드롭다운
    user_theme = st.sidebar.selectbox(
        "앱 테마를 선택하세요",
        options=["기본(Default)", "다크(Dark)", "라이트(Light)"],
        key="sidebar_theme"
    )

    # 글자 크기 배율 슬라이더
    font_size = st.sidebar.slider(
        "글자 크기 배율",
        min_value=1.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        key="sidebar_font"
    )

    # 선택된 설정 캡션 안내
    st.sidebar.caption(f"선택 테마: {user_theme} / 글자: {font_size}배")

