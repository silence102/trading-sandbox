# Hook: 마켓 브리핑 생성

## 트리거 요청

- "모닝 브리핑 생성해줘" → morning 타입
- "애프터 마켓 브리핑 생성해줘" → aftermarket 타입
- "오늘 시장 브리핑 생성해줘" → 시간대에 따라 자동 판단
- "마켓 브리핑 만들어줘" → 시간대에 따라 자동 판단

---

## 브리핑 유형

| 유형 | 시간 | 목적 | 데이터 기준 |
|------|------|------|------------|
| **모닝 브리핑** | 08:00 KST | 장 시작 전 투자 준비 | 전일 데이터 |
| **애프터 마켓 브리핑** | 18:00 KST | 장 마감 후 시장 요약 | 금일 데이터 |

---

## 실행 방법

### 모닝 브리핑 (장 시작 전)
```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
python scripts/main.py --type morning
```

### 애프터 마켓 브리핑 (장 마감 후)
```bash
python scripts/main.py --type aftermarket
```

### AI 분석 포함
```bash
python scripts/main.py --type morning --ai
python scripts/main.py --type aftermarket --ai
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
notes/daily_briefing/
├── YYYY-MM-DD_모닝브리핑.md
└── YYYY-MM-DD_애프터마켓브리핑.md
```

---

## Claude 실행 절차

1. 사용자의 요청이 모닝/애프터마켓 중 어느 타입인지 판단
   - 명시적으로 지정한 경우 해당 타입 사용
   - 지정하지 않은 경우: 현재 시간이 12:00 KST 이전이면 morning, 이후이면 aftermarket
2. 해당 타입으로 bash 명령어 실행
3. 생성된 브리핑 파일 내용 사용자에게 요약 전달
4. 파일 경로 안내

---

## GitHub Actions 자동 실행

매일 **08:00 모닝** / **18:00 애프터마켓** (KST) 자동 생성

### 현재 상태: **OFF** (기본값)

### 활성화 방법
1. GitHub 저장소 → Settings → Secrets and variables → Actions
2. **Variables** 탭 클릭
3. `BRIEFING_ENABLED` = `true` 추가

### 수동 실행
Actions 탭 → Daily Market Briefing → Run workflow → 브리핑 유형 선택

---

*마지막 업데이트: 2026년 2월 9일*
