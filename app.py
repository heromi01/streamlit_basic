import streamlit as st

# ========================================================
# 탭 그룹별 렌더링 함수 임포트
# ========================================================
from tabs.sidebar import render_sidebar
from tabs.group_inputs import render_inputs_group
from tabs.group_layouts import render_layouts_group
from tabs.group_visualizations import render_visualizations_group
from tabs.group_status_media import render_status_media_group

# ========================================================
# 앱 기본 설정 및 타이틀
# ========================================================
st.title("Streamlit 핵심 기능 & 위젯 마스터 가이드")
st.markdown("상위 탭 그룹을 선택하면, 각 그룹 하위에 기능별 **세부 서브 탭**이 나타나는 2단계 계층형 구조로 구성되었습니다.")
st.divider()

# ========================================================
# 1. 좌측 사이드바 패널 렌더링
# ========================================================
render_sidebar()

# ========================================================
# 2. 상위 탭 그룹 생성 (입력 위젯 / 레이아웃 / 데이터 / 상태 & 미디어)
# ========================================================
tab_group_inputs, tab_group_layouts, tab_group_charts, tab_group_status = st.tabs([
    "🎛️ 입력 위젯 그룹 (Input Widgets)",
    "📐 레이아웃 & 컨테이너 그룹 (Layouts & Containers)",
    "📊 데이터 & 시각화 그룹 (Data & Charts)",
    "🎨 상태 알림 & 미디어 그룹 (Status & Media)"
])

# 3. 각 상위 탭 내부에서 해당 하위 서브 탭 그룹 실행
with tab_group_inputs:
    render_inputs_group()

with tab_group_layouts:
    render_layouts_group()

with tab_group_charts:
    render_visualizations_group()

with tab_group_status:
    render_status_media_group()
