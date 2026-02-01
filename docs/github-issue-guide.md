# GitHub Issue 자동화 가이드

> 작업 로그를 GitHub Issue로 간편하게 관리하는 방법

## 1. 사전 설정 (최초 1회)

### Step 1: GitHub CLI 설치

**Windows (PowerShell 관리자 권한)**
```powershell
winget install GitHub.cli
```

또는 [GitHub CLI 다운로드](https://cli.github.com/)에서 직접 설치

### Step 2: GitHub 로그인
```bash
gh auth login
```
- GitHub.com 선택
- HTTPS 선택
- 브라우저로 인증

### Step 3: 로그 이슈 생성 (최초 1회)
```bash
gh issue create --title "📋 작업 로그" --body "프로젝트 진행 상황을 기록합니다." --label "log"
```

생성된 이슈 번호를 기억해두세요 (예: #1)

---

## 2. 일일 사용법

### 작업 완료 후 로그 추가

```bash
gh issue comment 1 --body "## 2026-02-01

### 완료 항목
- docs 폴더 README 추가
- API 비교 분석 문서 작성
- 트레이딩 시스템 비교 문서 작성

### 커밋
- docs: API 및 트레이딩 시스템 비교 분석 문서 추가
- docs: docs 폴더 README 추가"
```

### 간단 버전 (한 줄)
```bash
gh issue comment 1 --body "2026-02-01: docs 폴더 구성 완료, API/트레이딩 시스템 비교 문서 추가"
```

---

## 3. Claude 자동 로그 등록 (중요)

### 사용자 요청 방법

작업 마무리 시 다음과 같이 요청하세요:

> "오늘 작업 이슈 로그 등록해줘"

### Claude 실행 절차

**Claude는 이 문서를 읽고 다음 절차를 따라야 합니다:**

1. **현재 월 확인**: 오늘 날짜 기준으로 해당 월의 이슈 번호 확인 (6. 프로젝트 정보 참조)
2. **새 월인 경우**: 해당 월의 이슈가 없으면 새 이슈 생성
   ```bash
   gh issue create --title "📋 작업 로그 (YYYY년 M월)" --body "YYYY년 M월 프로젝트 진행 상황을 기록합니다." --label "log"
   ```
3. **커밋 내역 확인**: 오늘 날짜의 커밋 확인
   ```bash
   git log --oneline --since="midnight"
   ```
4. **로그 코멘트 등록**: 해당 월 이슈에 코멘트 추가
   ```bash
   cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox" && gh issue comment [이슈번호] --body "[작업 내용]"
   ```

### 코멘트 작성 형식

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

### 주의사항

- **작업 디렉토리**: 반드시 `c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox`에서 실행
- **월별 이슈 관리**: 매월 새 이슈를 생성하고, 이 문서의 "월별 로그 이슈" 테이블 업데이트 필요
- **이슈 번호 확인**: 6. 프로젝트 정보의 테이블에서 현재 월에 해당하는 이슈 번호 사용

---

## 4. 명령어 요약

| 용도 | 명령어 |
|------|--------|
| 이슈 생성 | `gh issue create --title "제목" --body "내용"` |
| 이슈에 코멘트 추가 | `gh issue comment [번호] --body "내용"` |
| 이슈 목록 보기 | `gh issue list` |
| 특정 이슈 보기 | `gh issue view [번호]` |
| 이슈 닫기 | `gh issue close [번호]` |

---

## 5. 라벨 활용

```bash
# 라벨 생성 (최초 1회)
gh label create "log" --description "작업 로그" --color "0E8A16"
gh label create "feature" --description "기능 개발" --color "1D76DB"
gh label create "docs" --description "문서 작업" --color "D4C5F9"

# 라벨과 함께 이슈 생성
gh issue create --title "제목" --body "내용" --label "log,docs"
```

---

## 6. 프로젝트 정보

- **레포지토리**: trading-sandbox

### 월별 로그 이슈

| 월 | 이슈 번호 | URL |
|----|----------|-----|
| 2026년 1월 | **#1** | https://github.com/silence102/trading-sandbox/issues/1 |
| 2026년 2월 | **#2** | https://github.com/silence102/trading-sandbox/issues/2 |

> 매월 새 이슈를 생성하여 월별로 작업 로그를 관리합니다.

---

## 7. 이슈 컨벤션

### 이슈 제목 형식

| 유형 | 제목 형식 | 예시 |
|------|----------|------|
| 작업 로그 | `📋 작업 로그 (YYYY년 M월)` | `📋 작업 로그 (2026년 2월)` |
| 기능 개발 | `[Feature] 기능명` | `[Feature] 자동매매 알림 기능` |
| 버그 수정 | `[Bug] 버그 설명` | `[Bug] API 토큰 만료 오류` |
| 문서 작업 | `[Docs] 문서 설명` | `[Docs] API 사용 가이드 추가` |

### 작업 로그 코멘트 형식

```markdown
## YYYY-MM-DD

### 완료 항목
- 작업 내용 1
- 작업 내용 2

### 커밋
- `커밋 메시지 1`
- `커밋 메시지 2`

### 추가된 파일 (선택)
- `파일 경로` - 설명
```

### 라벨 컨벤션

| 라벨 | 색상 | 용도 |
|------|------|------|
| `log` | `#0E8A16` (초록) | 작업 로그 |
| `feature` | `#1D76DB` (파랑) | 기능 개발 |
| `docs` | `#D4C5F9` (보라) | 문서 작업 |
| `bug` | `#D73A4A` (빨강) | 버그 수정 |

---

*마지막 업데이트: 2026년 2월 1일*
