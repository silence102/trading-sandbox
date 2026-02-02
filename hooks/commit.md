# 커밋 및 푸시 트리거

> 커밋 요청 시 이 문서를 참고하여 컨벤션에 맞게 진행합니다.

## 트리거 요청

사용자가 다음과 같이 요청하면 이 문서를 참고하여 실행합니다:

- "커밋해줘"
- "푸시해줘"
- "커밋하고 푸시해줘"
- "변경사항 올려줘"

---

## 실행 절차

### Step 1: 변경 사항 확인

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
git status
git diff --stat
```

### Step 2: 커밋 타입 결정

변경 내용에 따라 적절한 접두사를 선택합니다.

### Step 3: 커밋 메시지 작성 및 커밋

```bash
git add [파일들]
git commit -m "접두사: 커밋 메시지

상세 내용 (선택)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Step 4: 푸시

```bash
git push origin master
```

---

## 커밋 컨벤션

### 접두사 규칙

| 접두사 | 용도 | 예시 |
|--------|------|------|
| `feat:` | 새로운 기능 추가 | `feat: Claude 자동화 트리거 시스템 도입` |
| `fix:` | 버그 수정 | `fix: 이슈 번호 오류 수정` |
| `docs:` | 문서 추가/수정 | `docs: 증권사 리포트 기록 추가 (2026-01-26~28)` |
| `refactor:` | 코드 리팩토링 | `refactor: 폴더 구조 개선` |
| `style:` | 코드 포맷팅, 세미콜론 등 | `style: 마크다운 포맷 정리` |
| `chore:` | 빌드, 설정 파일 수정 | `chore: .gitignore 업데이트` |
| `revert:` | 이전 커밋 되돌리기 | `revert: 한투 리포트 자동화 계획 철회` |

### 메시지 작성 규칙

1. **제목**: 50자 이내, 명령형으로 작성
2. **본문** (선택): 변경 이유나 상세 내용
3. **Co-Author**: Claude 협업 시 항상 추가

### 예시

#### 단순 문서 추가
```
docs: 증권사 리포트 기록 추가 (2026-01-26~28)
```

#### 기능 추가 (상세 설명 포함)
```
feat: GitHub Issue 자동화 가이드 추가

- 월별 이슈 관리 체계 도입
- Claude 트리거 문서화
- gh CLI 사용 절차 정리

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

#### 여러 변경사항
```
docs: API 및 트레이딩 시스템 비교 분석 문서 추가

- docs/api-comparison.md: KIS vs 키움 API 비교
- docs/trading-systems.md: HTS/MTS/WTS 개념 정리

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## 폴더별 권장 접두사

| 폴더 | 권장 접두사 |
|------|------------|
| `docs/` | `docs:` |
| `notes/reports/` | `docs:` |
| `hooks/`, `automation/` | `feat:` 또는 `docs:` |
| `results/` | `docs:` |
| `troubleshooting_log/` | `docs:` |
| 설정 파일 (`.gitignore` 등) | `chore:` |

---

## 주의사항

- 커밋 전 `git status`로 변경 사항 확인
- 민감한 파일 (`.env`, API 키 등) 커밋 금지
- 큰 변경은 논리적 단위로 분리하여 커밋
- HEREDOC 형식으로 멀티라인 메시지 작성

```bash
git commit -m "$(cat <<'EOF'
feat: 기능 설명

상세 내용

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

*마지막 업데이트: 2026년 2월 3일*
