# Hook: 이슈 로그 등록

## 트리거 요청

- "오늘 작업 이슈 로그 등록해줘"
- "작업 로그 등록해줘"
- "이슈 로그 업데이트해줘"

---

## 실행 흐름

```
1. [hooks/issue-log.md] 읽기 (현재 문서)
      ↓
2. [automation/github-issue-log.md] 참조하여 작업 실행
      ↓
3. 작업 완료 후 아래 파일 업데이트
```

---

## 참조 문서

- **작업 절차**: `automation/github-issue-log.md`

---

## 실행 단계

### Step 1: 작업 절차 문서 읽기
```
automation/github-issue-log.md
```

### Step 2: 절차에 따라 작업 실행
1. 현재 월의 이슈 번호 확인
2. 새 월이면 이슈 생성
3. 오늘 커밋 내역 확인
4. 이슈에 로그 코멘트 등록

### Step 3: 작업 완료 후 업데이트할 파일

| 파일 | 업데이트 내용 | 조건 |
|------|-------------|------|
| `automation/github-issue-log.md` | 월별 로그 이슈 테이블에 새 이슈 추가 | 새 월 이슈 생성 시 |

---

## 작업 디렉토리

모든 명령은 아래 경로에서 실행:
```
c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox
```

---

*마지막 업데이트: 2026년 2월 1일*
