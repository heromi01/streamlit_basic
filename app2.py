import streamlit as st
from openai import OpenAI
import os
import base64
import uuid
from dotenv import load_dotenv
import chat_db
from app2_history import show_history_page
from styles import apply_custom_css

# ========================================================
# 0. 환경 변수 로드 (.env 연동)
# ========================================================
load_dotenv()

# ========================================================
# 1. 팝업 모달 다이얼로그 (@st.dialog) 함수 선언
# ========================================================
@st.dialog("🖼️ 이미지 파일 첨부")
def open_image_upload_dialog():
    """이미지 파일 전용 팝업 모달"""
    st.markdown("분석할 이미지 파일을 드래그 앤 드롭하거나 파일 찾기를 클릭하세요.")
    uploaded_images = st.file_uploader(
        "이미지 선택 (PNG, JPG, JPEG, WEBP)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        key="modal_image_uploader"
    )

    if uploaded_images:
        st.caption(f"선택된 이미지: **{len(uploaded_images)}개**")
        preview_cols = st.columns(min(len(uploaded_images), 3))
        for idx, img in enumerate(uploaded_images):
            with preview_cols[idx % 3]:
                st.image(img, caption=img.name, use_container_width=True)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✅ 첨부 완료", type="primary", use_container_width=True, key="btn_confirm_images"):
            if uploaded_images:
                for img in uploaded_images:
                    b64 = base64.b64encode(img.getvalue()).decode("utf-8")
                    ext = img.name.split(".")[-1].lower()
                    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
                    st.session_state.pending_images.append({
                        "name": img.name,
                        "b64": b64,
                        "mime": mime
                    })
            st.rerun()
    with btn_col2:
        if st.button("닫기", use_container_width=True, key="btn_close_image_modal"):
            st.rerun()


@st.dialog("📄 문서 파일 첨부")
def open_file_upload_dialog():
    """문서 파일 전용 팝업 모달"""
    st.markdown("분석할 텍스트 기반 문서 파일을 드래그 앤 드롭하세요.")
    uploaded_docs = st.file_uploader(
        "문서 선택 (TXT, CSV, MD, PY, JSON)",
        type=["txt", "csv", "md", "py", "json"],
        accept_multiple_files=True,
        key="modal_file_uploader"
    )

    if uploaded_docs:
        for doc in uploaded_docs:
            st.caption(f"📄 {doc.name} ({doc.size:,} bytes)")

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✅ 첨부 완료", type="primary", use_container_width=True, key="btn_confirm_files"):
            if uploaded_docs:
                for doc in uploaded_docs:
                    raw_bytes = doc.getvalue()
                    try:
                        text_content = raw_bytes.decode("utf-8")
                    except Exception:
                        text_content = raw_bytes.decode("cp949", errors="replace")
                    st.session_state.pending_files.append({
                        "name": doc.name,
                        "content": text_content
                    })
            st.rerun()
    with btn_col2:
        if st.button("닫기", use_container_width=True, key="btn_close_file_modal"):
            st.rerun()


