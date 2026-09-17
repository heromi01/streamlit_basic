import streamlit as st
import datetime

# ========================================================
# 3. 숫자, 날짜, 시간, 슬라이더 위젯 모듈
# ========================================================
def render_tab3():
    """숫자, 날짜 단일/범위, 시간, 슬라이더 관련 위젯 모음"""
    st.subheader("3. 수치 및 일시 입력 위젯 (Numbers & DateTime)")
    st.markdown("숫자 증감 입력, 단일/기간 날짜 선택, 시간 설정, 슬라이더 조작 위젯들입니다.")

    # (1) 숫자 입력
    st.markdown("#### (1) 숫자 입력 (`st.number_input`)")
    st.caption("정수 또는 실수를 입력받으며, `min_value`, `max_value`, `step`으로 범위를 한정합니다.")
    # min_value: 최솟값, max_value: 최댓값, value: 시작값, step: 단위
    user_age = st.number_input("나이를 입력하세요", min_value=1, max_value=120, value=25, step=1, key="tab3_num_age")
    st.write(f"입력된 나이: **{user_age}세**")

    st.divider()

    # (2) 단일 날짜 입력
    st.markdown("#### (2) 단일 날짜 선택 (`st.date_input`)")
    st.caption("달력 팝업을 열어 특정 하루를 선택합니다.")
    # format: 화면에 보일 날짜 표기 형식
    selected_date = st.date_input("희망 시작 날짜를 선택하세요", format="YYYY/MM/DD", key="tab3_date_single")
    st.write(f"선택한 날짜: **{selected_date}**")

    st.divider()

    # (3) 날짜 기간 범위 선택
    st.markdown("#### (3) 날짜 기간 범위 선택 (Date Range)")
    st.caption("`value`에 `(시작일, 종료일)` 튜플을 전달하여 기간 범위를 한 번에 선택합니다.")
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    # value=(시작일, 종료일): 기간 범위 선택 활성화
    date_range = st.date_input(
        "휴가 일정을 선택하세요 (시작일 ~ 종료일)",
        value=(today, next_week),
        format="YYYY/MM/DD",
        key="tab3_date_range"
    )
    st.write("선택된 일정 범위:", date_range)

    st.divider()

    # (4) 시간 입력
    st.markdown("#### (4) 시간 입력 (`st.time_input`)")
    st.caption("시/분 단위로 시간을 선택하며 `step`으로 분 간격을 조절합니다.")
    # value: 기본 시간, step: 분 단위 증감 간격
    meeting_time = st.time_input(
        "미팅 시작 시간을 선택하세요",
        value=datetime.time(9, 30),
        step=datetime.timedelta(minutes=15),
        key="tab3_time_meeting"
    )
    st.write(f"설정된 미팅 시간: **{meeting_time}**")

    st.divider()

    # (5) 기본 수치 슬라이더
    st.markdown("#### (5) 기본 수치 슬라이더 (`st.slider`)")
    st.caption("마우스로 드래그하여 수치를 조절합니다.")
    # min_value: 최솟값, max_value: 최댓값, step: 눈금 간격
    satisfaction_score = st.slider(
        "오늘의 학습 만족도 점수",
        min_value=0,
        max_value=100,
        value=85,
        step=5,
        key="tab3_slider_score"
    )
    st.write(f"만족도 점수: **{satisfaction_score}점**")

    st.divider()

    # (6) 양방향 범위 슬라이더 및 카테고리 슬라이더
    st.markdown("#### (6) 양방향 범위 슬라이더 & 카테고리 슬라이더")
    st.caption("두 개의 핸들로 범위를 정하거나, 텍스트 등급 단계를 슬라이딩합니다.")
    # value=(최소, 최대): 2개의 핸들로 범위를 지정
    price_range = st.slider(
        "예산 범위를 설정하세요 (단위: 만원)",
        min_value=0,
        max_value=200,
        value=(30, 120),
        key="tab3_slider_price"
    )
    st.write(f"설정된 예산 범위: **{price_range[0]}만원 ~ {price_range[1]}만원**")

    # st.select_slider: 단계별 텍스트 선택 슬라이더
    service_grade = st.select_slider(
        "서비스 품질 등급 평가",
        options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
        value="보통",
        key="tab3_select_slider_grade"
    )
    st.write(f"평가 등급: **{service_grade}**")

