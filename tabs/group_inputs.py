import streamlit as st

# ========================================================
# 입력 위젯 세부 모듈 임포트
# ========================================================
from tabs.tab1_text_code import render_tab1
from tabs.tab2_selection import render_tab2
from tabs.tab3_numeric_datetime import render_tab3
from tabs.tab7_form_chat import render_tab7

def render_inputs_group():
    """입력 위젯 그룹의 하위 세부 기능 탭들을 생성하고 렌더링"""
    st.info("💡 **[입력 위젯 그룹]** 아래 하위 탭을 선택하여 텍스트, 선택, 수치/일시, 폼/챗봇 위젯을 탐구하세요.")

    # 하위 서브 탭 4개 생성
    sub1, sub2, sub3, sub4 = st.tabs([
        "📝 텍스트 & 코드 (Text & Code)",
        "🎯 선택 & 옵션 (Selection Widgets)",
        "🔢 수치 & 일시 (Numbers & DateTime)",
        "🤖 폼 & 챗봇 (Form & Chat UI)"
    ])

    with sub1:
        render_tab1()

    with sub2:
        render_tab2()

    with sub3:
        render_tab3()

    with sub4:
        render_tab7()

