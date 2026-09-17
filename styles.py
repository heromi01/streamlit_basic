import streamlit as st

def apply_custom_css():
    """모던하고 세련된 미니멀 SaaS 테마 CSS를 앱 전역에 주입합니다."""
    st.markdown(
        """
        <style>
        /* ========================================================
           1. 폰트 및 전역 기본 스타일
           ======================================================== */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        html, body, [class*="css"] {
            font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
            letter-spacing: -0.01em;
        }

        /* 메인 컨테이너 상단 여백 최적화 */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1080px;
        }

        /* ========================================================
           2. 모던 헤더 & 브랜딩 뱃지
           ======================================================== */
        .app-brand-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.25rem;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid rgba(128, 128, 128, 0.15);
        }

        .brand-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(99, 102, 241, 0.1);
            color: #6366f1;
            border: 1px solid rgba(99, 102, 241, 0.25);
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 8px #10b981;
        }

        /* ========================================================
           3. 카드 컨테이너 & 박스 디자인
           ======================================================== */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            border-radius: 12px !important;
            border: 1px solid rgba(128, 128, 128, 0.18) !important;
            background: rgba(255, 255, 255, 0.02) !important;
            backdrop-filter: blur(8px);
            transition: all 0.2s ease-in-out;
        }

        /* ========================================================
           4. 세련된 메트릭/KPI 카드
           ======================================================== */
        [data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.05);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.12);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
        }

        [data-testid="stMetricLabel"] p {
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #888888 !important;
        }

        [data-testid="stMetricValue"] div {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #6366f1 !important;
        }

        /* ========================================================
           5. 첨부 파일 태그 칩 (Tag Chip)
           ======================================================== */
        .chip-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 6px;
            margin-bottom: 10px;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 500;
        }

        /* ========================================================
           6. 사이드바 정돈 및 슬림 스크롤바
           ======================================================== */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.15);
        }

        /* 불필요하게 굵은 기본 구분선 최소화 */
        hr {
            margin: 1.25rem 0 !important;
            border-color: rgba(128, 128, 128, 0.15) !important;
        }

        /* 버튼 hover 애니메이션 및 곡률 */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            border-color: #6366f1 !important;
            color: #6366f1 !important;
        }

        /* Primary 버튼 강조 */
        .stButton > button[kind="primary"] {
            background-color: #6366f1 !important;
            border-color: #6366f1 !important;
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #4f46e5 !important;
            border-color: #4f46e5 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
