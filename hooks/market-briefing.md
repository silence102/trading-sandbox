# Hook: 마켓 브리핑 생성

## 트리거 요청

- "오늘 시장 브리핑 생성해줘"
- "마켓 브리핑 만들어줘"
- "일일 브리핑 생성해줘"

---

## 실행 흐름

```
1. [hooks/market-briefing.md] 읽기 (현재 문서)
      ↓
2. scripts/main.py 실행
      ↓
3. 데이터 수집 (KRX, 뉴스 RSS, DART, ECOS)
      ↓
4. 브리핑 파일 생성 → results/daily_briefing/
```

---

## 실행 방법

### 기본 브리핑 (AI 분석 없이)
```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
python scripts/main.py
```

### AI 분석 포함 브리핑
```bash
python scripts/main.py --ai
```

---

## 수집 데이터

| 소스 | 내용 | API 키 필요 |
|------|------|------------|
| PyKRX | KOSPI/KOSDAQ 지수, 관심종목 시세 | 불필요 |
| 뉴스 RSS | 한국경제, 매일경제 등 투자 뉴스 | 불필요 |
| DART | 기업 공시 | 필요 |
| ECOS | 금리, 환율 등 경제지표 | 필요 |

---

## 결과물 위치

```
results/daily_briefing/
└── YYYY-MM-DD_마켓브리핑.md
```

---

## Claude 실행 절차

1. 위 bash 명령어 실행
2. 생성된 브리핑 파일 내용 사용자에게 요약 전달
3. 파일 경로 안내

---

## GitHub Actions 자동 실행

매일 18:00 (KST)에 자동으로 브리핑을 생성하고 저장소에 커밋합니다.

### 현재 상태: **OFF** (기본값)

### 활성화 방법
1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. **Variables** 탭 클릭
3. `BRIEFING_ENABLED` = `true` 추가

### API 키 설정 (선택)
Secrets 탭에서 추가:
- `DART_API_KEY`: DART 공시 수집용
- `ECOS_API_KEY`: 한국은행 경제지표용

### 수동 실행
Actions 탭 → Daily Market Briefing → Run workflow → `force_run: true` 선택

---

*마지막 업데이트: 2026년 2월 4일*
