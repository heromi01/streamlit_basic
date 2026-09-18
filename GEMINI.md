# 프로젝트 개발 규칙 (Streamlit Basic)

## 1. 코드 간결성 및 학습 우선 원칙 (Simplicity First)
- **복잡한 예외 처리 및 방어 코드 지양**:
  - `try-except`, 과도한 `None`/타입 검사, 복잡한 유효성 검사 등 코드를 복잡하게 만드는 로직은 작성하지 않습니다.
  - 초보자가 직관적으로 이해하고 따라 할 수 있도록 가장 쉽고 간단한 문법과 구조를 유지합니다.

## 2. 주석 및 마크다운 설명 작성 원칙
- **코드 라인별 주석**:
  - 주요 함수, 위젯 파라미터(옵션), 변수의 역할에 대해 `#` 주석으로 명확하고 친절하게 설명합니다.
- **화면 마크다운 설명**:
  - Streamlit 화면에도 `st.markdown()`, `st.caption()` 등을 활용하여 각 컴포넌트의 사용 목적과 기능 설명을 함께 렌더링합니다.

## 3. 공식 문서(API Reference) 기반 코드 작성 원칙
- **공식 API 문서 필수 참고**:
  - Streamlit 공식 API 문서([Streamlit API Reference](https://docs.streamlit.io/develop/api-reference)) 및 각 요소별 세부 페이지를 최우선으로 참고하여 예시 코드를 작성합니다.
  - 사용자가 특정 요소나 기능에 대한 코드 작성을 요청하면 공식 문서의 권장 용례, 최신 파라미터 규격, 권장 디자인 패턴을 반영하여 코드를 구성합니다.

## 4. Apple 인터페이스 디자인 및 모션 원칙 (Apple-Style Design & Motion Principles)
*참조 문서: `C:\pjt_hr\대시보드 배경 애니메이션 제작\apple-design-principles.md`*

- **소재와 깊이감 (Materials & Translucency)**:
  - 내비게이션 바, 툴바, 사이드바, 카드 컨테이너에 프로스티드 글래스(`backdrop-filter: blur(20px~30px) saturate(160%~180%)`)를 적용하여 배경 콘텐츠와 애니메이션이 은은하게 투과되도록 구성합니다.
  - 1px 반투명 헤어라인 보더(`rgba(255, 255, 255, 0.15~0.6)`)와 다층 앰비언트 그림자(`box-shadow`)로 물리적 두께감을 형성합니다.
- **즉각적인 반응과 스프링 모션 (Zero-Latency & Springs)**:
  - 포인터/손가락이 닿는 즉시 반응하는 무지연 피드백을 기본으로 합니다. (버튼, 카드 터치다운 시 `:active { transform: scale(0.96~0.97); }`)
  - 인위적이고 딱딱한 고정 시간 애니메이션 대신, 임계 감쇠(Critically Damped, damping 1.0) 또는 미세 탄성(damping 0.8) 스프링 커브(`cubic-bezier(0.25, 1, 0.5, 1)`)를 적용합니다.
  - 모든 모션은 조작 도중 방향을 바꾸거나 중단할 수 있는 인터럽터블(Interruptible) 상태를 유지합니다.
- **광학적 타이포그래피 (Optical Typography)**:
  - 시스템 폰트(`-apple-system, BlinkMacSystemFont, "SF Pro", "Pretendard"`)를 최우선 적용합니다.
  - 폰트 크기별 자간(Tracking) 차등화: 대형 디스플레이 타이틀은 타이트한 음수 자간(`-0.03em ~ -0.035em`), 본문은 `normal`, 캡션은 미세한 양수 자간을 적용합니다.
  - 폰트 크기별 행간(Leading) 차등화: 대제목은 타이트하게(`1.1 ~ 1.25`), 본문은 편안한 가독성(`1.5 ~ 1.65`)을 유지합니다.
- **접근성 및 모션 절제 (Accessibility & Reduced Motion)**:
  - `@media (prefers-reduced-motion: reduce)` 대응 (슬라이드/스프링 대신 짧은 불투명도 크로스페이드 처리)
  - `@media (prefers-reduced-transparency: reduce)` 대응 (블러 제거, 불투명도 상향)
  - 다크 모드(`@media (prefers-color-scheme: dark)`) 자동 지원

