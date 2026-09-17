import streamlit as st
import time

# ========================================================
# 모달 다이얼로그 함수 선언 (@st.dialog)
# ========================================================
@st.dialog("📋 회원 상세 정보 입력 모달")
def show_user_modal():
    """버튼 클릭 시 화면 중앙에 나타나는 독립된 모달 팝업 대화상자"""
    st.write("이 창은 `@st.dialog` 데코레이터로 생성된 모달 팝업입니다.")
    user_modal_name = st.text_input("모달 내부 이름 입력", value="홍길동", key="modal_name")
    user_modal_dept = st.selectbox("소속 부서", ["인사팀", "개발팀", "마케팅팀"], key="modal_dept")

    if st.button("확인 및 닫기", type="primary", key="modal_submit_btn"):
        st.success(f"저장되었습니다: {user_modal_name} ({user_modal_dept})")
        st.rerun()


# ========================================================
# 세부 기능별 렌더링 함수들
# ========================================================

def render_layout_columns():
    """1. 다단 컬럼 분할 (st.columns)"""
    st.subheader("1. 다단 컬럼 분할 (st.columns)")
    st.markdown("화면을 여러 열(Column)로 나누며, 비율 지정, 테두리(`border=True`), 간격(`gap`), 수직 정렬을 지원합니다.")

    # [1-A] 비율 지정 및 테두리가 있는 컬럼
    st.markdown("**비율 지정 컬럼 ([1, 2] 비율) & 테두리 적용**")
    col_ratio1, col_ratio2 = st.columns([1, 2], gap="medium", border=True)
    with col_ratio1:
        st.markdown("**1의 비율 (좁은 열)**")
        st.write("왼쪽 영역입니다.")
    with col_ratio2:
        st.markdown("**2의 비율 (넓은 열)**")
        st.write("오른쪽 영역으로 2배 넓게 차지합니다.")

    st.divider()

    # [1-B] 수직 중앙 정렬 컬럼
    st.markdown("**수직 중앙 정렬 컬럼 (`vertical_alignment='center'`)**")
    col_v1, col_v2 = st.columns(2, vertical_alignment="center")
    col_v1.markdown("높이가 높은 긴 설명 문장입니다.<br>이 컬럼의 내용이 길어져도 오른쪽 컴포넌트는 수직 중앙에 맞춰집니다.", unsafe_allow_html=True)
    col_v2.button("수직 중앙 정렬 버튼", key="btn_col_v")


def render_layout_containers():
    """2. 컨테이너 & 하단 고정 바 (st.container, st.bottom)"""
    st.subheader("2. 컨테이너 & 하단 고정 바 (st.container & st.bottom)")
    st.markdown("독립된 카드 블록, 스크롤 가능한 고정 높이 상자, 그리고 브라우저 화면 최하단 고정 바입니다.")

    # [2-A] 카드 스타일 테두리 컨테이너
    st.markdown("**테두리 카드 컨테이너 (`border=True`)**")
    with st.container(border=True):
        st.markdown("📦 **카드 컨테이너 내부 영역**")
        st.write("독립된 카드 형태로 컴포넌트들을 묶어 강조할 때 사용합니다.")

    st.divider()

    # [2-B] 스크롤 가능한 고정 높이 컨테이너
    st.markdown("**스크롤 가능한 고정 높이 컨테이너 (`height=120`)**")
    with st.container(height=120, border=True):
        st.write("1번째 줄: 고정 높이 컨테이너입니다.")
        st.write("2번째 줄: 내용이 넘치면 스크롤바가 생깁니다.")
        st.write("3번째 줄: 긴 로그나 약관 내용을 담을 때 좋습니다.")
        st.write("4번째 줄: 스크롤을 내려서 확인할 수 있습니다.")
        st.write("5번째 줄: 마지막 문장입니다.")

    st.divider()

    # [2-C] st.bottom 하단 고정 영역
    st.markdown("**화면 최하단 고정 영역 (`st.bottom`)**")
    st.info("이 기능은 브라우저 창의 최하단에 항상 고정되는 바입니다. 아래 버튼을 눌러보세요.")
    with st.bottom:
        st.caption("📌 **[st.bottom 영역]** 이 문구는 화면 스크롤과 무관하게 브라우저 창 가장 아래쪽에 항상 고정됩니다.")


