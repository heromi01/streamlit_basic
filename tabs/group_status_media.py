import streamlit as st

# ========================================================
# 상태 알림 & 미디어 세부 모듈 함수 임포트
# ========================================================
from tabs.tab6_status_media import (
    render_status_alerts_metrics,
    render_animations_progress,
    render_feedback_media
)

def render_status_media_group():
    """상태 알림 & 미디어 그룹의 하위 세부 기능 탭들을 생성하고 렌더링"""
    st.info("🎨 **[상태 알림 & 미디어 그룹]** 핵심 KPI 지표, 4색 알림 박스, 축하 애니메이션, 평점 피드백, 미디어를 하위 탭별로 탐구합니다.")

    # 하위 서브 탭 3개 생성
    sub_stat1, sub_stat2, sub_stat3 = st.tabs([
        "🚨 핵심 KPI & 알림 박스 (Metrics & Alerts)",
        "🎉 애니메이션 & 진행률 (Animation & Progress)",
        "🖼️ 평점 피드백 & 미디어 (Feedback & Media)"
    ])

    with sub_stat1:
        render_status_alerts_metrics()

    with sub_stat2:
        render_animations_progress()

    with sub_stat3:
        render_feedback_media()

