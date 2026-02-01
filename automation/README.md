# 자동화 (automation)

> Claude가 참고하여 자동으로 실행할 수 있는 작업들을 문서화한 폴더입니다.

## 사용 방법

사용자가 특정 작업을 요청하면, Claude는 이 폴더의 해당 문서를 읽고 절차에 따라 자동으로 실행합니다.

## 자동화 목록

| 파일 | 트리거 요청 | 설명 |
|------|------------|------|
| [github-issue-log.md](github-issue-log.md) | "오늘 작업 이슈 로그 등록해줘" | 작업 로그를 GitHub Issue에 등록 |

## 폴더 구조

```
automation/
├── README.md              # 본 문서 (자동화 목록)
└── github-issue-log.md    # GitHub Issue 작업 로그 자동화
```

## 새 자동화 추가 시

1. 역할별로 새 파일 생성 (예: `slack-notification.md`)
2. 트리거 요청, 실행 절차, 필요 정보를 명확히 문서화
3. 이 README의 자동화 목록 테이블에 추가

---

*마지막 업데이트: 2026년 2월 1일*
