# GitHub Issue 작업 로그 자동화

> 작업 완료 후 GitHub Issue에 로그를 자동 등록하는 절차

## 트리거 요청

사용자가 다음과 같이 요청하면 이 문서를 참고하여 실행합니다:

- "오늘 작업 이슈 로그 등록해줘"
- "작업 로그 등록해줘"
- "이슈 로그 업데이트해줘"

---

## 실행 절차

### Step 1: 작업 디렉토리 이동

모든 명령은 아래 경로에서 실행해야 합니다:
```
c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox
```

### Step 2: 현재 월의 이슈 번호 확인

아래 테이블에서 현재 월에 해당하는 이슈 번호를 확인합니다.

#### 월별 로그 이슈

| 월 | 이슈 번호 | URL |
|----|----------|-----|
| 2026년 1월 | **#1** | https://github.com/silence102/trading-sandbox/issues/1 |
| 2026년 2월 | **#2** | https://github.com/silence102/trading-sandbox/issues/2 |

### Step 3: 새 월인 경우 이슈 생성

해당 월의 이슈가 테이블에 없으면 새 이슈를 생성합니다:

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && gh issue create --title "📋 작업 로그 (YYYY년 M월)" --body "YYYY년 M월 프로젝트 진행 상황을 기록합니다." --label "log"
```

생성 후 이 문서의 "월별 로그 이슈" 테이블에 새 이슈 정보를 추가합니다.

### Step 4: 오늘 커밋 내역 확인

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && git log --oneline --since="midnight"
```

### Step 5: 작업 로그 코멘트 등록

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && gh issue comment [이슈번호] --body "[작업 내용]"
```

---

## 코멘트 작성 형식

```markdown
## YYYY-MM-DD

### 완료 항목
- 대화에서 수행한 작업 요약 1
- 대화에서 수행한 작업 요약 2

### 커밋
- `커밋해시` 커밋 메시지 1
- `커밋해시` 커밋 메시지 2

### 추가된 파일 (선택)
- `파일 경로` - 설명
```

---

## 예시

### 2월 작업 로그 등록 예시

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && gh issue comment 2 --body "## 2026-02-01

### 완료 항목
- 리포트 기록 현황 업데이트
- 증권사 API 비교 분석 문서 작성
- GitHub Issue 자동화 가이드 작성

### 커밋
- \`e1d2b8b\` docs: GitHub Issue 자동화 가이드 추가
- \`657eee8\` docs: API 및 트레이딩 시스템 비교 분석 문서 추가"
```

---

## 관련 명령어

| 용도 | 명령어 |
|------|--------|
| 이슈 목록 보기 | `gh issue list` |
| 특정 이슈 보기 | `gh issue view [번호]` |
| 이슈 제목 변경 | `gh issue edit [번호] --title "새 제목"` |
| 이슈 닫기 | `gh issue close [번호]` |

---

## 레포지토리 정보

- **레포지토리**: silence102/trading-sandbox
- **라벨**: `log` (작업 로그용)

---

*마지막 업데이트: 2026년 2월 1일*
