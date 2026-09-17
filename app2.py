import streamlit as st
from openai import OpenAI
import os
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
# 1. 페이지 기본 환경 설정 (중복 호출 방지)
# ========================================================
try:
    st.set_page_config(
        page_title="OpenAI 텍스트 전용 스마트 챗봇",
        page_icon="🤖",
        layout="wide"
    )
except Exception:
    pass

apply_custom_css()

# ========================================================
# 2. 세션 상태(st.session_state) 초기화
# ========================================================
# 로그인 여부 기본값 (미인증 상태)
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# 로그인한 사용자 ID
if "login_user" not in st.session_state:
    st.session_state.login_user = ""

# 화면 이동 메뉴 기본값
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "💬 실시간 AI 채팅"

# 현재 대화 세션 ID 초기화
if "current_session_id" not in st.session_state:
    existing_sessions = chat_db.get_all_sessions()
    if existing_sessions:
        st.session_state.current_session_id = existing_sessions[0]["id"]
    else:
        new_sid = str(uuid.uuid4())
        chat_db.create_session(new_sid, "새로운 대화")
        st.session_state.current_session_id = new_sid

# API Key 세션 상태
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")

# AI 모델 기본값 설정 (GPT-5.5 이상 모델 규격)
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-5.5"

# 시스템 프롬프트 기본값
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "당신은 친절하고 명확한 답변을 제공하는 지적인 AI 어시스턴트입니다."


# ========================================================
# 3. 로그인 화면 (보안 취약성 안내문 포함)
# ========================================================
def show_login_page():
    """로그인 폼 및 보안 취약성 상세 안내 화면"""
    st.title("🔐 OpenAI 챗봇 시스템 로그인")
    st.markdown("대화형 AI 서비스를 이용하기 위해 로그인을 진행해주세요.")

    # ⚠️ 보안 취약성 안내문 (Security Disclaimer)
    st.warning("""
    ### ⚠️ 보안 취약성 및 주의사항 안내 (Security Disclaimer)
    본 애플리케이션의 로그인 기능은 **Streamlit 세션 상태(`st.session_state`) 기반의 실습 및 프로토타입용 데모 인증**입니다.
    
    1. **단방향 암호화 해싱(Bcrypt, Argon2 등) 부재**: 입력된 비밀번호가 DB에 안전하게 해싱되지 않고 단순 세션 메모리에 보관됩니다.
    2. **HTTPS 및 전송 구간 보안 미보장**: 로컬 또는 기본 HTTP 통신 시 패킷 스니핑 및 세션 하이재킹 위험이 있습니다.
    3. **새로고침 시 세션 휘발**: 브라우저 새로고침이나 탭 종료 시 세션 상태가 초기화될 수 있습니다.
    4. **🚨 실제 운영 환경(Production) 절대 사용 금지**: 실무 환경 배포 시에는 반드시 OAuth2.0(Google, GitHub 등), Supabase Auth, Firebase Auth 등 검증된 보안 인증 인프라를 적용하십시오.
    """)

    st.write("")

    # 로그인 입력 폼 카드
    with st.container(border=True):
        st.subheader("데모 계정 로그인")
        st.caption("💡 테스트용 기본 계정: 아이디 `admin` / 비밀번호 `1234` (임의의 값을 입력하셔도 실습 가능합니다)")
        
        login_col1, login_col2 = st.columns(2)
        with login_col1:
            input_id = st.text_input("👤 아이디 (ID)", placeholder="admin", key="input_user_id")
        with login_col2:
            input_pw = st.text_input("🔑 비밀번호 (Password)", type="password", placeholder="1234", key="input_user_pw")

        btn_login = st.button("🚀 로그인 및 챗봇 시작하기", type="primary", use_container_width=True)

        if btn_login:
            if not input_id.strip() or not input_pw.strip():
                st.error("아이디와 비밀번호를 모두 입력해주세요.")
            else:
                st.session_state.is_logged_in = True
                st.session_state.login_user = input_id.strip()
                st.success(f"🎉 환영합니다, **{input_id}**님! 챗봇 화면으로 이동합니다.")
                st.rerun()


