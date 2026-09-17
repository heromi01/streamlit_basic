# ⚡ Streamlit AI Studio & 위젯 랩 (Streamlit Basic)

Streamlit의 핵심 위젯을 실습할 수 있는 **인터랙티브 가이드**와 OpenAI 최신 모델(GPT-5.5+) 및 SQLite 영구 저장을 연동한 **멀티모달 AI 챗봇**을 통합 제공하는 올인원 웹 애플리케이션입니다.

---

## ✨ 주요 특징 & 리팩토링 개선 사항

- **단일 통합 내비게이션**:
  - 화면마다 분산되어 있던 중복 이동 버튼, 다운로드 링크를 완전히 제거하고 **사이드바 단일 내비게이션**으로 직관적인 화면 전환을 제공합니다.
- **모던 프리미엄 SaaS UI**:
  - 딥 슬레이트 & 인디고 포인트 컬러 기반 커스텀 디자인 시스템(`styles.py`) 적용
  - 불필요한 구분선(`st.divider`)을 걷어내고 부드러운 카드 섀도우, 세련된 KPI 메트릭 카드, 태그 칩(Chip) UI 구축
- **멀티모달 AI 비전 & 파일 첨부**:
  - 드래그 앤 드롭 지원 모달 팝업 및 컴팩트 툴바를 통한 이미지/문서 파일 분석
- **SQLite 영구 보관 & 분석**:
  - 세션별 전체 대화 및 첨부 미디어 자동 저장, 키워드 검색, 마크다운(.md) 단일 원클릭 내보내기

---

## 📂 프로젝트 구성

```text
streamlit_basic/
├── app.py               # ⚡ [메인 통합 포털] AI 챗봇 + 히스토리 + 관리자 분석실 + 위젯 랩
├── app2.py              # 🤖 OpenAI 멀티모달 AI 챗봇 (미니 세션 현황판 내장)
├── app2_history.py      # 📜 대화 히스토리 대시보드
├── admin_analytics.py   # 📈 [신규] 관리자 통계 분석실 (일자별 차트/발화비율/세션 관리)
├── styles.py            # 🎨 모던 프리미엄 테마 & 커스텀 CSS 모듈
├── chat_db.py           # 🗄️ SQLite 기반 대화 세션 및 통계 관리 모듈
├── tabs/                # 📚 위젯 랩 기능별 모듈
│   ├── group_inputs.py
│   ├── group_layouts.py
│   ├── group_visualizations.py
│   ├── group_status_media.py
│   └── ...
├── run.bat              # 원클릭 통합 앱 실행 배치 파일
├── .env.example         # OpenAI API 키 환경 변수 템플릿
├── pyproject.toml       # 패키지 의존성 정의 (uv)
└── uv.lock              # 패키지 잠금 파일
```

---

## 🚀 빠른 시작

### 1. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 본인의 OpenAI API 키를 입력합니다.
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 패키지 동기화 및 실행 (`uv` 권장)
```bash
# 의존성 패키지 동기화
uv sync

# [통합 포털 실행] 챗봇, 히스토리, 위젯 랩을 한 곳에서 실행
uv run streamlit run app.py

# 또는 배치 파일 실행
run.bat
```

> **단독 실행 지원**: 특정 화면만 독립적으로 띄우고 싶은 경우 아래 명령어로도 실행할 수 있습니다.
> - AI 챗봇 단독: `uv run streamlit run app2.py`
> - 대화 히스토리 단독: `uv run streamlit run app2_history.py`
