# Hook: 실시간 시장 확인

## 트리거 요청

- "지금 KOSPI 시세 확인해줘"
- "현재 시장 상황 알려줘"
- "오늘 증시 어때?"
- "관심종목 시세 확인해줘"

---

## 실행 흐름

```
1. [hooks/market-check.md] 읽기 (현재 문서)
      ↓
2. scripts/main.py --test [항목] 실행
      ↓
3. 결과를 사용자에게 즉시 전달
```

---

## 실행 방법

### 시세 확인 (KRX)
```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
python scripts/main.py --test krx
```

### 뉴스 확인
```bash
python scripts/main.py --test news
```

### 전체 상태 확인
```bash
python scripts/main.py --status
```

---

## 조회 가능 항목

| 명령어 | 조회 내용 |
|--------|----------|
| `--test krx` | KOSPI/KOSDAQ 지수, 관심종목 시세 |
| `--test news` | 최근 투자 관련 뉴스 |
| `--test dart` | 최근 공시 (API 키 필요) |
| `--test ecos` | 금리, 환율 (API 키 필요) |
| `--status` | 전체 API 연결 상태 |

---

## Claude 실행 절차

1. 사용자 요청에 맞는 명령어 실행
2. 결과를 정리하여 사용자에게 전달
3. 필요시 추가 분석 제공

---

*마지막 업데이트: 2026년 2월 4일*
