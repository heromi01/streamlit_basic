import streamlit as st
import pandas as pd

# ========================================================
# 4. 데이터, 차트, 지도 시각화 모듈 세부 함수들
# ========================================================

def render_map():
    """인터랙티브 지도 시각화 (st.map)"""
    st.subheader("1. 인터랙티브 지도 (st.map)")
    st.caption("서울 주요 명소의 위도(`lat`)와 경도(`lon`)를 지도에 자동 핀 표시합니다.")
    landmark_df = pd.DataFrame({
        "lat": [37.5665, 37.5512, 37.5796, 37.5126],
        "lon": [126.9780, 126.9882, 126.9770, 127.1026],
        "장소": ["서울시청", "남산서울타워", "경복궁", "롯데월드타워"]
    })
    # latitude, longitude 및 height를 명시하여 탭 내부에서도 지도가 안정적으로 렌더링되도록 합니다.
    st.map(landmark_df, latitude="lat", longitude="lon", zoom=11, height=400)
    st.caption("▲ 마우스로 지도를 드래그하거나 스크롤로 확대/축소할 수 있습니다.")


def render_charts():
    """다양한 내장 그래프 차트 (Line, Area, Scatter, Bar)"""
    st.subheader("2. 인터랙티브 차트 모음 (Charts)")
    st.markdown("Streamlit 내장 차트는 복잡한 설정 없이 데이터프레임만으로 즉시 시각화합니다.")

    # (1) 꺾은선 & 누적 영역 차트
    st.markdown("#### (1) 꺾은선 & 누적 영역 차트 (`st.line_chart`, `st.area_chart`)")
    # x축과 y축을 명시적으로 전달할 수 있도록 깔끔한 열 구조로 정의합니다.
    temperature_df = pd.DataFrame({
        "요일": ["월", "화", "수", "목", "금", "토", "일"],
        "최고기온": [18, 20, 22, 19, 23, 25, 24],
        "최저기온": [7, 8, 10, 9, 11, 13, 12]
    })
    st.markdown("**- 요일별 기온 변화 (Line Chart)**")
    st.line_chart(temperature_df, x="요일", y=["최고기온", "최저기온"])

    st.markdown("**- 누적 영역 차트 (Area Chart)**")
    st.area_chart(temperature_df, x="요일", y=["최고기온", "최저기온"])

    st.divider()

    # (2) 산점도 차트
    st.markdown("#### (2) 산점도 차트 (`st.scatter_chart`)")
    st.caption("공부 시간과 시험 점수 사이의 상관관계를 점으로 표시합니다.")
    score_df = pd.DataFrame({
        "공부시간": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "시험점수": [45, 55, 62, 70, 75, 82, 88, 91, 95, 98]
    })
    st.scatter_chart(score_df, x="공부시간", y="시험점수")

    st.divider()

    # (3) 막대 차트
    st.markdown("#### (3) 막대 차트 (`st.bar_chart`)")
    # 데이터프레임 구조로 x축과 y축을 명확히 지정하여 Vega-Lite 호환성을 극대화합니다.
    bar_df = pd.DataFrame({
        "요일": ["월", "화", "수", "목", "금"],
        "방문자수": [30, 45, 60, 75, 90]
    })
    st.bar_chart(bar_df, x="요일", y="방문자수")


def render_tables_json():
    """데이터프레임, 정적 테이블 및 JSON 트리 뷰어"""
    st.subheader("3. 표 및 JSON 데이터 표시 (Data Display)")
    st.markdown("인터랙티브 표, 정적 HTML 테이블, 계층형 JSON 뷰어입니다.")

    sample_data = {
        "이름": ["김철수", "이영희", "박민수"],
        "부서": ["개발팀", "디자인팀", "마케팅팀"],
        "점수": [95, 88, 92]
    }

    # (1) 인터랙티브 데이터프레임
    st.markdown("#### (1) 인터랙티브 데이터프레임 (`st.dataframe`)")
    st.caption("헤더 클릭 시 정렬 지원 및 열 크기 조절이 가능합니다.")
    st.dataframe(sample_data)

    st.divider()

    # (2) 정적 데이터 테이블
    st.markdown("#### (2) 정적 데이터 테이블 (`st.table`)")
    st.caption("인터랙티브 기능 없이 전체 데이터가 한눈에 보이도록 고정된 순수 HTML 표입니다.")
    st.table(sample_data)

    st.divider()

    # (3) 계층형 JSON 뷰어
    st.markdown("#### (3) 계층형 JSON 뷰어 (`st.json`)")
    sample_json_data = {
        "프로젝트": "Streamlit 마스터",
        "버전": "1.64.0",
        "기능목록": ["텍스트 입력", "차트 시각화", "지도", "폼 & 챗봇"],
        "환경설정": {
            "패키지매니저": "uv",
            "파이썬버전": "3.12"
        }
    }
    st.json(sample_json_data, expanded=True)


def render_tab4():
    """전체 렌더링 호환 함수"""
    render_map()
    st.divider()
    render_charts()
    st.divider()
    render_tables_json()