# ========================================================
# 4. 사이드바 설정 및 세션 관리 렌더링
# ========================================================
def render_chat_sidebar():
    """사이드바 설정 패널 (접속 정보, API Key, 모델 선택, 세션 관리)"""
    with st.sidebar:
        st.markdown(f"👤 접속자: **{st.session_state.login_user or '게스트'}**님")
        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.login_user = ""
            st.rerun()

        st.divider()

        # 화면 전환 메뉴 (단독 실행 모드일 때 라디오 노출)
        if st.session_state.current_menu in ["💬 실시간 AI 채팅", "📜 과거 대화 히스토리"]:
            nav_choice = st.radio(
                "🧭 화면 이동",
                ["💬 실시간 AI 채팅", "📜 과거 대화 히스토리"],
                index=0 if st.session_state.current_menu == "💬 실시간 AI 채팅" else 1,
                key="sidebar_nav_radio"
            )
            if nav_choice != st.session_state.current_menu:
                st.session_state.current_menu = nav_choice
                st.rerun()
            st.divider()

        # 🔑 OpenAI API Key 설정
        st.subheader("🔑 OpenAI API Key")
        def on_sidebar_key_change():
            st.session_state.api_key = st.session_state.sidebar_api_key_input.strip()

        st.text_input(
            "API Key 등록/변경",
            value=st.session_state.api_key,
            type="password",
            placeholder="sk-...",
            help="OpenAI API 키를 입력하면 세션에 즉시 반영됩니다.",
            key="sidebar_api_key_input",
            on_change=on_sidebar_key_change
        )

        # API Key 유효성 즉시 검사 버튼
        if st.button("🔍 API Key 연결 확인", use_container_width=True):
            test_key = st.session_state.api_key.strip()
            if not test_key:
                st.warning("API Key를 먼저 입력해주세요.")
            else:
                try:
                    test_client = OpenAI(api_key=test_key)
                    test_client.models.list()
                    st.success("✅ OpenAI API Key가 정상 확인되었습니다!")
                except Exception as test_err:
                    st.error(f"❌ API Key 인증 실패: {test_err}")

        # 🧠 AI 모델 선택 (GPT-5.5 이상 모델 규격만 제공)
        model_options = [
            "gpt-5.5",
            "gpt-5.5-turbo",
            "gpt-5.6",
            "gpt-5.6-sol",
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "gpt-6.0"
        ]
        curr_model = st.session_state.get("selected_model", "gpt-5.5")
        if curr_model not in model_options:
            curr_model = model_options[0]
            st.session_state.selected_model = curr_model
        model_idx = model_options.index(curr_model)
        st.session_state.selected_model = st.selectbox(
            "🧠 AI 모델 선택 (GPT-5.5+)",
            options=model_options,
            index=model_idx,
            help="GPT-5.5 이상의 최신 모델 목록입니다."
        )

        # 🎭 시스템 프롬프트 설정
        st.session_state.system_prompt = st.text_area(
            "🎭 AI 역할 지침 (System Prompt)",
            value=st.session_state.get("system_prompt", "당신은 친절하고 명확한 답변을 제공하는 지적인 AI 어시스턴트입니다."),
            height=70
        )

        st.divider()

        # 🗄️ 세션 관리 (최대 10개 유지)
        st.subheader("🗄️ 대화 세션 관리")
        st.caption("💡 DB에 최대 10개 세션만 보관되며, 초과 시 오래된 세션부터 자동 삭제됩니다.")

        # 새 대화 시작 버튼
        if st.button("➕ 새 대화 시작 (New Chat)", use_container_width=True, type="primary"):
            new_sid = str(uuid.uuid4())
            chat_db.create_session(new_sid, "새로운 대화")
            st.session_state.current_session_id = new_sid
            st.rerun()

        # 세션 목록 준비
        all_sessions = chat_db.get_all_sessions()
        session_ids = [s["id"] for s in all_sessions]
        if st.session_state.current_session_id not in session_ids:
            if session_ids:
                st.session_state.current_session_id = session_ids[0]
            else:
                new_sid = str(uuid.uuid4())
                chat_db.create_session(new_sid, "새로운 대화")
                st.session_state.current_session_id = new_sid
                all_sessions = chat_db.get_all_sessions()
                session_ids = [s["id"] for s in all_sessions]

        session_map = {s["id"]: f"[{s['created_at'][:10]}] {s['title']}" for s in all_sessions}
        curr_idx = session_ids.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_ids else 0

        def on_session_select_change():
            st.session_state.current_session_id = st.session_state.session_selector_widget

        st.selectbox(
            "보관된 세션 선택 (최대 10개)",
            options=session_ids,
            index=curr_idx,
            format_func=lambda sid: session_map.get(sid, sid),
            key="session_selector_widget",
            on_change=on_session_select_change
        )

        # 현재 대화 세션 삭제 버튼
        if st.button("🗑️ 현재 세션 삭제", use_container_width=True):
            chat_db.delete_session(st.session_state.current_session_id)
            remaining = chat_db.get_all_sessions()
            if remaining:
                st.session_state.current_session_id = remaining[0]["id"]
            else:
                new_sid = str(uuid.uuid4())
                chat_db.create_session(new_sid, "새로운 대화")
                st.session_state.current_session_id = new_sid
            st.rerun()