def render_layout_dialog_popover():
    """3. 모달 대화상자 & 팝오버 (@st.dialog, st.popover)"""
    st.subheader("3. 모달 대화상자 & 팝오버 (@st.dialog & st.popover)")
    st.markdown("화면 중앙에 뜨는 모달 팝업 창과 버튼 클릭 시 열리는 플로팅 오버레이 창입니다.")

    # [3-A] st.dialog 모달 대화상자
    st.markdown("**모달 대화상자 (`@st.dialog`)**")
    st.caption("버튼을 클릭하면 브라우저 화면 중앙에 반투명 오버레이와 함께 모달 팝업창이 열립니다.")
    if st.button("🚀 모달 대화상자 열기", key="btn_open_dialog"):
        show_user_modal()

    st.divider()

    # [3-B] st.popover 팝오버 플라이아웃 창
    st.markdown("**팝오버 플라이아웃 창 (`st.popover`)**")
    st.caption("버튼을 클릭하면 해당 위치 바로 아래에 플로팅 팝업창이 떠서 부가 설정이나 필터를 보여줍니다.")
    with st.popover("⚙️ 간편 환경설정 팝오버 열기"):
        st.markdown("**알림 수신 설정**")
        email_flag = st.checkbox("이메일 알림 받기", value=True, key="layout_popover_email")
        volume_level = st.slider("알림 음량", min_value=0, max_value=100, value=80, key="layout_popover_vol")
        st.write(f"설정 요약: 이메일({email_flag}), 음량({volume_level}%)")


def render_layout_dynamic_space():
    """4. 동적 교체 & 여백 조절 (st.empty, st.space)"""
    st.subheader("4. 동적 교체 & 여백 조절 (st.empty & st.space)")
    st.markdown("단일 요소 자리를 잡고 실시간으로 덮어쓰는 플레이스홀더와 컴포넌트 간 여백 조절입니다.")

    # [4-A] st.empty 단일 요소 동적 교체
    st.markdown("**단일 요소 동적 교체 플레이스홀더 (`st.empty`)**")
    st.caption("하나의 자리(Placeholder)를 미리 잡고, 내용을 실시간으로 덮어쓰거나 지울 수 있습니다.")
    countdown_box = st.empty()
    countdown_box.info("아래 버튼을 누르면 이 안내 박스가 실시간 카운트다운으로 바뀝니다.")

    if st.button("카운트다운 시작 (st.empty 테스트)", key="btn_empty_start"):
        for i in range(3, 0, -1):
            countdown_box.warning(f"⏳ {i}초 남았습니다...")
            time.sleep(0.5)
        countdown_box.success("🎉 카운트다운 완료! 내용이 성공적으로 교체되었습니다.")

    st.divider()

    # [4-B] st.space 여백 공간 조절
    st.markdown("**위젯 간 여백 공간 조절 (`st.space`)**")
    st.caption("`st.space('small' | 'medium' | 'large')`를 사용하여 컴포넌트 사이에 시각적 간격을 조절합니다.")
    st.write("위쪽 문장입니다.")
    st.space("large")
    st.write("▲ `st.space('large')`로 위아래 넓은 간격이 적용된 아래쪽 문장입니다.")


def render_layout_expander_tabs():
    """5. 접이식 상자 & 사이드바 & 탭 (st.expander, st.sidebar, st.tabs)"""
    st.subheader("5. 접이식 상자, 사이드바 & 서브탭 (st.expander & st.sidebar)")
    st.markdown("공간을 절약하는 아코디언 메뉴와 좌측 사이드바, 중첩 서브 탭입니다.")

    # [5-A] st.expander 접이식 상자
    st.markdown("**접이식 상자 (`st.expander`)**")
    with st.expander("자주 묻는 질문 (FAQ) 열어보기", expanded=False, icon="📌"):
        st.markdown("- **Q: st.expander 안에 다른 위젯도 넣을 수 있나요?**")
        st.markdown("  - A: 네, 텍스트, 버튼, 차트 등 모든 위젯을 내부에 배치할 수 있습니다!")
        st.button("접이식 상자 내부 버튼", key="btn_inside_expander")

    st.divider()

    # [5-B] st.sidebar 좌측 사이드바 안내
    st.markdown("**사이드바 레이아웃 (`st.sidebar`)**")
    st.info("현재 화면 왼쪽의 사이드바가 `st.sidebar`로 구성되어 있습니다. 메뉴, 전역 필터, 브랜딩에 최적입니다.")

    st.divider()

    # [5-C] 중첩 서브 탭 예시
    st.markdown("**영역 내부 서브 탭 분할 (`st.tabs`)**")
    sub_tab1, sub_tab2 = st.tabs(["📌 서브 탭 1 (요약)", "📊 서브 탭 2 (세부정보)"])
    with sub_tab1:
        st.write("첫 번째 서브 탭의 요약 내용입니다.")
    with sub_tab2:
        st.write("두 번째 서브 탭의 상세 데이터입니다.")
