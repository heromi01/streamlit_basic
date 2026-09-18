import os
from dotenv import load_dotenv
import streamlit as st
from streamlit.runtime.secrets import secrets_singleton
from styles import apply_custom_css, render_login_card, render_user_profile

# ==============================================================================
# Streamlit 공식 User Authentication & Navigation Hub (app2.py)
# 인증 문서: https://docs.streamlit.io/develop/api-reference/user
# 내비게이션 문서: https://docs.streamlit.io/develop/api-reference/navigation
# 디자인 가이드: apple-design-principles.md
# ==============================================================================

# 0. .env 환경 변수 로드 및 Streamlit 공식 Secrets 동적 주입
# secrets.toml 대신 .env 파일에서 Google OIDC 인증 정보를 불러옵니다.
load_dotenv()

secrets_singleton.merge_programmatic_secrets({
    "auth": {
        "redirect_uri": os.getenv("AUTH_REDIRECT_URI", "http://localhost:8501/oauth2callback"),
        "cookie_secret": os.getenv("AUTH_COOKIE_SECRET", "0123456789abcdef0123456789abcdef"),
        "client_id": os.getenv("AUTH_CLIENT_ID", ""),
        "client_secret": os.getenv("AUTH_CLIENT_SECRET", ""),
        "server_metadata_url": os.getenv(
            "AUTH_SERVER_METADATA_URL",
            "https://accounts.google.com/.well-known/openid-configuration"
        ),
    }
})

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Streamlit AI Studio",
    page_icon="⚡",
    layout="wide"
)

# 2. Apple 디자인 시스템 CSS 전역 주입 (templates/apple_theme.css 분리 관리)
apply_custom_css()

# 3. 로그인 화면 정의 (Apple Frosted Glass 템플릿 연동)
def login_screen():
    # 화면 중앙 정렬 3열 레이아웃
    _, center_col, _ = st.columns([1, 1.8, 1])

    with center_col:
        # 분리된 HTML 템플릿(templates/login_card.html) 렌더링
        render_login_card()

        # 공식 st.login(): .streamlit/secrets.toml 설정 기반으로 Google OIDC 로그인 시작
        if st.button("Google 계정으로 로그인", icon=":material/login:", type="primary", use_container_width=True):
            st.login()

        st.caption("※ 보안을 위해 승인된 Google Workspace 계정으로만 접근할 수 있습니다.")


# 4. 페이지 정의 (st.Page)
# 참고: https://docs.streamlit.io/develop/api-reference/navigation/st.page
login_page = st.Page(login_screen, title="Log in", icon=":material/lock:")

main_page = st.Page(r"stream_pages\main.py", title="메인 대시보드", icon=":material/home:", default=True)
chat_page = st.Page(r"stream_pages\chat.py", title="AI 챗봇", icon=":material/chat:")
analytics_page = st.Page(r"stream_pages\analytics.py", title="통계 분석실", icon=":material/bar_chart:")
nav_page = st.Page(r"stream_pages\navigation.py", title="내비게이션 가이드", icon=":material/explore:")
settings_page = st.Page(r"stream_pages\settings.py", title="환경 설정", icon=":material/settings:")

# 5. 로그인 상태 확인 (st.user.is_logged_in) 및 동적 페이지 라우팅
is_logged_in = getattr(st.user, "is_logged_in", False)
if not is_logged_in:
    # [미로그인 상태]: 로그인 페이지만 렌더링 (사이드바 메뉴 숨김: position="hidden")
    pg = st.navigation([login_page], position="hidden")
else:
    # [로그인 완료 상태]: 딕셔너리를 활용한 공식 섹션 그룹화 (position="sidebar")
    pg = st.navigation({
        "서비스 (Apps)": [main_page, chat_page, analytics_page],
        "문서 & 가이드 (Guides)": [nav_page],
        "시스템 (Admin)": [settings_page]
    })

    with st.sidebar:
        # 분리된 HTML 템플릿(templates/user_profile.html) 렌더링
        render_user_profile(
            name=getattr(st.user, "name", "인증 사용자"),
            email=getattr(st.user, "email", "-")
        )

        # 공식 st.logout(): 인증 세션 파기 및 초기화
        if st.button("로그아웃", icon=":material/logout:", use_container_width=True):
            st.logout()

# 6. 애플리케이션 실행
if __name__ == "__main__":
    pg.run()

