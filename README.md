# Streamlit Basic & OpenAI 멀티모달 챗봇 프로젝트

Streamlit의 주요 기능과 위젯을 학습할 수 있는 종합 가이드 및 OpenAI 최신 모델(GPT-5.5+)과 SQLite 영구 저장을 연동한 멀티모달 AI 챗봇 프로젝트입니다.

---

## 📂 프로젝트 구성

```text
streamlit_basic/
├── app.py               # Streamlit 핵심 기능 & 위젯 계층형 학습 가이드
├── app2.py              # OpenAI 멀티모달 AI 챗봇 (SQLite 영구 저장 & 파일 첨부)
├── app2_history.py      # 과거 대화 히스토리 및 분석 대시보드
├── chat_db.py           # SQLite 기반 대화 세션 및 메시지 영구 저장 관리 모듈
├── tabs/                # app.py 기능별 모듈화 탭 코드
│   ├── group_inputs.py
│   ├── group_layouts.py
│   ├── group_visualizations.py
│   ├── group_status_media.py
│   └── ...
├── run.bat              # app2.py (AI 챗봇) 실행 배치 파일
├── run_basic.bat        # app.py (위젯 가이드) 실행 배치 파일
├── .env.example         # 환경 변수 템플릿 파일
├── pyproject.toml       # 프로젝트 의존성 설정 (uv)
└── uv.lock              # 의존성 잠금 파일
```

---

## 🚀 주요 기능

### 1. Streamlit 위젯 마스터 가이드 (`app.py`)
- 텍스트/코드, 선택 위젯, 숫자/날짜 위젯
- 차트 및 지도 시각화
- 2단계 계층형 탭 그룹 및 레이아웃 컨테이너
- 상태 알림, 미디어, 폼 및 챗 인터페이스

### 2. OpenAI 멀티모달 AI 챗봇 & 히스토리 대시보드 (`app2.py` / `app2_history.py`)
- **최신 OpenAI 모델 지원**: `gpt-5.5`, `gpt-5.6-sol`, `gpt-5.6-luna` 등 최신 모델군 완벽 지원
- **실시간 스트리밍 응답**: `st.write_stream` 기반 실시간 타자기 효과
- **드래그 앤 드롭 팝업 첨부**: `@st.dialog`를 활용한 이미지 및 문서 파일 모달 팝업 첨부
- **SQLite 영구 저장**: 대화 세션과 메시지, 첨부 이미지(Base64)가 로컬 DB에 자동 보관
- **과거 대화 대시보드**:
  - 세션별 전체 대화 및 과거 첨부 이미지 원본 복원
  - 대화 본문 키워드 통합 검색 및 필터링
  - 대화 통계 요약 지표 (KPI)
  - 마크다운(.md) 파일 내보내기 및 세션 삭제
- **원클릭 화면 전환**: 사이드바 라디오 메뉴 및 상단 바로가기 버튼을 통해 챗봇과 히스토리 대시보드를 자유롭게 이동

---

## ⚙️ 실행 방법

### 1. 사전 준비 (환경 변수 설정)
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 본인의 OpenAI API 키를 입력합니다.
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 패키지 설치 및 실행 (`uv` 권장)
```bash
# 의존성 설치
uv sync

# 1) OpenAI 멀티모달 AI 챗봇 실행
uv run streamlit run app2.py
# 또는 run.bat 실행

# 2) Streamlit 기본 가이드 실행
uv run streamlit run app.py
# 또는 run_basic.bat 실행
```
