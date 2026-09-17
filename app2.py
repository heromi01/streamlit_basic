import streamlit as st
from openai import OpenAI
import os
import base64
import uuid
from dotenv import load_dotenv
import chat_db
from app2_history import show_history_page

# ========================================================
# 0. 환경 변수 로드 (.env 연동)
# ========================================================
load_dotenv()

# ========================================================
# 1. 페이지 기본 설정
# ========================================================
st.set_page_config(
    page_title="OpenAI 멀티모달 챗봇 (SQLite & Vision)",
    page_icon="🤖",
    layout="wide"
)

# ========================================================
# 2. 사이드바 메뉴 선택 (화면 전환 제어)
# ========================================================
if "current_menu" not in st.session_state:
    st.session_state["current_menu"] = "💬 실시간 AI 채팅"

# 사이드바 최상단 화면 이동 라디오 메뉴
menu = st.sidebar.radio(
    "🧭 화면 이동",
    ["💬 실시간 AI 채팅", "📜 과거 대화 히스토리"],
    key="current_menu"
)
st.sidebar.divider()


# ========================================================
# 3. 팝업 모달 다이얼로그 (@st.dialog) 함수 선언
# ========================================================
@st.dialog("🖼️ 이미지 파일 첨부 (드래그 앤 드롭)")
def open_image_upload_dialog():
    """이미지 파일 전용 팝업 모달"""
    st.markdown("분석할 이미지 파일을 아래 영역에 **드래그 앤 드롭**하거나 **파일 찾기**를 클릭하세요.")
    uploaded_images = st.file_uploader(
        "이미지 파일 선택 (PNG, JPG, JPEG, WEBP)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        key="modal_image_uploader"
    )

    if uploaded_images:
        st.write(f"선택된 이미지: **{len(uploaded_images)}개**")
        preview_cols = st.columns(min(len(uploaded_images), 3))
        for idx, img in enumerate(uploaded_images):
            with preview_cols[idx % 3]:
                st.image(img, caption=img.name, width=150)

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


