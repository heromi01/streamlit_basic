import streamlit as st
import pandas as pd
import chat_db
from styles import apply_custom_css

# ========================================================
# 관리자 2차 인증 모달 팝업 다이얼로그 (@st.dialog)
# - 관리자 통계 분석실 접근 시 보안 강화를 위해 팝업으로 추가 인증 수행
# ========================================================
@st.dialog("🔒 관리자 2차 보안 인증 (Admin Authentication)")
def admin_login_dialog():
    """관리자 통계 분석실 접근을 위한 2차 계정 인증 팝업"""
    st.markdown("관리자 통계 분석실에 접근하려면 **관리자 전용 계정**으로 한 번 더 인증해야 합니다.")
    st.caption("💡 기본 관리자 계정: 아이디 `admin` / 비밀번호 `admin1234`")

    # 관리자 계정 정보 입력 폼
    admin_id = st.text_input("👤 관리자 ID", key="admin_popup_id", placeholder="admin")
    admin_pw = st.text_input("🔑 관리자 비밀번호", type="password", key="admin_popup_pw", placeholder="••••••••")

    col_login, col_cancel = st.columns(2)
    with col_login:
        if st.button("🔓 인증 및 입장", type="primary", use_container_width=True, key="admin_popup_login_btn"):
            if admin_id.strip() == "admin" and admin_pw.strip() in ["admin1234", "1234", "admin"]:
                st.session_state.is_admin_authenticated = True
                st.success("✅ 관리자 인증에 성공했습니다!")
                st.rerun()
            else:
                st.error("❌ 관리자 아이디 또는 비밀번호가 올바르지 않습니다.")

    with col_cancel:
        if st.button("❌ 취소 및 돌아가기", use_container_width=True, key="admin_popup_cancel_btn"):
            st.session_state.current_menu = "🤖 AI 멀티모달 챗봇"
            st.rerun()


