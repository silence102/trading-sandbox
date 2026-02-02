# 리서치 리포트 자동화 가이드

> 한국투자증권 리서치 리포트를 자동으로 수집하고 AI로 요약하는 시스템

---

## 한눈에 보기

```
┌─────────────────────────────────────────────────────────────────┐
│                    리서치 리포트 자동화 파이프라인                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [1. 크롤링]          [2. 추출]           [3. 요약]             │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│   │ 한투    │  ───▶   │  PDF    │  ───▶   │ Claude  │          │
│   │ 웹사이트 │  PDF    │  텍스트  │  텍스트  │   API   │          │
│   └─────────┘         └─────────┘         └─────────┘          │
│        │                   │                   │                │
│        ▼                   ▼                   ▼                │
│  notes/auto_reports/  notes/auto_reports/  results/daily_reports/
│   (PDF + 텍스트)       (PDF + 텍스트)       (AI 요약)            │
│                                                                 │
│   ✅ API 키 불필요     ✅ API 키 불필요    ⚠️ API 키 필요        │
└─────────────────────────────────────────────────────────────────┘
```

---

## API 키 없이 사용 가능한 기능

| 단계 | 기능 | API 키 필요 | 설명 |
|------|------|:-----------:|------|
| **Step 1** | 크롤링 | ❌ | 리서치 페이지에서 PDF 자동 다운로드 |
| **Step 2** | PDF 추출 | ❌ | PDF → 텍스트 변환 |
| **Step 3** | AI 요약 | ⚠️ **필요** | Claude API로 종합 분석 |

**결론**: API 키 없이도 Step 1, 2는 동작합니다. 요약만 안 됩니다.

---

## 빠른 시작

### 1단계: 환경 설정

```bash
# 프로젝트 폴더로 이동
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: API 키 설정 (요약 기능 사용 시)

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 API 키 입력
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**API 키 발급 방법**:
1. https://console.anthropic.com 접속
2. 회원가입 및 결제 정보 등록
3. API Keys 메뉴에서 키 생성

### 3단계: 실행

```bash
# 전체 파이프라인 실행
python scripts/main.py

# 특정 날짜만
python scripts/main.py --date 2026-02-02

# 크롤링만 (API 키 불필요)
python scripts/report_crawler.py
```

---

## 폴더 구조

```
trading-sandbox/
├── scripts/                    # 🔧 자동화 스크립트
│   ├── main.py                # 통합 실행 (전체 파이프라인)
│   ├── report_crawler.py      # Step 1: 웹 크롤링
│   ├── pdf_extractor.py       # Step 2: PDF → 텍스트
│   └── report_summarizer.py   # Step 3: AI 요약
│
├── notes/
│   └── auto_reports/          # 📁 크롤링 결과 (PDF + 텍스트)
│       └── download_log.json  # 다운로드 기록 (중복 방지)
│
├── results/
│   └── daily_reports/         # 📊 AI 요약 결과
│       └── summary_prompt_guide.md  # 요약 프롬프트 가이드
│
├── logs/                       # 📝 실행 로그
│
├── hooks/
│   └── daily-report.md        # 🎯 트리거 문서
│
├── requirements.txt           # Python 의존성
├── .env                       # API 키 (직접 생성)
└── .env.example               # API 키 템플릿
```

---

## 사용 시나리오

### 시나리오 1: API 키 없이 PDF만 수집

```bash
# 크롤링만 실행
python scripts/report_crawler.py --date 2026-02-02

# 결과: notes/auto_reports/ 에 PDF 저장됨
```

### 시나리오 2: 이미 있는 PDF 텍스트 추출

```bash
# PDF 추출만 실행
python scripts/pdf_extractor.py

# 결과: notes/auto_reports/ 에 텍스트(.txt) 저장됨
```

### 시나리오 3: 전체 자동화 (API 키 필요)

```bash
# 전체 파이프라인
python scripts/main.py

# 결과: results/daily_reports/YYYY-MM-DD_종합리포트.md
```

### 시나리오 4: 매일 자동 실행

```bash
# 스케줄러 모드 (매일 08:00 자동 실행)
python scripts/main.py --schedule
```

---

## 트리거 (Claude 세션에서)

아래 문구로 요청하면 자동화가 실행됩니다:

- "오늘 리서치 리포트 요약해줘"
- "일일 리포트 생성해줘"
- "리서치 리포트 크롤링해줘"

→ `hooks/daily-report.md` 참조하여 실행

---

## 주의사항

### 저작권
- 리포트 원본의 저작권은 **한국투자증권**에 있습니다
- **개인 학습 목적**으로만 사용하세요
- 상업적 이용 및 재배포 금지

### 크롤링 에티켓
- 과도한 요청을 방지하기 위해 자동 딜레이 적용
- 하루 1회 정도 실행 권장

### API 비용
- Claude API는 **유료**입니다
- 토큰 사용량에 따라 과금
- 예상 비용: 리포트 3~5개 요약 시 약 $0.01~0.05

---

## 문제 해결

### "ANTHROPIC_API_KEY가 설정되지 않았습니다"
→ `.env` 파일에 API 키를 설정하세요

### 크롤링이 안 됨
→ Chrome 브라우저가 설치되어 있어야 합니다
→ 한투 웹사이트 점검 시간일 수 있습니다

### PDF 텍스트가 깨짐
→ 일부 이미지 기반 PDF는 텍스트 추출이 어려울 수 있습니다

---

## 관련 문서

- [hooks/daily-report.md](../hooks/daily-report.md) - 트리거 상세
- [results/daily_reports/summary_prompt_guide.md](../results/daily_reports/summary_prompt_guide.md) - 요약 프롬프트 커스터마이즈 가이드
- [automation/README.md](../automation/README.md) - 자동화 작업 목록
- [.env.example](../.env.example) - API 키 설정 템플릿

---

*마지막 업데이트: 2026년 2월 2일*
