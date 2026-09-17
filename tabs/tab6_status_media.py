import streamlit as st
import time

# ========================================================
# 6. 상태 알림, 피드백, 미디어 요소 모듈 세부 함수들
# ========================================================

def render_status_alerts_metrics():
    """핵심 지표 카드 및 상태 알림 박스 4총사"""
    st.subheader("1. 핵심 지표 & 상태 알림 (Metrics & Alerts)")
    st.markdown("매출/방문자 지표와 상황별 상태 알림 박스입니다.")

    # (1) 핵심 지표 카드
    st.markdown("#### (1) 핵심 지표 카드 (`st.metric`)")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="오늘 방문자 수", value="1,240명", delta="120명 (증가)")
    col2.metric(label="총 매출액", value="3,500,000원", delta="-250,000원 (감소)")
    col3.metric(label="고객 만족도", value="98.5%", delta="1.2%")

    st.divider()

    # (2) 상태 알림 박스 4총사 (UI 컴포넌트 예시)
    st.markdown("#### (2) 상태 피드백 알림 박스 4총사 (UI 디자인 컴포넌트)")
    st.caption("상황에 맞는 색상과 아이콘으로 직관적인 상태 메시지를 렌더링하는 UI 컴포넌트들입니다.")
    st.success("성공(Success): 작업이 정상적으로 완료되었습니다! (`st.success`)", icon="✅")
    st.info("정보(Info): 새로운 기능 업데이트가 적용되었습니다. (`st.info`)", icon="ℹ️")
    st.warning("경고(Warning): 입력값 형식을 다시 확인해주세요. (`st.warning`)", icon="⚠️")
    st.error("오류 알림 컴포넌트 예시(Error): 실제 오류가 아니며, 오류 상황을 사용자에게 알릴 때 사용하는 UI 상자입니다. (`st.error`)", icon="🚨")



def render_animations_progress():
    """축하 애니메이션, 프로그레스 바, 스피너, 토스트 알림"""
    st.subheader("2. 애니메이션 & 진행 피드백 (Animation & Progress)")
    st.markdown("사용자 상호작용 피드백, 진행률 표시 및 팝업 토스트 알림입니다.")

    # (1) 축하 애니메이션 2종
    st.markdown("#### (1) 축하 애니메이션 (`st.balloons`, `st.snow`)")
    col_ani1, col_ani2 = st.columns(2)
    if col_ani1.button("🎈 풍선 날리기 효과", key="tab6_btn_balloons"):
        st.balloons()
    if col_ani2.button("❄️ 눈 내리기 효과", key="tab6_btn_snow"):
        st.snow()

    st.divider()

    # (2) 로딩 스피너 및 진행률 바
    st.markdown("#### (2) 로딩 스피너 및 진행률 바 (`st.progress`, `st.spinner`)")
    if st.button("작업 시뮬레이션 시작", key="tab6_btn_progress"):
        with st.spinner("데이터를 처리하는 중입니다..."):
            progress_bar = st.progress(0)
            for percent in range(1, 101):
                time.sleep(0.01)
                progress_bar.progress(percent)
        st.success("데이터 처리가 성공적으로 완료되었습니다! 👏")

    st.divider()

    # (3) 토스트 알림
    st.markdown("#### (3) 토스트 알림 (`st.toast`)")
    if st.button("토스트 알림 띄우기", key="tab6_btn_toast"):
        st.toast("우측 하단 토스트 알림이 성공적으로 전송되었습니다!", icon="🚀")


def render_feedback_media():
    """컬러 피커, 별점/표정 피드백, 미디어 이미지"""
    st.subheader("3. 평점 피드백 & 미디어 (Feedback & Media)")
    st.markdown("색상 선택기, 별점/표정 평가, 고화질 이미지 렌더링입니다.")

    # (1) 색상 선택기
    st.markdown("#### (1) 색상 선택기 (`st.color_picker`)")
    picked_color = st.color_picker("원하는 색상을 골라보세요", value="#0066CC", key="tab6_color")
    st.write(f"선택된 색상 코드: **{picked_color}**")
    st.markdown(
        f"<div style='background-color: {picked_color}; width: 100%; height: 35px; border-radius: 6px;'></div>",
        unsafe_allow_html=True
    )

    st.divider()

    # (2) 별점 및 감정 피드백
    st.markdown("#### (2) 별점 및 감정 피드백 (`st.feedback`)")
    star_rating = st.feedback("stars", key="tab6_feedback_stars")
    st.write(f"부여한 별점 점수: **{star_rating}**점")

    face_rating = st.feedback("faces", key="tab6_feedback_faces")
    st.write(f"감정 반응 인덱스: **{face_rating}**")

    st.divider()

    # (3) 미디어 이미지
    st.markdown("#### (3) 미디어 요소 (`st.image`)")
    sample_image_url = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=800&auto=format&fit=crop"
    # width="stretch"로 부모 컨테이너 너비에 맞춤 (Streamlit 최신 권장 규격)
    st.image(sample_image_url, caption="Unsplash 무료 고화질 이미지 예시", width="stretch")


def render_tab6():
    """전체 렌더링 호환 함수"""
    render_status_alerts_metrics()
    st.divider()
    render_animations_progress()
    st.divider()
    render_feedback_media()
