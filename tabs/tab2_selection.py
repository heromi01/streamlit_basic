import streamlit as st

# ========================================================
# 2. 선택 및 옵션 위젯 모듈
# ========================================================
def render_tab2():
    """라디오 버튼, 선택 박스, 멀티셀렉트, 필스 등 선택형 위젯 모음"""
    st.subheader("2. 선택 및 옵션 위젯 (Selection Widgets)")
    st.markdown("단일 선택, 다중 선택, 토글 스위치, 칩 버튼 등 다양한 형태의 선택형 컴포넌트입니다.")

    # (1) 라디오 버튼 가로 배치
    st.markdown("#### (1) 라디오 버튼 가로 배치 (`st.radio`)")
    st.caption("`horizontal=True` 옵션을 통해 선택지들을 가로로 나란히 나열합니다.")
    # options: 선택 목록, horizontal=True: 가로 정렬
    selected_color = st.radio(
        "좋아하는 테마 색상을 선택하세요",
        options=["빨강", "파랑", "초록", "보라"],
        horizontal=True,
        key="tab2_radio_color"
    )
    st.write(f"선택한 색상: **{selected_color}**")

    st.divider()

    # (2) 라디오 버튼 심화 (captions, index=None)
    st.markdown("#### (2) 라디오 버튼 심화 (설명 캡션 & 초기 미선택)")
    st.caption("각 항목 아래에 `captions`를 달고, `index=None`으로 빈 상태에서 시작합니다.")
    # captions: 부가 설명 문구 리스트, index=None: 기본 선택 없음
    delivery_option = st.radio(
        "배송 방법을 선택해주세요",
        options=["새벽 배송", "일반 택배", "방문 수령"],
        captions=["내일 아침 7시 전 도착 보장", "2~3일 소요 (기본 배송)", "매장에 직접 방문하여 픽업"],
        index=None,
        key="tab2_radio_delivery"
    )
    st.write(f"선택하신 배송 방식: **{delivery_option}**")

    st.divider()

    # (3) 기본 드롭다운 선택 상자
    st.markdown("#### (3) 기본 드롭다운 선택 상자 (`st.selectbox`)")
    st.caption("여러 목록 중 하나를 드롭다운 리스트 형태로 펼쳐서 선택합니다.")
    # index: 기본 선택될 항목 번호 (0: 첫 번째)
    selected_job = st.selectbox(
        "직업을 선택하세요",
        options=["개발자", "디자이너", "데이터 분석가", "기획자", "학생"],
        index=0,
        key="tab2_select_job"
    )
    st.write(f"선택한 직업: **{selected_job}**")

    st.divider()

    # (4) 선택 박스 심화 (placeholder, index=None)
    st.markdown("#### (4) 선택 박스 심화 (안내 문구 & 초기 미선택)")
    st.caption("`index=None`과 `placeholder`를 활용하여 드롭다운 선택 전 힌트를 띄웁니다.")
    # placeholder: 선택 전 안내 문구
    selected_city = st.selectbox(
        "여행하고 싶은 도시를 선택하세요",
        options=["서울", "부산", "제주도", "강릉", "경주"],
        index=None,
        placeholder="목록에서 도시를 선택해 주세요...",
        key="tab2_select_city"
    )
    st.write(f"선택된 여행지: **{selected_city}**")

    st.divider()

    # (5) 다중 선택 위젯
    st.markdown("#### (5) 다중 선택 (`st.multiselect`)")
    st.caption("목록에서 원하는 항목을 여러 개 복수로 골라낼 수 있습니다.")
    # default: 처음부터 선택되어 있을 기본 항목 리스트
    selected_skills = st.multiselect(
        "관심 있는 기술 스택을 모두 선택하세요",
        options=["Python", "Streamlit", "Pandas", "SQL", "Machine Learning"],
        default=["Python", "Streamlit"],
        key="tab2_multiselect_skills"
    )
    st.write("선택된 기술 스택:", selected_skills)

    st.divider()

    # (6) 최신 필스 & 세그먼트 컨트롤
    st.markdown("#### (6) 모던 UI 필스(Pills) & 세그먼트 컨트롤")
    st.caption("알약 모양의 칩 버튼(`st.pills`)과 분할 세그먼트 버튼(`st.segmented_control`)입니다.")
    # st.pills: 칩 형태 버튼 선택기
    coffee_type = st.pills(
        "커피 종류를 선택하세요",
        options=["아메리카노", "카페라떼", "바닐라라떼", "콜드브루"],
        default="아메리카노",
        key="tab2_pills_coffee"
    )
    st.write(f"선택한 음료: **{coffee_type}**")

    # st.segmented_control: 분할 세그먼트 선택기
    device_type = st.segmented_control(
        "주 사용 기기",
        options=["스마트폰", "태블릿", "노트북", "데스크톱"],
        default="노트북",
        key="tab2_segment_device"
    )
    st.write(f"선택한 기기: **{device_type}**")

    st.divider()

    # (7) 체크박스 & 토글 스위치
    st.markdown("#### (7) 체크박스 & 토글 스위치 (`st.checkbox`, `st.toggle`)")
    st.caption("참/거짓(True/False) 불리언 상태를 설정합니다.")
    # value: 초기 체크 여부
    agree_terms = st.checkbox("개인정보 처리방침에 동의합니다", value=False, key="tab2_check_agree")
    st.write(f"동의 여부: **{agree_terms}**")

    # st.toggle: 스위치 형태 토글
    show_details = st.toggle("상세 정보 표시하기", value=False, key="tab2_toggle_details")
    if show_details:
        st.info("토글 스위치가 켜졌을 때만 나타나는 상세 안내 문구입니다!")

