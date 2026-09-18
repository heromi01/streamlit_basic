import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 데이터 시각화 및 통계 분석실 (analytics.py)
# 공식 Chart Elements: https://docs.streamlit.io/develop/api-reference/charts
# ==============================================================================

# ==============================================================================
# 1. 로그인 인증 가드 (Auth Guard)
# ==============================================================================
if not st.user.is_logged_in:
    st.warning("🔒 로그인이 필요한 서비스입니다. 먼저 로그인해 주세요.")
    st.stop()

# 2. 페이지 헤더
st.title("📊 데이터 통계 & 시각화 분석실")
st.caption("Streamlit 기본 KPI 메트릭 및 반응형 차트 컴포넌트 시연")

st.markdown(
    """
    이 페이지는 다양한 시각화 요소를 통해 서비스 지표를 한눈에 파악할 수 있는 대시보드 화면입니다.
    상단의 KPI 카드와 하단의 트렌드 차트를 확인해 보세요.
    """
)

st.divider()

# 2. 핵심 KPI 지표 카드 (st.metric)
col1, col2, col3 = st.columns(3)

with col1:
    # st.metric(label, value, delta): 핵심 수치와 증감 추이를 시각적으로 표현
    st.metric(
        label="월간 활성 사용자 (MAU)",
        value="12,840명",
        delta="+14.2% (전월 대비)",
        help="이번 달 최소 1회 이상 로그인한 순수 사용자 수입니다."
    )

with col2:
    st.metric(
        label="평균 체류 시간",
        value="8분 42초",
        delta="+1분 15초",
        help="사용자당 세션 평균 유지 시간입니다."
    )

with col3:
    st.metric(
        label="API 응답 속도",
        value="98.4ms",
        delta="-12.3ms (개선)",
        help="평균 API 레이턴시 측정치입니다."
    )

st.divider()

# 3. 샘플 시계열 데이터 생성
# 7일간의 일별 방문자 및 활동 트렌드 데이터프레임
dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
sample_df = pd.DataFrame({
    "방문자 수": [1200, 1450, 1380, 1620, 1890, 2100, 2350],
    "대화 생성 수": [3200, 3900, 3600, 4200, 5100, 5800, 6400]
}, index=dates)

# 4. 차트 레이아웃 2열 배치
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 일별 방문자 추이 (Line Chart)")
    st.caption("`st.line_chart`를 활용한 시계열 꺾은선 그래프")
    st.line_chart(sample_df["방문자 수"], color="#0071e3")

with chart_col2:
    st.subheader("📊 일별 대화 생성량 (Bar Chart)")
    st.caption("`st.bar_chart`를 활용한 막대 그래프")
    st.bar_chart(sample_df["대화 생성 수"], color="#34c759")

st.divider()

# 5. 원본 데이터프레임 뷰어 (st.dataframe)
st.subheader("📋 주간 집계 원본 데이터")
st.dataframe(sample_df)
