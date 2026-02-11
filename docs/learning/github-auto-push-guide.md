# GitHub 자동 업로드 원리 가이드

> "작업이 끝나자마자 GitHub에 올라가는데, 이게 어떤 원리야?"

---

## 결론부터

이 프로젝트에서 코드/문서 변경이 GitHub에 즉시 반영되는 것은 **두 가지 별개의 메커니즘** 때문입니다.

| 상황 | 누가 올리나 | 원리 |
|------|-----------|------|
| Claude Code와 작업 중 | **Claude Code** 직접 | 사용자 요청 또는 작업 완료 후 `git commit && git push` 실행 |
| 매일 아침/점심/저녁 브리핑 | **GitHub Actions** 자동 | cron 스케줄로 워크플로우 실행 후 자동 커밋 & 푸시 |

---

## 메커니즘 1: Claude Code의 직접 push

### 어떻게 동작하나

Claude Code (이 AI)는 터미널 명령을 직접 실행할 수 있습니다. 작업 완료 후 다음 명령을 실행합니다:

```bash
git add [수정된 파일들]
git commit -m "docs: [변경 내용 요약]"
git push
```

### 왜 즉시 올라가나

- 별도의 동기화 설정이 없어도 됩니다
- Claude Code가 작업 완료 → 커밋 → 푸시를 한 번에 처리합니다
- 이 프로젝트는 `hooks/commit.md`에 "커밋해줘/푸시해줘" 트리거가 있어서, 해당 요청 시 `automation/` 절차를 따릅니다

### 이게 설정된 시점

- `6448f69` (2026-02-10): 3분기 브리핑 체계 구축 작업부터 Claude Code가 직접 커밋 & 푸시 시작
- 이전에는 수동으로 커밋하거나 VSCode Source Control 패널을 통해 업로드했습니다
- Claude Code에게 "작업 끝나면 커밋하고 올려줘"라고 요청한 순간부터 이 패턴이 정착되었습니다

### 이 방식의 장점

- 작업 완료와 동시에 백업됩니다
- 커밋 히스토리가 작업 단위로 정확하게 쌓입니다
- 나중에 `git log`로 어떤 작업을 했는지 추적 가능합니다

### 주의사항

- **커밋 컨벤션 필수**: `CLAUDE.md`에 정의된 `feat:`, `docs:`, `fix:` 등 prefix 없이 올라가면 히스토리 관리가 어려워집니다
- 커밋 없이 끝내도 되는 작업(실험, 임시 확인 등)은 명시적으로 "커밋하지 말고" 또는 "나중에 정리해서 커밋해줘"라고 요청하면 됩니다

---

## 메커니즘 2: GitHub Actions 자동 커밋

### 어떻게 동작하나

`.github/workflows/daily-briefing.yml` 파일에 정의된 워크플로우가:

1. 매일 정해진 시간에 GitHub 서버에서 자동 실행됩니다
2. Python 스크립트로 브리핑을 생성합니다
3. 생성된 파일을 `git commit && git push`로 저장소에 올립니다

```yaml
# daily-briefing.yml 핵심 부분
- name: Commit and push briefing
  run: |
    git config --local user.email "github-actions[bot]@users.noreply.github.com"
    git config --local user.name "github-actions[bot]"
    git add notes/daily_briefing/
    git commit -m "docs: 모닝 브리핑 자동 생성 (2026-02-11)"
    git push
```

### 스케줄

| 시간 (KST) | cron 표현식 (UTC) | 브리핑 유형 |
|-----------|-----------------|------------|
| 08:00 월~금 | `0 23 * * 0-4` | 모닝 브리핑 |
| 12:30 월~금 | `30 3 * * 1-5` | 미드데이 브리핑 |
| 18:00 월~금 | `0 9 * * 1-5` | 애프터마켓 브리핑 |

### 활성화 조건

GitHub Actions 자동 실행이 되려면 **두 가지 Repository 설정**이 필요합니다:

```
GitHub 저장소 → Settings → Secrets and variables → Actions

[Variables 탭]
BRIEFING_ENABLED = true    ← 워크플로우 실행 여부 제어
AI_ENABLED = true          ← OpenAI AI 분석 포함 여부

[Secrets 탭]
DART_API_KEY = [키값]      ← DART 공시 API
ECOS_API_KEY = [키값]      ← 한국은행 경제지표 API
OPENAI_API_KEY = [키값]    ← OpenAI GPT API (AI_ENABLED=true 시 필요)
```

### GitHub Actions에서 push가 가능한 이유

- GitHub Actions 워크플로우는 기본적으로 `GITHUB_TOKEN`이라는 임시 토큰을 자동 발급받습니다
- 이 토큰은 현재 저장소에 대한 읽기/쓰기 권한이 있어서 `git push`가 가능합니다
- 별도로 Personal Access Token (PAT)을 설정할 필요가 없습니다

---

## 전체 흐름 요약

```
[Claude Code 작업 완료]          [GitHub Actions 스케줄]
         │                               │
         ▼                               ▼
  git commit + push              cron 시간 도달
         │                               │
         ▼                               ▼
  GitHub 저장소에 반영          워크플로우 실행 (우분투 서버)
                                         │
                                         ▼
                                브리핑 생성 + 자동 커밋
                                         │
                                         ▼
                                 GitHub 저장소에 반영
                                         │
                                         ▼
                            git pull로 로컬에 동기화 가능
```

---

## 로컬에서 최신 브리핑 받기

GitHub Actions가 자동 생성한 브리핑을 로컬에서 보려면:

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
git pull origin master
```

또는 GitHub 웹(https://github.com/silence102/trading-sandbox)에서 직접 확인할 수도 있습니다.

---

*생성일: 2026년 2월 11일*
*마지막 업데이트: 2026년 2월 11일*
