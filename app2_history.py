import streamlit as st
import base64
import chat_db

# ========================================================
# 과거 대화 히스토리 화면 표시 함수
# ========================================================
def show_history_page():
    """과거 대화 내역 조회 및 분석 화면"""
    
    # 1. 상단 타이틀 및 화면 전환 버튼
    st.title("📜 과거 대화 히스토리 및 분석")
    st.markdown("SQLite 데이터베이스(`chat_history.db`)에 저장된 모든 대화 세션과 주고받은 메시지를 확인합니다.")
    st.caption("💡 텍스트 메시지뿐만 아니라 당시 첨부했던 이미지와 문서 파일 내역도 온전히 복원됩니다.")

    # 실시간 채팅 화면으로 이동하는 버튼
    if st.button("🤖 실시간 AI 채팅창으로 이동", type="primary", icon="💬"):
        st.session_state["current_menu"] = "💬 실시간 AI 채팅"
        st.rerun()

    st.divider()

    # 2. 대화 통계 요약 지표 (KPI Metrics)
    stats = chat_db.get_db_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📁 총 세션 수", value=f"{stats['total_sessions']}개")
    with col2:
        st.metric(label="💬 총 메시지 수", value=f"{stats['total_messages']}개")
    with col3:
        st.metric(label="👤 사용자 질문", value=f"{stats['user_messages']}개")
    with col4:
        st.metric(label="🤖 AI 답변", value=f"{stats['assistant_messages']}개")

    st.divider()

    # 3. 사이드바: 키워드 검색, 세션 정렬 및 선택
    all_sessions = chat_db.get_all_sessions()

    with st.sidebar:
        st.subheader("🔍 대화 검색 및 세션 선택")

        # 실시간 채팅 바로가기 버튼
        if st.button("🤖 실시간 채팅창 열기", use_container_width=True):
            st.session_state["current_menu"] = "💬 실시간 AI 채팅"
            st.rerun()

        st.markdown("---")

        # 키워드 검색 입력창
        search_keyword = st.text_input(
            "대화 내용 검색",
            placeholder="예: Python, 분석...",
            help="메시지 본문에 포함된 키워드를 실시간으로 검색합니다."
        )

        matched_session_ids = set()
        if search_keyword.strip():
            search_results = chat_db.search_messages(search_keyword.strip())
            st.info(f"검색 결과: **{len(search_results)}건** 일치")
            matched_session_ids = {r["session_id"] for r in search_results}

        # 정렬 순서 라디오 버튼 (최신순 / 과거순)
        sort_order = st.radio(
            "세션 정렬",
            ["최신순", "과거순"],
            horizontal=True
        )

        sessions_to_display = list(all_sessions)
        if sort_order == "과거순":
            sessions_to_display.reverse()

        # 검색 결과 필터링 체크박스
        if search_keyword.strip() and matched_session_ids:
            if st.checkbox("일치하는 세션만 표시", value=True):
                sessions_to_display = [s for s in sessions_to_display if s["id"] in matched_session_ids]

        st.subheader("📋 대화 세션 목록")

        if not sessions_to_display:
            st.warning("표시할 대화 세션이 없습니다.")
            selected_session_id = None
        else:
            session_dict = {
                s["id"]: f"[{s['created_at'][:10]}] {s['title']}"
                for s in sessions_to_display
            }

            # 확인할 세션 선택 셀렉트박스
            selected_session_id = st.selectbox(
                "확인할 세션 선택",
                options=list(session_dict.keys()),
                format_func=lambda sid: session_dict.get(sid, sid)
            )

            st.markdown("---")

            # 선택 세션 관리 (다운로드 및 삭제)
            st.subheader("⚙️ 세션 관리")
            md_text = chat_db.export_session_markdown(selected_session_id)
            st.download_button(
                label="📥 대화 내역 다운로드 (.md)",
                data=md_text.encode("utf-8"),
                file_name=f"chat_{selected_session_id[:8]}.md",
                mime="text/markdown",
                use_container_width=True
            )

            if st.button("🗑️ 선택한 세션 삭제", use_container_width=True):
                chat_db.delete_session(selected_session_id)
                st.success("세션이 삭제되었습니다.")
                st.rerun()

    # 4. 우측 본문: 선택한 세션의 대화 내역 출력
    if not all_sessions:
        st.info("💡 아직 저장된 대화 내역이 없습니다. 실시간 채팅에서 새로운 대화를 시작해보세요!")
    elif not selected_session_id:
        st.warning("일치하는 세션이 없습니다. 다른 키워드를 검색해보세요.")
    else:
        selected_session = next((s for s in all_sessions if s["id"] == selected_session_id), None)
        session_title = selected_session["title"] if selected_session else "대화"
        session_created_at = selected_session["created_at"] if selected_session else "-"
        messages = chat_db.get_session_messages(selected_session_id)

        # 세션 정보 카드
        with st.container(border=True):
            col_info, col_dl = st.columns([3, 1])
            with col_info:
                st.subheader(f"📌 {session_title}")
                st.caption(f"생성 일시: {session_created_at} | 메시지 수: **{len(messages)}개**")
            with col_dl:
                st.download_button(
                    label="📥 Markdown 저장",
                    data=chat_db.export_session_markdown(selected_session_id).encode("utf-8"),
                    file_name=f"chat_{selected_session_id[:8]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="history_dl_btn"
                )

        st.write("")

        # 메시지 순차적 출력
        for msg in messages:
            with st.chat_message(msg["role"]):
                role_label = "👤 사용자" if msg["role"] == "user" else "🤖 AI 어시스턴트"
                st.caption(f"{role_label} • {msg['created_at']}")

                # 첨부 이미지 복원 렌더링
                if msg.get("images"):
                    st.markdown("**🖼️ 첨부 이미지:**")
                    cols = st.columns(min(len(msg["images"]), 3))
                    for idx, img_b64 in enumerate(msg["images"]):
                        with cols[idx % 3]:
                            st.image(base64.b64decode(img_b64), caption=f"이미지 #{idx+1}", width=280)

                # 첨부 문서 파일명 배지 표시
                if msg.get("files"):
                    file_badges = "  ".join([f"`📄 {f}`" for f in msg["files"]])
                    st.markdown(f"**📎 첨부 문서:** {file_badges}")

                # 텍스트 본문 출력
                st.markdown(msg["content"])


# 단독 실행 시에도 정상 동작하도록 지원
if __name__ == "__main__":
    st.set_page_config(
        page_title="과거 대화 히스토리",
        page_icon="📜",
        layout="wide"
    )
    show_history_page()
