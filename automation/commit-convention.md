# 커밋 컨벤션 상세 가이드

> 프로젝트 전체에서 사용하는 커밋 메시지 규칙

---

## 커밋 메시지 구조

```
<접두사>: <제목>

<본문> (선택)

<꼬리말> (선택)
```

---

## 접두사 (Type)

### 주요 접두사

| 접두사 | 설명 | 사용 시점 |
|--------|------|----------|
| **feat** | 새로운 기능 | 새로운 기능, 시스템, 자동화 추가 |
| **fix** | 버그 수정 | 오류, 버그, 잘못된 내용 수정 |
| **docs** | 문서 | README, 가이드, 분석 문서, 리포트 기록 |
| **refactor** | 리팩토링 | 기능 변경 없이 코드/구조 개선 |
| **style** | 스타일 | 포맷팅, 공백, 오타 수정 |
| **chore** | 기타 작업 | 설정 파일, 빌드, 의존성 |
| **revert** | 되돌리기 | 이전 변경사항 철회 |

### 선택 접두사

| 접두사 | 설명 |
|--------|------|
| **test** | 테스트 코드 |
| **perf** | 성능 개선 |
| **ci** | CI/CD 설정 |

---

## 제목 작성 규칙

1. **50자 이내**로 간결하게
2. **명령형**으로 작성 (동사 원형)
3. **마침표 없이** 끝내기
4. **무엇을** 했는지 명확하게

### 좋은 예시
```
docs: 증권사 리포트 기록 추가 (2026-01-26~28)
feat: Claude 자동화 트리거 시스템 도입
fix: 이슈 번호 참조 오류 수정
```

### 나쁜 예시
```
docs: 문서 수정함.          # 마침표, 무엇을 수정했는지 불명확
feat: 추가                  # 무엇을 추가했는지 불명확
리포트 업데이트             # 접두사 누락
```

---

## 본문 작성 규칙 (선택)

- **왜** 변경했는지 설명
- **무엇이** 달라졌는지 목록으로 정리
- 한 줄당 72자 이내 권장

```
feat: GitHub Issue 자동화 가이드 추가

- 월별 이슈 관리 체계 도입 (#1: 1월, #2: 2월)
- Claude 트리거 문서화 (hooks/issue-log.md)
- gh CLI 사용 절차 상세 정리
```

---

## 꼬리말 (Footer)

### Co-Author (Claude 협업 시 필수)
```
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### 이슈 참조 (선택)
```
Closes #1
Refs #2
```

---

## 전체 예시

### 단순 문서 추가
```bash
git commit -m "docs: 증권사 리포트 기록 추가 (2026-01-26~28)"
```

### 기능 추가 (상세)
```bash
git commit -m "$(cat <<'EOF'
feat: Claude 자동화 트리거 시스템 (hooks/automation) 도입

- hooks/: 트리거 진입점 (issue-log.md, report-update.md)
- automation/: 작업 절차 문서 (github-issue-log.md)
- 월별 GitHub Issue 관리 체계 구축

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### 되돌리기
```bash
git commit -m "$(cat <<'EOF'
revert: 한투 리포트 자동화 계획 철회 (보안 차단)

- 안랩 보안 솔루션으로 인해 크롤링 자동화 불가
- 삭제: scripts/, requirements.txt, .env.example
- 추가: troubleshooting_log/ 폴더 및 불발 사유 기록

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## 프로젝트별 규칙

### 리포트 기록 추가
```
docs: 증권사 리포트 기록 추가 (YYYY-MM-DD~DD)
```

### README 업데이트
```
docs: README 업데이트 - [변경 내용]
```

### 결과 보고서 추가
```
docs: YYYY년 M월 모의투자 결과 보고서 추가 (+X.XX%)
```

### 트러블슈팅 기록
```
docs: 트러블슈팅 기록 추가 - [이슈명]
```

---

## 참고

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)

---

*마지막 업데이트: 2026년 2월 3일*
