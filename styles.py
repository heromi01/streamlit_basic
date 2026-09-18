import os
import streamlit as st

# 템플릿 디렉토리 경로
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def _load_template(filename: str) -> str:
    """templates 디렉토리에서 HTML 또는 CSS 파일을 로드합니다."""
    filepath = os.path.join(TEMPLATE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def apply_custom_css():
    """Apple 디자인 시스템 CSS(templates/apple_theme.css)를 앱 전역에 주입합니다."""
    css_content = _load_template("apple_theme.css")
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def render_login_card():
    """Apple 프로스티드 글래스 로그인 카드(templates/login_card.html)를 렌더링합니다."""
    html_content = _load_template("login_card.html")
    if html_content:
        st.markdown(html_content, unsafe_allow_html=True)

def render_user_profile(name: str, email: str):
    """인증된 사용자 프로필 뱃지(templates/user_profile.html)를 렌더링합니다."""
    html_content = _load_template("user_profile.html")
    if html_content:
        rendered = html_content.replace("{{ name }}", str(name)).replace("{{ email }}", str(email))
        st.markdown(rendered, unsafe_allow_html=True)
