import streamlit as st

# ========================================================
# 데이터 및 시각화 세부 모듈 함수 임포트
# ========================================================
from tabs.tab4_charts_map import (
    render_map,
    render_charts,
    render_tables_json
)

def render_visualizations_group():
    """데이터 & 시각화 그룹의 하위 세부 기능 탭들을 생성하고 렌더링"""
    st.info("📊 **[데이터 & 시각화 그룹]** 지도 시각화, 각종 그래프 차트, 그리고 표/JSON 데이터 표시를 하위 탭별로 탐구합니다.")

    # 하위 서브 탭 3개 생성
    sub_vis1, sub_vis2, sub_vis3 = st.tabs([
        "🗺️ 인터랙티브 지도 (Map)",
        "📈 그래프 차트 (Charts)",
        "📋 데이터 표 & JSON (Tables & JSON)"
    ])

    with sub_vis1:
        render_map()

    with sub_vis2:
        render_charts()

    with sub_vis3:
        render_tables_json()

