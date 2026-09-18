import streamlit as st

# ==============================================================================
# Streamlit 공식 Navigation & Pages API 시연 페이지 (navigation.py)
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation
# ==============================================================================

# ==============================================================================
# 1. 로그인 인증 가드 (Auth Guard)
# ==============================================================================
if not st.user.is_logged_in:
    st.warning("🔒 로그인이 필요한 서비스입니다. 먼저 로그인해 주세요.")
    st.stop()

# 2. 페이지 헤더 및 소개
st.title("🧭 Navigation & Pages API")
st.caption("공식 API 참조: [https://docs.streamlit.io/develop/api-reference/navigation](https://docs.streamlit.io/develop/api-reference/navigation)")

st.markdown(
    """
    Streamlit 1.36+부터 도입된 **Navigation API**는 멀티페이지 애플리케이션의 
    페이지 등록, 섹션 분류, 권한 기반 동적 라우팅, 코드 기반 페이지 전환(`st.switch_page`)을 완벽하게 제어합니다.
    """
)

st.divider()

# 2. 3대 핵심 API 상세 설명 및 코드 예시
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. `st.Page` (페이지 객체 정의)")
    st.markdown("스크립트 파일 경로 또는 파이썬 함수를 개별 페이지로 선언합니다.")
    st.code(
        """# 파일 경로 지정 방식
p1 = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)

# 파이썬 함수 지정 방식
def my_page():
    st.write("Hello World")

p2 = st.Page(my_page, title="Custom", icon=":material/settings:")
""",
        language="python"
    )
    st.caption("※ `title`, `icon`, `url_path`, `default` 등의 파라미터를 설정할 수 있습니다.")

with col2:
    st.subheader("2. `st.navigation` (라우터 설정)")
    st.markdown("정의된 페이지들을 묶어 앱의 메뉴와 실행 흐름을 구성합니다.")
    st.code(
        """# 1) 단순 리스트 구성
pg = st.navigation([p1, p2])

# 2) 딕셔너리를 활용한 섹션 그룹화 (권장)
pg = st.navigation({
    "메인": [p1],
    "설정": [p2]
}, position="sidebar")

pg.run()
""",
        language="python"
    )
    st.caption("※ `position='hidden'`을 주면 사이드바 메뉴를 숨기고 전체 화면으로 표시할 수 있습니다.")

st.divider()

# 3. st.switch_page 실시간 인터랙션 데모
st.subheader("3. `st.switch_page` (프로그래밍 방식 페이지 전환)")
st.markdown(
    """
    사용자가 사이드바 메뉴를 직접 클릭하지 않아도, 버튼 클릭이나 특정 조건 달성 시 
    파이썬 코드(`st.switch_page`)를 통해 다른 페이지로 즉시 이동할 수 있습니다.
    """
)

# st.switch_page() 동작 버튼
if st.button("🏠 메인 대시보드로 이동하기 (st.switch_page)", icon=":material/arrow_forward:", type="primary"):
    # stream_pages/main.py 페이지로 즉시 전환
    st.switch_page("stream_pages/main.py")

st.caption("※ 위 버튼을 누르면 `st.switch_page('stream_pages/main.py')`가 실행되어 즉시 메인 페이지로 이동합니다.")

