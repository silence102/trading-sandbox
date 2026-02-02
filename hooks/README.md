# Hooks (트리거 진입점)

> 사용자의 특정 요청을 감지하여 자동화 작업을 실행하는 진입점입니다.

## 작동 방식

```
사용자 요청 → hooks/ 확인 → automation/ 참조 → 작업 실행 → 관련 파일 업데이트
```

## Claude 필수 확인 사항

**새 대화 세션 시작 시, 사용자가 아래 트리거 요청을 하면:**

1. 이 폴더(`hooks/`)의 해당 트리거 파일을 먼저 읽습니다
2. 트리거 파일에 명시된 `automation/` 문서를 참조합니다
3. 작업 완료 후 관련 파일들을 업데이트합니다

---

## 트리거 목록

| 트리거 요청 | Hook 파일 | 실행 작업 |
|------------|-----------|----------|
| "오늘 작업 이슈 로그 등록해줘" | [issue-log.md](issue-log.md) | GitHub Issue에 작업 로그 등록 |
| "리포트 기록 업데이트해줘" | [report-update.md](report-update.md) | 새 리포트 PDF OCR 후 README 업데이트 |
| "커밋해줘" / "푸시해줘" | [commit.md](commit.md) | 커밋 컨벤션에 따라 커밋 및 푸시 |

---

## 폴더 구조

```
hooks/                      # 트리거 진입점
├── README.md              # 본 문서
├── issue-log.md           # 이슈 로그 등록 트리거
├── report-update.md       # 리포트 업데이트 트리거
└── commit.md              # 커밋/푸시 트리거

automation/                 # 실제 작업 절차
├── README.md
├── github-issue-log.md    # 이슈 로그 상세 절차
└── commit-convention.md   # 커밋 컨벤션 상세 가이드
```

---

*마지막 업데이트: 2026년 2월 2일*