@st.dialog("📄 문서 파일 첨부 (드래그 앤 드롭)")
def open_file_upload_dialog():
    """문서 파일 전용 팝업 모달"""
    st.markdown("요약 및 분석할 문서 파일을 아래 영역에 **드래그 앤 드롭**하세요.")
    uploaded_docs = st.file_uploader(
        "문서 파일 선택 (TXT, CSV, MD, PY, JSON)",
        type=["txt", "csv", "md", "py", "json"],
        accept_multiple_files=True,
        key="modal_file_uploader"
    )

    if uploaded_docs:
        for doc in uploaded_docs:
            st.caption(f"📄 {doc.name} (크기: {doc.size} bytes)")

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
# 4. 실시간 AI 채팅 화면 구현 함수
# ========================================================
def show_chat_page():
    """실시간 AI 멀티모달 채팅 화면"""
    
    # 1. 상단 타이틀 및 설명
    st.title("🤖 OpenAI 멀티모달 AI 챗봇 (SQLite 영구 저장 & Vision)")
    st.markdown("OpenAI 최신 모델(GPT-5.5+)과 **SQLite 대화 영구 저장**, **이미지/문서 팝업 첨부** 기능을 지원하는 스마트 챗봇입니다.")
    st.caption("💡 텍스트 대화뿐만 아니라 이미지 및 문서 파일을 첨부하고, 과거 대화 내역을 언제든 다시 불러올 수 있습니다.")

    # 과거 대화 히스토리 화면으로 전환하는 버튼
    if st.button("📜 과거 대화 히스토리 대시보드로 이동", icon="📜", type="secondary"):
        st.session_state["current_menu"] = "📜 과거 대화 히스토리"
        st.rerun()

    st.divider()

    # 2. 세션 상태(st.session_state) 초기화
    if "current_session_id" not in st.session_state:
        new_sid = str(uuid.uuid4())
        chat_db.create_session(new_sid, "새로운 대화")
        st.session_state.current_session_id = new_sid

    if "pending_images" not in st.session_state:
        st.session_state.pending_images = []

    if "pending_files" not in st.session_state:
        st.session_state.pending_files = []

    # 3. 사이드바: 챗봇 환경 설정 및 대화 기록 관리
    with st.sidebar:
        st.header("⚙️ 챗봇 환경 설정")

        # [3-A] .env 환경 변수 연동 상태
        env_api_key = os.getenv("OPENAI_API_KEY", "")
        if env_api_key:
            st.success("🟢 .env 파일에서 API Key 연동 완료")
        else:
            st.warning("⚠️ .env 파일에 OPENAI_API_KEY가 없습니다.")

        api_key = st.text_input(
            "🔑 OpenAI API Key",
            value=env_api_key,
            type="password",
            placeholder="sk-...",
            help=".env 파일에 등록된 키가 기본 사용됩니다."
        )

        # [3-B] 모델 선택 (GPT-5.5+ 최신 규격)
        model_name = st.selectbox(
            "🧠 AI 모델 선택 (GPT-5.5+)",
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

        # [3-C] 시스템 프롬프트 설정
        system_instruction = st.text_area(
            "🎭 AI 역할 지침 (System Prompt)",
            value="당신은 친절하고 지적인 AI 어시스턴트입니다. 사용자의 질문과 첨부된 이미지 및 문서를 꼼꼼히 확인하고 명확하게 답변해주세요.",
            height=80
        )

        st.divider()

        # [3-D] SQLite 세션 관리
        st.subheader("📜 대화 세션 관리")

        # 1. 새 대화 시작 버튼
        if st.button("➕ 새 대화 시작 (New Chat)", use_container_width=True, type="primary"):
            new_sid = str(uuid.uuid4())
            chat_db.create_session(new_sid, "새로운 대화")
            st.session_state.current_session_id = new_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

        # 2. SQLite 세션 목록 선택
        saved_sessions = chat_db.get_all_sessions()
        session_options = {s["id"]: f"{s['title']} ({s['created_at'][:10]})" for s in saved_sessions}

        if st.session_state.current_session_id not in session_options:
            session_options[st.session_state.current_session_id] = "현재 대화 (새로운 대화)"

        session_keys = list(session_options.keys())
        current_idx = session_keys.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_keys else 0

        selected_sid = st.selectbox(
            "이전 대화 불러오기",
            options=session_keys,
            index=current_idx,
            format_func=lambda x: session_options.get(x, x)
        )

        if selected_sid != st.session_state.current_session_id:
            st.session_state.current_session_id = selected_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

        # 3. 현재 대화 세션 삭제 버튼
        if st.button("🗑️ 현재 대화 삭제", use_container_width=True):
            chat_db.delete_session(st.session_state.current_session_id)
            remaining_sessions = chat_db.get_all_sessions()
            if remaining_sessions:
                st.session_state.current_session_id = remaining_sessions[0]["id"]
            else:
                new_sid = str(uuid.uuid4())
                chat_db.create_session(new_sid, "새로운 대화")
                st.session_state.current_session_id = new_sid
            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()

        # 4. 사이드바 히스토리 페이지 이동 버튼
        st.markdown("---")
        if st.button("📜 과거 대화 히스토리 전체보기", use_container_width=True):
            st.session_state["current_menu"] = "📜 과거 대화 히스토리"
            st.rerun()

    # 4. 현재 세션 메시지 내역 불러오기 및 출력
    current_messages = chat_db.get_session_messages(st.session_state.current_session_id)

    for msg in current_messages:
        with st.chat_message(msg["role"]):
            if msg.get("images"):
                for img_b64 in msg["images"]:
                    st.image(base64.b64decode(img_b64), caption="첨부된 이미지", width=350)

            if msg.get("files"):
                for fname in msg["files"]:
                    st.caption(f"📎 첨부 문서: {fname}")

            st.markdown(msg["content"])

    # 5. 분리된 첨부 버튼 영역 (이미지 첨부 / 문서 파일 첨부)
    btn_col1, btn_col2, btn_info = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("🖼️ 이미지 첨부 (모달 팝업)", use_container_width=True):
            open_image_upload_dialog()

    with btn_col2:
        if st.button("📄 문서 파일 첨부 (모달 팝업)", use_container_width=True):
            open_file_upload_dialog()

    with btn_info:
        st.caption("각 버튼을 클릭하면 드래그 앤 드롭 지원 모달 팝업창이 열립니다.")

    # 6. 전송 대기 중인 첨부 항목 카드
    has_pending = bool(st.session_state.pending_images or st.session_state.pending_files)
    if has_pending:
        with st.container(border=True):
            col_title, col_cancel = st.columns([4, 1])
            with col_title:
                st.markdown("📎 **현재 전송 대기 중인 첨부 항목**:")
            with col_cancel:
                if st.button("❌ 첨부 전체 취소", use_container_width=True):
                    st.session_state.pending_images = []
                    st.session_state.pending_files = []
                    st.rerun()

            if st.session_state.pending_images:
                cols = st.columns(min(len(st.session_state.pending_images), 4))
                for i, p_img in enumerate(st.session_state.pending_images):
                    with cols[i % 4]:
                        st.image(base64.b64decode(p_img["b64"]), caption=p_img["name"], width=120)

            if st.session_state.pending_files:
                for p_file in st.session_state.pending_files:
                    st.caption(f"📄 {p_file['name']}")

    # 7. 하단 채팅 입력창
    user_prompt = st.chat_input("메시지를 입력하세요 (위 첨부 항목과 함께 전달됩니다)...")

    direct_send_btn = False
    if has_pending and not user_prompt:
        direct_send_btn = st.button("🚀 첨부 파일만으로 분석 요청하기", type="secondary")

    # 8. 메시지 전송 및 OpenAI 스트리밍 응답
    if user_prompt or direct_send_btn:
        if not api_key:
            st.warning("⚠️ OpenAI API Key가 필요합니다. 좌측 사이드바 또는 .env 파일을 확인해주세요!")
        else:
            actual_prompt = user_prompt if user_prompt else "(첨부된 파일 및 이미지 분석을 요청합니다)"

            # 문서 및 이미지 결합
            full_user_content = actual_prompt
            attached_filenames = []
            for pf in st.session_state.pending_files:
                full_user_content += f"\n\n[첨부 문서: {pf['name']}]\n```\n{pf['content']}\n```"
                attached_filenames.append(pf['name'])

            attached_images_b64 = [p_img["b64"] for p_img in st.session_state.pending_images]
            for p_img in st.session_state.pending_images:
                attached_filenames.append(f"🖼️ {p_img['name']}")

            # 사용자 메시지 표시
            with st.chat_message("user"):
                if attached_images_b64:
                    for img_b64 in attached_images_b64:
                        st.image(base64.b64decode(img_b64), caption="첨부된 이미지", width=350)
                if attached_filenames:
                    for fname in attached_filenames:
                        st.caption(f"📎 첨부: {fname}")
                st.markdown(actual_prompt)

            # SQLite 저장
            chat_db.save_message(
                session_id=st.session_state.current_session_id,
                role="user",
                content=actual_prompt,
                images=attached_images_b64,
                files=attached_filenames
            )

            # 첫 질문 시 세션 제목 자동 업데이트
            if len(current_messages) == 0:
                short_title = actual_prompt[:25] + ("..." if len(actual_prompt) > 25 else "")
                chat_db.update_session_title(st.session_state.current_session_id, short_title)

            # OpenAI 메시지 구성
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

            # OpenAI 스트리밍 호출
            client = OpenAI(api_key=api_key)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=api_messages,
                    stream=True
                )
                assistant_response = st.write_stream(stream)

            # AI 답변 SQLite 저장
            chat_db.save_message(
                session_id=st.session_state.current_session_id,
                role="assistant",
                content=assistant_response
            )

            st.session_state.pending_images = []
            st.session_state.pending_files = []
            st.rerun()


# ========================================================
# 5. 선택된 메뉴에 따른 화면 분기 실행
# ========================================================
if menu == "💬 실시간 AI 채팅":
    show_chat_page()
else:
    show_history_page()