# ========================================================
# 5. 실시간 텍스트 전용 AI 채팅 화면
# ========================================================
def show_chat_page():
    """실시간 텍스트 전용 AI 채팅 화면"""

    # 미로그인 상태라면 로그인 화면 렌더링 후 중단
    if not st.session_state.get("is_logged_in", False):
        show_login_page()
        return

    # 사이드바 렌더링
    render_chat_sidebar()

    # 1. 상단 타이틀 및 소개
    st.title("🤖 OpenAI 텍스트 전용 스마트 챗봇")
    st.markdown("최신 OpenAI 모델을 활용한 **실시간 텍스트 대화** 공간입니다. (SQLite 영구 보관 & 세션당 100턴 제한)")
    st.caption("💡 불필요한 첨부 요소를 배제하고 대화 본문에 집중한 심플하고 빠른 챗봇입니다.")

    # 과거 대화 히스토리 화면 전환 버튼
    col_top1, col_top2 = st.columns([1, 4])
    with col_top1:
        if st.button("📜 과거 대화 내역 전체보기", type="secondary", use_container_width=True):
            st.session_state.current_menu = "📜 과거 대화 히스토리"
            st.rerun()

    st.divider()

    # 2. 현재 세션 대화 턴 수 및 제한 상태 확인
    current_sid = st.session_state.current_session_id
    turn_count = chat_db.get_session_turn_count(current_sid)
    is_limit_reached = chat_db.is_turn_limit_reached(current_sid, max_turns=chat_db.MAX_TURNS_PER_SESSION)

    # 3. 현재 세션 상단 정보 카드 (디자인 리뉴얼)
    with st.container(border=True):
        info_col1, info_col2, info_col3 = st.columns([3, 2, 2])
        with info_col1:
            sessions = chat_db.get_all_sessions()
            curr_title = next((s["title"] for s in sessions if s["id"] == current_sid), "새로운 대화")
            st.markdown(f"📌 **현재 세션**: `{curr_title}`")
        with info_col2:
            turn_color = "red" if is_limit_reached else "green"
            st.markdown(f"💬 **대화 진행도**: :{turn_color}[{turn_count} / {chat_db.MAX_TURNS_PER_SESSION} 턴]")
        with info_col3:
            if st.session_state.api_key.strip():
                st.markdown("🔑 **API Key**: :green[등록 완료 🟢]")
            else:
                st.markdown("🔑 **API Key**: :red[미등록 🔴]")

    # 4. API Key 등록 여부 검증 (Key가 없으면 채팅 불가 차단)
    current_api_key = st.session_state.api_key.strip()

    if not current_api_key:
        st.warning("""
        ### 🔑 OpenAI API Key 등록이 필요합니다!
        본 챗봇은 **OpenAI API Key가 등록되어야만 동작**하도록 설정되어 있습니다.  
        아래 입력창 또는 **좌측 사이드바**에서 API Key(`sk-...`)를 등록해주세요.
        """)
        
        quick_key = st.text_input(
            "OpenAI API Key 입력",
            type="password",
            placeholder="sk-proj-...",
            help="입력한 키는 현재 세션에만 임시 보관되며 서버에 영구 저장되지 않습니다."
        )
        if st.button("✅ API Key 등록하고 대화 시작하기", type="primary"):
            if quick_key.strip():
                st.session_state.api_key = quick_key.strip()
                st.success("API Key가 성공적으로 등록되었습니다!")
                st.rerun()
            else:
                st.error("유효한 API Key를 입력해주세요.")
        return

    # 5. 세션당 100턴 도달 여부 알림
    if is_limit_reached:
        st.error(f"""
        ⚠️ **본 세션의 최대 대화 수({chat_db.MAX_TURNS_PER_SESSION}턴)에 도달했습니다.**  
        대화 품질과 시스템 자원 관리를 위해 더 이상의 메시지를 보낼 수 없습니다.  
        새로운 질문을 계속하시려면 사이드바의 **'➕ 새 대화 시작'** 버튼을 클릭해주세요!
        """)

    # 6. 이전 대화 메시지 출력
    current_messages = chat_db.get_session_messages(current_sid)
    for msg in current_messages:
        with st.chat_message(msg["role"]):
            role_label = "👤 사용자" if msg["role"] == "user" else "🤖 AI 어시스턴트"
            st.caption(f"{role_label} • {msg['created_at']}")
            st.markdown(msg["content"])

    # 7. 하단 채팅 입력창 (100턴 초과 시 비활성화)
    chat_disabled = is_limit_reached
    user_prompt = st.chat_input(
        "AI에게 보낼 메시지를 입력하세요..." if not chat_disabled else "최대 100턴에 도달하여 입력이 제한되었습니다.",
        disabled=chat_disabled,
        key="chat_input_prompt"
    )

    # 8. 사용자 입력 처리 및 OpenAI 응답 스트리밍
    if user_prompt:
        # 사용자 메시지 화면 출력
        with st.chat_message("user"):
            st.caption("👤 사용자 • 방금 전")
            st.markdown(user_prompt)

        # 사용자 메시지 SQLite 저장
        chat_db.save_message(
            session_id=current_sid,
            role="user",
            content=user_prompt
        )

        # 첫 질문인 경우 세션 제목을 질문 요약으로 자동 갱신
        if len(current_messages) == 0:
            short_title = user_prompt[:25] + ("..." if len(user_prompt) > 25 else "")
            chat_db.update_session_title(current_sid, short_title)

        # 순수 텍스트 OpenAI 대화 페이로드 구성
        api_messages = [
            {"role": "system", "content": st.session_state.get("system_prompt", "당신은 친절하고 명확한 답변을 제공하는 지적인 AI 어시스턴트입니다.")}
        ]
        for prev in current_messages:
            api_messages.append({"role": prev["role"], "content": prev["content"]})
        api_messages.append({"role": "user", "content": user_prompt})

        # OpenAI 클라이언트 호출 및 스트리밍 답변 렌더링
        client = OpenAI(api_key=current_api_key)
        selected_model = st.session_state.get("selected_model", "gpt-5.5")

        try:
            with st.chat_message("assistant"):
                st.caption("🤖 AI 어시스턴트 • 응답 중...")
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=api_messages,
                    stream=True
                )
                assistant_response = st.write_stream(stream)

            # AI 답변 SQLite 저장
            chat_db.save_message(
                session_id=current_sid,
                role="assistant",
                content=assistant_response
            )

            # 정상 응답 및 DB 저장 완료 시에만 화면 갱신
            st.rerun()

        except Exception as err:
            err_str = str(err)
            if "Incorrect API key" in err_str or "invalid_api_key" in err_str or "401" in err_str:
                st.error("""
                ### 🔑 OpenAI API Key 인증 실패 (401 Unauthorized)
                등록된 OpenAI API Key가 올바르지 않거나 만료되었습니다.  
                좌측 사이드바의 **OpenAI API Key 등록/변경** 입력창에 현재 유효한 API Key(`sk-...`)를 입력한 후 다시 질문해주세요.
                """)
            elif "does not exist" in err_str or "model_not_found" in err_str or "404" in err_str:
                st.error(f"""
                ### 🧠 모델 접근 오류 (404 Not Found)
                선택하신 모델(`{selected_model}`)은 현재 OpenAI 계정에서 지원되지 않거나 API 접근 권한이 없습니다.  
                사이드바에서 다른 모델을 선택하시거나 계정 권한을 확인해주세요.
                """)
            elif "rate_limit" in err_str or "quota" in err_str or "429" in err_str:
                st.error("""
                ### ⏳ API 사용 한도 초과 또는 잔액 부족 (429 Rate Limit)
                OpenAI 계정의 크레딧 잔액이 부족하거나 일시적인 분당 요청 한도에 도달했습니다.  
                OpenAI 플랫폼 대시보드에서 크레딧 잔액 및 결제 수단을 확인해주세요.
                """)
            else:
                st.error(f"❌ OpenAI API 호출 중 오류가 발생했습니다: {err_str}")
            # ※ 주의: 오류 발생 시에는 st.rerun()을 실행하지 않아야 사용자가 오류 내용을 확인하고 조치할 수 있습니다.


# ========================================================
# 6. app2.py 단독 실행 시 진입점
# ========================================================
if __name__ == "__main__":
    if not st.session_state.is_logged_in:
        show_login_page()
    else:
        if st.session_state.current_menu == "💬 실시간 AI 채팅":
            show_chat_page()
        else:
            show_history_page()
