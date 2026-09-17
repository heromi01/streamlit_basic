import streamlit as st

# ========================================================
# 1. 텍스트 입력 & 코드/수식 표시 모듈
# ========================================================
def render_tab1():
    """사용자 텍스트 입력 및 코드/수식 표시 컴포넌트 모음"""
    st.subheader("1. 텍스트 입력 & 표시 (Text, Code & LaTeX)")
    st.markdown("사용자로부터 한 줄 또는 여러 줄의 문자열을 입력받는 위젯과 프로그래밍 코드, 수학 수식 렌더링입니다.")

    # (1) 기본 한 줄 텍스트 입력
    st.markdown("#### (1) 기본 한 줄 텍스트 입력 (`st.text_input`)")
    st.caption("가장 기본적인 한 줄 입력창입니다. `value` 옵션으로 기본값을 미리 지정합니다.")
    # label: 안내 텍스트, value: 초기 기본값
    user_name = st.text_input("이름을 입력하세요", value="홍길동", key="tab1_name")
    st.write(f"입력된 이름: **{user_name}**")

    st.divider()

    # (2) 힌트(플레이스홀더) 및 글자 수 제한
    st.markdown("#### (2) 힌트 문구와 글자 수 제한")
    st.caption("`placeholder`로 입력 예시를 흐리게 보여주고, `max_chars`로 최대 입력 글자 수를 제한합니다.")
    # placeholder: 힌트 문구, max_chars: 최대 글자 수
    user_nickname = st.text_input(
        "닉네임 입력 (최대 6글자)",
        placeholder="예: 파이썬러버",
        max_chars=6,
        key="tab1_nickname"
    )
    st.write(f"설정된 닉네임: **{user_nickname}**")

    st.divider()

    # (3) 비밀번호 마스킹 입력
    st.markdown("#### (3) 비밀번호 마스킹 입력 (`type='password'`)")
    st.caption("`type='password'` 옵션을 지정하면 입력한 글자가 점이나 별표로 가려집니다.")
    # type="password": 문자 숨김 처리 옵션
    user_password = st.text_input("비밀번호를 입력하세요", type="password", key="tab1_pw")
    st.write(f"입력된 비밀번호 길이: **{len(user_password)}**자리")

    st.divider()

    # (4) 여러 줄 장문 텍스트 입력
    st.markdown("#### (4) 여러 줄 장문 텍스트 입력 (`st.text_area`)")
    st.caption("자기소개, 리뷰, 메모 등 줄바꿈이 필요한 긴 문장은 `st.text_area`를 사용합니다.")
    # height: 세로 높이, placeholder: 입력 안내 문구
    user_bio = st.text_area(
        "자기소개",
        placeholder="간단한 자기소개를 여러 줄로 자유롭게 입력해보세요.",
        height=100,
        key="tab1_bio"
    )
    st.write("작성된 자기소개 내용:")
    st.markdown(f"> {user_bio}")

    st.divider()

    # (5) 코드 블록 표시 및 복사 기능
    st.markdown("#### (5) 프로그래밍 코드 표시 (`st.code`)")
    st.caption("구문 강조(Syntax Highlighting)와 우측 상단 원클릭 복사 버튼을 제공합니다.")
    sample_python_code = '''def hello_streamlit():
    message = "Streamlit 공식 문서를 탐구 중입니다!"
    return message

print(hello_streamlit())'''
    # language="python": 파이썬 구문 강조 적용
    st.code(sample_python_code, language="python")

    st.divider()

    # (6) 수학 수식 렌더링
    st.markdown("#### (6) 수학 수식 렌더링 (`st.latex`)")
    st.caption("LaTeX 수식 문법을 지원하여 복잡한 수학 공식을 깔끔하게 화면에 띄웁니다.")
    # st.latex: LaTeX 수식 표기
    st.latex(r"E = mc^2")
    st.latex(r"\sigma(z) = \frac{1}{1 + e^{-z}}")

