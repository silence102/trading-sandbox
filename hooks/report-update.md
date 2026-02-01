# Hook: 리포트 기록 업데이트

## 트리거 요청

- "리포트 기록 업데이트해줘"
- "새 리포트 추가됐어"
- "리포트 README 업데이트해줘"

---

## 실행 흐름

```
1. [hooks/report-update.md] 읽기 (현재 문서)
      ↓
2. notes/reports/ 폴더의 PDF 파일 확인
      ↓
3. 새 파일 OCR로 읽고 주요 내용 파악
      ↓
4. 관련 파일 업데이트
```

---

## 실행 단계

### Step 1: 현재 리포트 파일 목록 확인
```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && ls notes/reports/*.pdf
```

### Step 2: README에 기록된 파일과 비교
```
notes/reports/README.md
```
- "리포트 기록 현황" 테이블에 없는 새 파일 확인

### Step 3: 새 파일 OCR로 읽기
- Read 도구로 PDF 파일 읽기
- 주요 내용 파악 (날짜, 리포트 종류, 핵심 키워드)

### Step 4: 파일 업데이트

| 파일 | 업데이트 내용 |
|------|-------------|
| `notes/reports/README.md` | 리포트 기록 현황 테이블에 새 파일 추가 |
| `README.md` (메인) | 리포트 분석 현황 (파일 개수, 날짜 범위) 업데이트 |

---

## 업데이트 형식

### notes/reports/README.md - 리포트 기록 현황
```markdown
| `YY-MM-DD~DD_기록.pdf` | MM/DD~DD | 주요 내용 요약 |
```

### README.md (메인) - 진행 중 항목
```markdown
- [ ] 한국투자증권 리포트 분석 및 기록 (N개 파일, MM/DD~MM/DD)
```

---

## 작업 디렉토리

모든 명령은 아래 경로에서 실행:
```
c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox
```

---

*마지막 업데이트: 2026년 2월 1일*