# ========================================================
# 2. 실시간 AI 채팅 화면 구현 함수
# ========================================================
def show_chat_page():
    """실시간 AI 멀티모달 채팅 화면"""
    apply_custom_css()

    # 1. 세련된 상단 브랜딩 헤더
    st.markdown(
        """
        <div class="app-brand-header">
            <div>
                <h2 style="margin: 0; font-weight: 700; letter-spacing: -0.02em;">🤖 AI 멀티모달 어시스턴트</h2>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">
                    OpenAI 최신 모델 연동 • SQLite 실시간 대화 보관 • Vision 멀티모달 분석
                </p>
            </div>
            <div class="brand-pill">
                <span class="status-dot"></span>
                <span>Active Model</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. 세션 상태 초기화
    if "current_session_id" not in st.session_state:
        new_sid = str(uuid.uuid4())
        chat_db.create_session(new_sid, "새로운 대화")
        st.session_state.current_session_id = new_sid

    if "pending_images" not in st.session_state:
        st.session_state.pending_images = []

    if "pending_files" not in st.session_state:
        st.session_state.pending_files = []

    # 3. 사이드바: 챗봇 설정 및 세션 관리 (중복 버튼 제거 및 일원화)
    with st.sidebar:
        st.markdown("### ⚙️ 모델 & 환경 설정")

        env_api_key = os.getenv("OPENAI_API_KEY", "")
        api_key = st.text_input(
            "OpenAI API Key",
            value=env_api_key,
            type="password",
            placeholder="sk-...",
            help=".env 파일에 등록된 키가 기본 연동됩니다."
        )

        model_name = st.selectbox(
            "AI 모델 선택",
            options=[
                "gpt-5.5",
                "gpt-5.6-sol",
                "gpt-5.6-luna",
                "gpt-5.6-terra",
                "gpt-5",
                "gpt-5-mini",
                "gpt-4o"
            ],
            index=0
        )

        system_instruction = st.text_area(
            "시스템 역할 지침",
            value="당신은 친절하고 전문적인 AI 어시스턴트입니다. 사용자의 질문과 첨부된 자료를 꼼꼼하게 검토하고 논리적으로 답변해주세요.",
            height=70
        )

        st.markdown("---")
        st.markdown("### 💬 대화 세션")

        # 새 대화 시작 버튼
        if st.button("➕ 새 대화 시작", use_container_width=True, type="primary"):
            new_sid = str(uuid.uuid4())
            chat_db.create_session(new_sid, "새로운 대화")
            st.session_state.current_session_id = new_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

        # 세션 선택 목록
        saved_sessions = chat_db.get_all_sessions()
        session_options = {s["id"]: f"{s['title']} ({s['created_at'][:10]})" for s in saved_sessions}

        if st.session_state.current_session_id not in session_options:
            session_options[st.session_state.current_session_id] = "현재 대화 (새로운 대화)"

        session_keys = list(session_options.keys())
        current_idx = session_keys.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_keys else 0

        selected_sid = st.selectbox(
            "세션 목록",
            options=session_keys,
            index=current_idx,
            format_func=lambda x: session_options.get(x, x),
            label_visibility="collapsed"
        )

        if selected_sid != st.session_state.current_session_id:
            st.session_state.current_session_id = selected_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

        # 세션 관리 (삭제)
        if st.button("🗑️ 현재 세션 삭제", use_container_width=True):
            chat_db.delete_session(st.session_state.current_session_id)
            remaining = chat_db.get_all_sessions()
            if remaining:
                st.session_state.current_session_id = remaining[0]["id"]
            else:
                new_sid = str(uuid.uuid4())
                chat_db.create_session(new_sid, "새로운 대화")
                st.session_state.current_session_id = new_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

    # 4. 현재 대화 메시지 내역 불러오기
    current_messages = chat_db.get_session_messages(st.session_state.current_session_id)

    # [미니 세션 현황판] 현재 세션 상태 요약 배지 렌더링 (요구사항 1 적용)
    short_sid = st.session_state.current_session_id[:8]
    total_msgs = len(current_messages)
    pending_img_count = len(st.session_state.pending_images)
    pending_file_count = len(st.session_state.pending_files)

    st.markdown(
        f"""
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1.25rem; align-items: center;">
            <span class="chip" style="background: rgba(99, 102, 241, 0.08); font-size: 0.8rem;">
                🆔 세션: <code>{short_sid}</code>
            </span>
            <span class="chip" style="background: rgba(59, 130, 246, 0.08); font-size: 0.8rem;">
                🧠 모델: <b>{model_name}</b>
            </span>
            <span class="chip" style="background: rgba(16, 185, 129, 0.08); font-size: 0.8rem;">
                💬 대화: <b>{total_msgs}개</b>
            </span>
            <span class="chip" style="background: rgba(245, 158, 11, 0.08); font-size: 0.8rem;">
                📎 첨부 대기: <b>{pending_img_count}장 / {pending_file_count}개</b>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not current_messages:
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align: center; padding: 1.5rem 1rem;">
                    <span style="font-size: 2.2rem;">👋</span>
                    <h3 style="margin: 0.5rem 0 0.25rem 0;">무엇을 도와드릴까요?</h3>
                    <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 0;">
                        텍스트 질문을 입력하거나, 아래 툴바에서 이미지 및 문서 파일을 첨부해 분석을 요청해보세요.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        for msg in current_messages:
            with st.chat_message(msg["role"]):
                if msg.get("images"):
                    img_cols = st.columns(min(len(msg["images"]), 3))
                    for idx, img_b64 in enumerate(msg["images"]):
                        with img_cols[idx % 3]:
                            st.image(base64.b64decode(img_b64), caption="첨부 이미지", use_container_width=True)

                if msg.get("files"):
                    file_badges = " ".join([f"`📄 {f}`" for f in msg["files"]])
                    st.markdown(f"📎 {file_badges}")

                st.markdown(msg["content"])

    # 5. 전송 대기 중인 첨부 항목 카드 (컴팩트 칩 스타일)
    has_pending = bool(st.session_state.pending_images or st.session_state.pending_files)
    if has_pending:
        with st.container(border=True):
            top_col, cancel_col = st.columns([5, 1])
            with top_col:
                st.markdown("**📎 전송 대기 중인 첨부 항목**")
            with cancel_col:
                if st.button("취소", use_container_width=True, key="btn_cancel_pending"):
                    st.session_state.pending_images = []
                    st.session_state.pending_files = []
                    st.rerun()

            if st.session_state.pending_images:
                cols = st.columns(min(len(st.session_state.pending_images), 4))
                for i, p_img in enumerate(st.session_state.pending_images):
                    with cols[i % 4]:
                        st.image(base64.b64decode(p_img["b64"]), caption=p_img["name"], width=110)

            if st.session_state.pending_files:
                file_chips = "".join([f"<span class='chip'>📄 {pf['name']}</span>" for pf in st.session_state.pending_files])
                st.markdown(f"<div class='chip-container'>{file_chips}</div>", unsafe_allow_html=True)

    # 6. 컴팩트 퀵 첨부 툴바
    st.write("")
    attach_col1, attach_col2, attach_space = st.columns([1.2, 1.2, 5])
    with attach_col1:
        if st.button("🖼️ 이미지 첨부", use_container_width=True, key="quick_img_btn"):
            open_image_upload_dialog()
    with attach_col2:
        if st.button("📄 문서 첨부", use_container_width=True, key="quick_doc_btn"):
            open_file_upload_dialog()

    # 7. 하단 채팅 입력창
    user_prompt = st.chat_input("메시지를 입력하세요...")

    direct_send = False
    if has_pending and not user_prompt:
        direct_send = st.button("🚀 첨부 항목만으로 분석 요청", type="secondary")

    # 8. 메시지 전송 및 OpenAI 응답 처리
    if user_prompt or direct_send:
        if not api_key:
            st.warning("⚠️ OpenAI API Key가 필요합니다. 사이드바 설정을 확인해주세요.")
        else:
            actual_prompt = user_prompt if user_prompt else "(첨부된 파일 및 이미지 분석을 요청합니다)"

            full_user_content = actual_prompt
            attached_filenames = []
            for pf in st.session_state.pending_files:
                full_user_content += f"\n\n[첨부 문서: {pf['name']}]\n```\n{pf['content']}\n```"
                attached_filenames.append(pf['name'])

            attached_images_b64 = [p_img["b64"] for p_img in st.session_state.pending_images]
            for p_img in st.session_state.pending_images:
                attached_filenames.append(f"🖼️ {p_img['name']}")

            # 사용자 메시지 렌더링
            with st.chat_message("user"):
                if attached_images_b64:
                    cols = st.columns(min(len(attached_images_b64), 3))
                    for i, img_b64 in enumerate(attached_images_b64):
                        with cols[i % 3]:
                            st.image(base64.b64decode(img_b64), caption="첨부 이미지", use_container_width=True)
                if attached_filenames:
                    file_badges = " ".join([f"`{f}`" for f in attached_filenames])
                    st.markdown(f"📎 {file_badges}")
                st.markdown(actual_prompt)

            # DB 저장
            chat_db.save_message(
                session_id=st.session_state.current_session_id,
                role="user",
                content=actual_prompt,
                images=attached_images_b64,
                files=attached_filenames
            )

            # 세션 제목 자동 업데이트
            if len(current_messages) == 0:
                short_title = actual_prompt[:25] + ("..." if len(actual_prompt) > 25 else "")
                chat_db.update_session_title(st.session_state.current_session_id, short_title)

            # API 메시지 포맷 구성
            api_messages = [{"role": "system", "content": system_instruction}]
            for prev in current_messages:
                if prev["role"] == "user":
                    if prev.get("images"):
                        payload = [{"type": "text", "text": prev["content"]}]
                        for b64_str in prev["images"]:
                            payload.append({
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{b64_str}"}
                            })
                        api_messages.append({"role": "user", "content": payload})
                    else:
                        api_messages.append({"role": "user", "content": prev["content"]})
                else:
                    api_messages.append({"role": "assistant", "content": prev["content"]})

            if attached_images_b64:
                current_payload = [{"type": "text", "text": full_user_content}]
                for p_img in st.session_state.pending_images:
                    current_payload.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{p_img['mime']};base64,{p_img['b64']}"}
                    })
                api_messages.append({"role": "user", "content": current_payload})
            else:
                api_messages.append({"role": "user", "content": full_user_content})

            # 스트리밍 생성
            client = OpenAI(api_key=api_key)
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=api_messages,
                    stream=True
                )
                assistant_response = st.write_stream(stream)

            # AI 응답 저장
            chat_db.save_message(
                session_id=st.session_state.current_session_id,
                role="assistant",
                content=assistant_response
            )

            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()


# ========================================================
# 3. 독립 실행 지원
# ========================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="AI 멀티모달 어시스턴트",
        page_icon="🤖",
        layout="wide"
    )

    if "current_menu" not in st.session_state:
        st.session_state["current_menu"] = "💬 실시간 AI 채팅"

    from admin_analytics import show_admin_analytics_page

    menu = st.sidebar.radio(
        "🧭 메뉴",
        ["💬 실시간 AI 채팅", "📜 과거 대화 히스토리", "📈 관리자 통계 분석실"],
        key="current_menu"
    )

    if menu == "💬 실시간 AI 채팅":
        show_chat_page()
    elif menu == "📜 과거 대화 히스토리":
        show_history_page()
    else:
        show_admin_analytics_page()
