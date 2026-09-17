import streamlit as st
import base64
import chat_db
from styles import apply_custom_css

# ========================================================
# 과거 대화 히스토리 화면 표시 함수
# ========================================================
def show_history_page():
    """과거 대화 내역 조회 및 분석 대시보드 화면"""
    apply_custom_css()

    # 1. 상단 브랜딩 헤더 (중복 이동 버튼 제거)
    st.markdown(
        """
        <div class="app-brand-header">
            <div>
                <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.02em;">📜 대화 히스토리 & 분석 대시보드</h2>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">
                    SQLite 영구 보관된 대화 세션 조회 • 키워드 검색 • 미디어 원본 복원
                </p>
            </div>
            <div class="brand-pill">
                <span class="status-dot"></span>
                <span>Database Sync</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. 대화 통계 요약 지표 (KPI Metrics)
    stats = chat_db.get_db_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="총 세션 수", value=f"{stats['total_sessions']}개")
    with col2:
        st.metric(label="총 메시지 수", value=f"{stats['total_messages']}개")
    with col3:
        st.metric(label="사용자 질문", value=f"{stats['user_messages']}개")
    with col4:
        st.metric(label="AI 답변", value=f"{stats['assistant_messages']}개")

    st.write("")

    # 3. 사이드바: 검색, 정렬 및 세션 선택 (중복 이동 버튼 제거)
    all_sessions = chat_db.get_all_sessions()

    with st.sidebar:
        st.markdown("### 🔍 대화 탐색")

        # 키워드 검색
        search_keyword = st.text_input(
            "본문 키워드 검색",
            placeholder="검색어 입력...",
            label_visibility="collapsed"
        )

        matched_session_ids = set()
        if search_keyword.strip():
            search_results = chat_db.search_messages(search_keyword.strip())
            st.caption(f"일치 결과: **{len(search_results)}건**")
            matched_session_ids = {r["session_id"] for r in search_results}

        # 정렬 옵션
        sort_order = st.radio(
            "정렬 방식",
            ["최신순", "과거순"],
            horizontal=True
        )

        sessions_to_display = list(all_sessions)
        if sort_order == "과거순":
            sessions_to_display.reverse()

        if search_keyword.strip() and matched_session_ids:
            if st.checkbox("일치 세션만 보기", value=True):
                sessions_to_display = [s for s in sessions_to_display if s["id"] in matched_session_ids]

        st.markdown("---")
        st.markdown("### 📋 세션 목록")

        if not sessions_to_display:
            st.warning("표시할 세션이 없습니다.")
            selected_session_id = None
        else:
            session_dict = {
                s["id"]: f"[{s['created_at'][:10]}] {s['title']}"
                for s in sessions_to_display
            }

            selected_session_id = st.selectbox(
                "세션 선택",
                options=list(session_dict.keys()),
                format_func=lambda sid: session_dict.get(sid, sid),
                label_visibility="collapsed"
            )

            # 선택 세션 삭제 버튼 (사이드바 관리 영역)
            if st.button("🗑️ 선택 세션 삭제", use_container_width=True):
                chat_db.delete_session(selected_session_id)
                st.rerun()

    # 4. 우측 본문: 선택된 세션 대화 상세 출력
    if not all_sessions:
        st.info("💡 아직 저장된 대화 내역이 없습니다. 새로운 대화를 시작해보세요!")
    elif not selected_session_id:
        st.warning("일치하는 세션이 없습니다. 다른 키워드로 검색해보세요.")
    else:
        selected_session = next((s for s in all_sessions if s["id"] == selected_session_id), None)
        session_title = selected_session["title"] if selected_session else "대화"
        session_created_at = selected_session["created_at"] if selected_session else "-"
        messages = chat_db.get_session_messages(selected_session_id)

        # 세션 정보 및 단일 다운로드 헤더 카드
        with st.container(border=True):
            col_info, col_dl = st.columns([4, 1.2])
            with col_info:
                st.markdown(f"### 📌 {session_title}")
                st.caption(f"생성 일시: {session_created_at} • 총 {len(messages)}개의 메시지")
            with col_dl:
                md_text = chat_db.export_session_markdown(selected_session_id)
                st.download_button(
                    label="📥 Markdown 내보내기",
                    data=md_text.encode("utf-8"),
                    file_name=f"chat_{selected_session_id[:8]}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        st.write("")

        # 메시지 히스토리 순차적 렌더링
        for msg in messages:
            with st.chat_message(msg["role"]):
                role_label = "👤 사용자" if msg["role"] == "user" else "🤖 AI 어시스턴트"
                st.caption(f"{role_label} • {msg['created_at']}")

                # 첨부 이미지 복원
                if msg.get("images"):
                    cols = st.columns(min(len(msg["images"]), 3))
                    for idx, img_b64 in enumerate(msg["images"]):
                        with cols[idx % 3]:
                            st.image(base64.b64decode(img_b64), caption=f"첨부 이미지 #{idx+1}", use_container_width=True)

                # 첨부 파일 태그 칩 복원
                if msg.get("files"):
                    file_chips = "".join([f"<span class='chip'>📄 {f}</span>" for f in msg["files"]])
                    st.markdown(f"<div class='chip-container'>{file_chips}</div>", unsafe_allow_html=True)

                st.markdown(msg["content"])


# 단독 실행 지원
if __name__ == "__main__":
    st.set_page_config(
        page_title="대화 히스토리 & 분석",
        page_icon="📜",
        layout="wide"
    )
    show_history_page()
