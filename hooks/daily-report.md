# 일일 리서치 리포트 자동 생성

> 한국투자증권 리서치 리포트를 자동으로 크롤링하고 요약합니다.

## 트리거 요청

사용자가 다음과 같이 요청하면 이 문서를 참고하여 실행합니다:

- "오늘 리서치 리포트 요약해줘"
- "일일 리포트 생성해줘"
- "리서치 리포트 크롤링해줘"

---

## 실행 방법

### 방법 1: 전체 파이프라인 실행

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
python scripts/main.py
```

### 방법 2: 특정 날짜 리포트 생성

```bash
python scripts/main.py --date 2026-02-02
```

### 방법 3: 단계별 실행

```bash
# 1. 크롤링만
python scripts/report_crawler.py --date 2026-02-02

# 2. PDF 추출만
python scripts/pdf_extractor.py

# 3. 요약만
python scripts/report_summarizer.py --date 2026-02-02
```

### 방법 4: 스케줄러 (매일 자동)

```bash
python scripts/main.py --schedule
```

---

## 사전 준비

### 1. 의존성 설치

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
pip install -r requirements.txt
```

### 2. API 키 설정

`.env` 파일 생성 (.env.example 참고):

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 3. Chrome 브라우저

크롤러가 Chrome을 사용하므로 Chrome 브라우저가 설치되어 있어야 합니다.

---

## 파이프라인 흐름

```
1. [크롤링] 리서치 페이지 접속 → 리포트 목록 파싱 → PDF 다운로드
        ↓
2. [추출] PDF → 텍스트 변환 (PyMuPDF)
        ↓
3. [요약] Claude API로 종합 분석 → Markdown 리포트 생성
        ↓
4. [저장] notes/auto_reports/YYYY-MM-DD_종합리포트.md
```

---

## 출력 경로

| 단계 | 경로 | 설명 |
|------|------|------|
| PDF 원본 | `notes/auto_reports/` | 다운로드된 PDF 파일 |
| 추출 텍스트 | `notes/auto_reports/` | PDF에서 추출된 텍스트 (.txt) |
| 종합 리포트 | `results/daily_reports/` | Claude 요약 결과 |
| 요약 가이드 | `results/daily_reports/summary_prompt_guide.md` | 프롬프트 커스터마이즈 |
| 실행 로그 | `logs/` | 파이프라인 실행 로그 |

---

## 옵션

| 옵션 | 설명 |
|------|------|
| `--date YYYY-MM-DD` | 특정 날짜 지정 |
| `--skip-crawl` | 크롤링 스킵 (기존 PDF 사용) |
| `--skip-extract` | 추출 스킵 (기존 텍스트 사용) |
| `--schedule` | 스케줄러 모드 (매일 08:00) |

---

## 주의사항

- 리포트 원본의 저작권은 한국투자증권에 있습니다
- 개인 학습 목적으로만 사용하세요
- 과도한 크롤링을 방지하기 위해 요청 간 딜레이가 적용됩니다

---

*마지막 업데이트: 2026년 2월 2일*
