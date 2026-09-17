import streamlit as st
import chat_db
from styles import apply_custom_css

# ========================================================
# 과거 대화 히스토리 화면 모듈
# - SQLite DB(chat_history.db)에 보관된 최대 10개 세션 열람
# - 세션당 텍스트 대화 내역(최대 100턴) 조회 및 마크다운 다운로드 지원
# ========================================================

def render_history_page(chat_page=None):
    """과거 대화 히스토리 대시보드 화면 렌더링"""
    apply_custom_css()

    # 로그인 여부 검증 (미인증 사용자는 로그인 화면 렌더링 후 차단)
    if not st.session_state.get("is_logged_in", False):
        from app2 import show_login_page
        show_login_page()
        return

    # 1. 상단 타이틀 및 간결한 소개 안내
    st.title("📜 과거 대화 히스토리 및 분석 (Chat History)")
    st.markdown("SQLite 데이터베이스(`chat_history.db`)에 보관된 **최대 10개 대화 세션**의 텍스트 대화 내역을 탐색하고 내보낼 수 있는 대시보드입니다.")
    st.caption("💡 DB에는 최신 10개 세션만 유지(FIFO)되며, 각 세션당 최대 100개 대화(턴)의 텍스트 기록을 확인할 수 있습니다.")

    # 실시간 채팅 화면으로 즉시 복귀하는 버튼
    col_nav1, col_nav2 = st.columns([1, 3])
    with col_nav1:
        if st.button("💬 실시간 AI 채팅으로 돌아가기", type="primary", use_container_width=True):
            st.session_state["current_menu"] = "🤖 AI 멀티모달 챗봇"
            st.rerun()

    st.divider()

    # 2. 전체 대화 통계 요약 지표 카드 (KPI Metrics)
    db_stats = chat_db.get_db_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 최대 10개 세션 FIFO 보관 상태 표시
        st.metric(label="📁 보관 세션 수", value=f"{db_stats['total_sessions']} / 10개", help="DB에 최대 10개의 세션만 유지되며 오래된 세션부터 자동 삭제됩니다.")
    with col2:
        st.metric(label="💬 총 누적 메시지 수", value=f"{db_stats['total_messages']}개")
    with col3:
        st.metric(label="👤 사용자 질문 수", value=f"{db_stats['user_messages']}개")
    with col4:
        st.metric(label="🤖 AI 답변 수", value=f"{db_stats['assistant_messages']}개")

    st.divider()

    # 3. 사이드바: 키워드 검색, 세션 목록 및 정렬
    all_sessions = chat_db.get_all_sessions()

    with st.sidebar:
        st.header("🔍 대화 탐색 및 세션 선택")

        # 실시간 대화창 복귀 링크 (단독 실행 모드일 때만 노출)
        if not st.session_state.get("is_portal_mode", False):
            if st.button("💬 실시간 채팅창 열기", use_container_width=True):
                st.session_state["current_menu"] = "🤖 AI 멀티모달 챗봇"
                st.rerun()
            st.divider()

        # [3-A] 본문 키워드 통합 검색
        st.subheader("🔎 키워드 통합 검색")
        search_keyword = st.text_input(
            "메시지 내용 검색",
            placeholder="예: Python, 환각, 업무 자동화...",
            help="저장된 대화 본문에서 특정 키워드를 검색합니다."
        )

        matched_session_ids = set()
        if search_keyword.strip():
            search_results = chat_db.search_messages(search_keyword.strip())
            st.info(f"검색 결과: **{len(search_results)}건** 일치")
            matched_session_ids = {r["session_id"] for r in search_results}

        # [3-B] 세션 정렬 (최신순 / 과거순)
        sort_order = st.radio(
            "정렬 순서",
            options=["최신순", "과거순"],
            horizontal=True
        )

        sessions_to_display = list(all_sessions)
        if sort_order == "과거순":
            sessions_to_display.reverse()

        # 검색어가 있을 경우 일치 세션만 필터링
        if search_keyword.strip() and matched_session_ids:
            if st.checkbox("일치 세션만 보기", value=True):
                sessions_to_display = [s for s in sessions_to_display if s["id"] in matched_session_ids]

        st.subheader("📋 세션 목록 (최대 10개)")

        if not sessions_to_display:
            st.warning("표시할 세션이 없습니다.")
            selected_session_id = None
        else:
            session_dict = {
                s["id"]: f"[{s['created_at'][:10]}] {s['title']}"
                for s in sessions_to_display
            }

            # 확인할 세션 선택
            selected_session_id = st.selectbox(
                "세션 선택",
                options=list(session_dict.keys()),
                format_func=lambda sid: session_dict.get(sid, sid),
                help="조회할 대화 세션을 선택하세요."
            )

            st.divider()

            # [3-C] 선택된 세션 관리 (다운로드 및 삭제)
            st.subheader("⚙️ 세션 관리")
            md_content = chat_db.export_session_markdown(selected_session_id)
            st.download_button(
                label="📥 대화 내역 다운로드 (.md)",
                data=md_content.encode("utf-8"),
                file_name=f"chat_{selected_session_id[:8]}.md",
                mime="text/markdown",
                use_container_width=True,
                help="선택한 세션의 텍스트 대화 내용을 마크다운 파일로 다운로드합니다."
            )

            if st.button("🗑️ 선택한 세션 삭제", use_container_width=True):
                chat_db.delete_session(selected_session_id)
                st.success("세션이 삭제되었습니다.")
                st.rerun()

    # 4. 우측 본문: 선택된 세션 대화 상세 내용 렌더링 (순수 텍스트)
    if not all_sessions:
        st.info("💡 아직 저장된 대화 내역이 없습니다. 실시간 채팅에서 새로운 대화를 시작해보세요!")
    elif not selected_session_id:
        st.warning("일치하는 세션이 없습니다. 다른 검색어를 입력해보세요.")
    else:
        selected_session = next((s for s in all_sessions if s["id"] == selected_session_id), None)
        session_title = selected_session["title"] if selected_session else "대화"
        session_created_at = selected_session["created_at"] if selected_session else "-"
        messages = chat_db.get_session_messages(selected_session_id)
        turn_count = len([m for m in messages if m["role"] == "user"])

        # 세션 정보 카드 (컨테이너 테두리)
        with st.container(border=True):
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.subheader(f"📌 {session_title}")
                st.caption(f"세션 ID: `{selected_session_id}` | 생성 일시: {session_created_at}")
                st.caption(f"대화 진행도: **{turn_count} / 100턴** (총 메시지 {len(messages)}개)")
            with col_btn:
                st.download_button(
                    label="📥 Markdown 저장",
                    data=chat_db.export_session_markdown(selected_session_id).encode("utf-8"),
                    file_name=f"chat_{selected_session_id[:8]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="main_export_btn"
                )

        st.write("")

        # 각 텍스트 메시지 순차적 렌더링
        for msg in messages:
            with st.chat_message(msg["role"]):
                role_name = "👤 사용자" if msg["role"] == "user" else "🤖 AI 어시스턴트"
                st.caption(f"{role_name} • {msg['created_at']}")
                st.markdown(msg["content"])

# app2.py와의 호환을 위한 별칭
show_history_page = render_history_page

# app2_history.py 단독 실행 지원
if __name__ == "__main__":
    st.set_page_config(
        page_title="OpenAI 챗봇 과거 대화 히스토리",
        page_icon="📜",
        layout="wide"
    )
    render_history_page()
