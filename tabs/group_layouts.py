import streamlit as st

# ========================================================
# 레이아웃 세부 모듈 함수 임포트
# ========================================================
from tabs.tab5_layout import (
    render_layout_columns,
    render_layout_containers,
    render_layout_dialog_popover,
    render_layout_dynamic_space,
    render_layout_expander_tabs,
)

def render_layouts_group():
    """레이아웃 & 컨테이너 그룹의 하위 세부 기능 탭들을 생성하고 렌더링"""
    st.info("📐 **[레이아웃 & 컨테이너 그룹]** 공식 문서에 명시된 10가지 전체 레이아웃 요소를 하위 탭별로 분리하여 실습합니다.")

    # 하위 서브 탭 5개 생성
    sub_layout1, sub_layout2, sub_layout3, sub_layout4, sub_layout5 = st.tabs([
        "🏛️ 다단 컬럼 (Columns)",
        "📦 컨테이너 & 하단 고정 (Container & Bottom)",
        "💬 모달 & 팝오버 (Dialog & Popover)",
        "⏳ 동적 교체 & 여백 (Empty & Space)",
        "📂 접이식 & 사이드바 (Expander & Sidebar)"
    ])

    with sub_layout1:
        render_layout_columns()

    with sub_layout2:
        render_layout_containers()

    with sub_layout3:
        render_layout_dialog_popover()

    with sub_layout4:
        render_layout_dynamic_space()

    with sub_layout5:
        render_layout_expander_tabs()