def show_admin_analytics_page():
    """관리자 전용 통계 분석 및 세션 관리 대시보드"""
    apply_custom_css()

    # 0. 전역 로그인 여부 검증 (미인증 사용자는 로그인 화면 렌더링 후 차단)
    if not st.session_state.get("is_logged_in", False):
        from app2 import show_login_page
        show_login_page()
        return

    # 1. 관리자 2차 인증 상태 관리
    if "is_admin_authenticated" not in st.session_state:
        st.session_state.is_admin_authenticated = False

    # 2. 미인증 상태인 경우 2차 로그인 팝업 다이얼로그 노출 및 차단
    if not st.session_state.is_admin_authenticated:
        # 팝업 다이얼로그 즉시 띄우기
        admin_login_dialog()

        # 배경 안내 카드 (팝업 닫힘 시 재호출 지원)
        with st.container(border=True):
            st.warning("""
            ### 🔒 관리자 2차 보안 인증이 필요합니다
            관리자 통계 분석실은 전체 대화 세션 감사, 삭제 및 통계 데이터 접근 권한이 포함되어 있습니다.  
            안전한 시스템 운영을 위해 **관리자 계정으로 한 번 더 인증**을 진행해주세요.
            """)
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button("🔑 관리자 인증 팝업 열기", type="primary", use_container_width=True):
                    admin_login_dialog()
            with col_btn2:
                if st.button("💬 실시간 챗봇으로 돌아가기", use_container_width=True):
                    st.session_state.current_menu = "🤖 AI 멀티모달 챗봇"
                    st.rerun()
        return

    # 3. 인증 완료 시: 상단 관리자 브랜딩 헤더 및 모드 종료(잠금) 버튼
    col_header, col_logout = st.columns([4, 1.2])
    with col_header:
        st.markdown(
            """
            <div class="app-brand-header" style="margin-bottom: 0.5rem;">
                <div>
                    <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.02em;">📈 관리자 통계 분석실 (Admin Studio)</h2>
                    <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">
                        대화량 추이 시각화 • 사용자/AI 발화 분석 • 세션 상세 감사 및 관리
                    </p>
                </div>
                <div class="brand-pill" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border-color: rgba(239, 68, 68, 0.25);">
                    <span class="status-dot" style="background-color: #ef4444; box-shadow: 0 0 8px #ef4444;"></span>
                    <span>Admin Mode</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_logout:
        st.write("") # 수직 정렬 여백
        if st.button("🔒 관리자 모드 종료", type="secondary", use_container_width=True, help="관리자 인증을 잠그고 챗봇 화면으로 돌아갑니다."):
            st.session_state.is_admin_authenticated = False
            st.session_state.current_menu = "🤖 AI 멀티모달 챗봇"
            st.rerun()

    st.divider()

    # 4. 상단 핵심 KPI 메트릭 카드 4종
    stats = chat_db.get_db_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="전체 대화 세션", value=f"{stats['total_sessions']}개")
    with col2:
        st.metric(label="누적 메시지 수", value=f"{stats['total_messages']}개")
    with col3:
        st.metric(label="사용자 질문 (User)", value=f"{stats['user_messages']}건")
    with col4:
        st.metric(label="AI 어시스턴트 답변", value=f"{stats['assistant_messages']}건")

    st.write("")

    # 5. 탭 분리: 통계 및 시각화 vs 세션 데이터 관리
    tab_analytics, tab_management = st.tabs([
        "📊 통계 및 시각화 차트 분석",
        "📋 세션 데이터 상세 & 관리"
    ])

    # ----------------------------------------------------
    # TAB 1: 통계 및 시각화 차트 분석
    # ----------------------------------------------------
    with tab_analytics:
        st.markdown("#### 📅 일자별 대화량 추이")
        daily_data = chat_db.get_daily_stats()

        if daily_data:
            df_daily = pd.DataFrame(daily_data)
            df_daily = df_daily.rename(columns={
                "date": "일자",
                "total": "전체 메시지",
                "user": "사용자 질문",
                "assistant": "AI 답변"
            })
            df_chart = df_daily.set_index("일자")[["사용자 질문", "AI 답변"]]

            # 일자별 누적 바 차트
            st.bar_chart(df_chart, stack=True, use_container_width=True)

            # 세부 수치 요약 테이블 (접이식)
            with st.expander("📊 일자별 데이터 상세 테이블 보기", expanded=False):
                st.dataframe(df_daily, use_container_width=True, hide_index=True)
        else:
            st.info("💡 아직 누적된 일자별 대화 데이터가 없습니다.")

        st.write("")
        st.markdown("#### 👥 발화 비율 및 세션 랭킹")
        rank_col1, rank_col2 = st.columns([1, 1])

        with rank_col1:
            st.caption("**발화 주체별 메시지 비중 (User vs AI)**")
            if stats["total_messages"] > 0:
                df_role = pd.DataFrame({
                    "발화 주체": ["사용자 (User)", "AI 어시스턴트"],
                    "메시지 수": [stats["user_messages"], stats["assistant_messages"]]
                }).set_index("발화 주체")
                st.bar_chart(df_role, horizontal=True, use_container_width=True)
            else:
                st.info("메시지 데이터가 없습니다.")

        with rank_col2:
            st.caption("**대화량 상위 세션 (Top Active Sessions)**")
            top_sessions = chat_db.get_session_message_counts()
            if top_sessions:
                df_top = pd.DataFrame(top_sessions[:5])
                df_top = df_top.rename(columns={
                    "title": "세션 제목",
                    "created_at": "생성 일시",
                    "msg_count": "메시지 수"
                })[["세션 제목", "메시지 수", "생성 일시"]]
                st.dataframe(df_top, use_container_width=True, hide_index=True)
            else:
                st.info("세션 데이터가 없습니다.")

    # ----------------------------------------------------
    # TAB 2: 세션 데이터 상세 & 관리
    # ----------------------------------------------------
    with tab_management:
        all_sessions = chat_db.get_all_sessions()

        if not all_sessions:
            st.info("💡 저장된 세션이 없습니다.")
        else:
            filter_col1, filter_col2 = st.columns([2, 1])
            with filter_col1:
                keyword = st.text_input("🔍 세션 제목 및 본문 키워드 필터", placeholder="키워드 검색...", key="admin_search")
            with filter_col2:
                sort_order = st.selectbox("정렬 순서", ["최신순", "과거순"], key="admin_sort")

            filtered_sessions = list(all_sessions)
            if sort_order == "과거순":
                filtered_sessions.reverse()

            if keyword.strip():
                matched_records = chat_db.search_messages(keyword.strip())
                matched_ids = {m["session_id"] for m in matched_records}
                filtered_sessions = [s for s in filtered_sessions if s["id"] in matched_ids or keyword.lower() in s["title"].lower()]

            if not filtered_sessions:
                st.warning("조건에 일치하는 세션이 없습니다.")
            else:
                session_map = {s["id"]: f"[{s['created_at'][:10]}] {s['title']}" for s in filtered_sessions}
                selected_admin_sid = st.selectbox(
                    "상세 확인할 세션 선택",
                    options=list(session_map.keys()),
                    format_func=lambda sid: session_map.get(sid, sid)
                )

                selected_sess = next((s for s in all_sessions if s["id"] == selected_admin_sid), None)
                if selected_sess:
                    sess_msgs = chat_db.get_session_messages(selected_admin_sid)

                    with st.container(border=True):
                        info_c, act_c1, act_c2 = st.columns([3, 1.2, 1.2])
                        with info_c:
                            st.markdown(f"**📌 {selected_sess['title']}**")
                            st.caption(f"ID: `{selected_admin_sid}` | 생성: {selected_sess['created_at']} | 메시지: {len(sess_msgs)}개")
                        with act_c1:
                            md_content = chat_db.export_session_markdown(selected_admin_sid)
                            st.download_button(
                                "📥 Markdown 저장",
                                data=md_content.encode("utf-8"),
                                file_name=f"admin_{selected_admin_sid[:8]}.md",
                                mime="text/markdown",
                                use_container_width=True,
                                key="admin_dl_btn"
                            )
                        with act_c2:
                            if st.button("🗑️ 세션 삭제", use_container_width=True, type="secondary", key="admin_del_btn"):
                                chat_db.delete_session(selected_admin_sid)
                                st.success("세션이 삭제되었습니다.")
                                st.rerun()

                    # 메시지 타임라인 미리보기
                    with st.expander("📜 메시지 원본 로그 열람", expanded=True):
                        for m in sess_msgs:
                            role_icon = "👤" if m["role"] == "user" else "🤖"
                            st.markdown(f"**{role_icon} {m['role'].upper()}** `[{m['created_at']}]`")
                            st.markdown(m["content"])
                            st.markdown("---")

if __name__ == "__main__":
    st.set_page_config(
        page_title="관리자 통계 분석실",
        page_icon="📈",
        layout="wide"
    )
    show_admin_analytics_page()
