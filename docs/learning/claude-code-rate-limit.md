# Claude Code 사용량 리미트 관리 및 알림 가이드

> Pro 플랜 사용 시 리미트에 도달하면 일정 시간 후 복구된다. 이 복구 시점을 감지하여 폰으로 알림을 받는 방법과, 리미트 중에도 다른 AI 도구로 작업을 이어가는 방법을 정리한다.

---

## 1. Claude 플랜별 사용량 리미트 정리

| 플랜 | 가격 | 리셋 주기 | 리셋 시점 |
|------|------|----------|----------|
| **Pro** | $20/월 | 5시간 단위 + 일간 | 매일 UTC 00:00 (KST 09:00) |
| **Max (5x)** | $100/월 | 5시간 단위 + 주간 | 매주 리셋 |
| **Max (20x)** | $200/월 | 5시간 단위 + 주간 | 매주 리셋 |

### 리미트 확인 방법

| 방법 | 명령/경로 | 정보 |
|------|----------|------|
| **웹 (가장 정확)** | claude.ai → Settings → Usage | 사용량 %, 리셋 시간 |
| **CLI 명령** | `/usage` (Claude Code 내에서) | 현재 세션 사용량 |
| **계정 정보** | `claude --account` | 구독 등급 확인 |

### 리미트 도달 시 표시되는 메시지

```
You've reached your usage limit for this period.
Resets in: 4 hours 23 minutes
```

---

## 2. 리미트 복구 알림을 폰으로 받기

### 방법 A: Pushover + Claude Code Hooks (가장 실용적)

Claude Code의 공식 Hooks 시스템을 활용하여 이벤트 발생 시 Pushover로 폰에 푸시 알림을 보낸다.

**구조:**
```
Claude Code → Hook 이벤트 감지 → 스크립트 실행 → Pushover API → 폰 알림
```

#### Step 1: Pushover 설정 (폰 알림 서비스)

1. [pushover.net](https://pushover.net/) 가입 (30일 무료 후 $5 일회성)
2. 폰에 Pushover 앱 설치 (iOS/Android)
3. 웹에서 Application 생성 → API Token 획득
4. User Key 확인

#### Step 2: 알림 스크립트 작성

프로젝트 폴더에 `.claude/hooks/` 디렉토리 생성:

```python
#!/usr/bin/env python3
# .claude/hooks/notify-pushover.py
"""
Claude Code 이벤트 발생 시 Pushover로 폰 알림 전송
"""
import json
import sys
import requests
from datetime import datetime

PUSHOVER_USER_KEY = "YOUR_USER_KEY"
PUSHOVER_APP_TOKEN = "YOUR_APP_TOKEN"

def send_pushover(title: str, message: str, priority: int = 0):
    """Pushover API로 폰 알림 전송"""
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
        "priority": priority,
    })

def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    notification_type = data.get("notification_type", "")
    message = data.get("message", "")
    now = datetime.now().strftime("%H:%M")

    if notification_type == "idle_prompt":
        send_pushover(
            f"[{now}] Claude Code 대기 중",
            message or "입력을 기다리고 있습니다"
        )
    elif notification_type == "permission_prompt":
        send_pushover(
            f"[{now}] Claude Code 권한 요청",
            message or "권한 승인이 필요합니다",
            priority=1  # 높은 우선순위
        )

if __name__ == "__main__":
    main()
```

#### Step 3: Claude Code Hooks 설정

`~/.claude/settings.json` (전역) 또는 `.claude/settings.json` (프로젝트별):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt|idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/notify-pushover.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

#### Step 4: 리미트 복구 타이머 스크립트

리미트에 도달하면 수동으로 타이머를 걸어 복구 시 알림을 받는 스크립트:

```python
#!/usr/bin/env python3
# .claude/hooks/limit-timer.py
"""
리미트 도달 시 실행 → 지정 시간 후 Pushover 알림
사용법: python limit-timer.py [분]
  예: python limit-timer.py 300  (5시간 = 300분 후 알림)
"""
import sys
import time
import requests
from datetime import datetime, timedelta

PUSHOVER_USER_KEY = "YOUR_USER_KEY"
PUSHOVER_APP_TOKEN = "YOUR_APP_TOKEN"

def send_pushover(title, message, priority=1):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
        "priority": priority,
        "sound": "cosmic",
    })

def main():
    minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 300  # 기본 5시간
    target = datetime.now() + timedelta(minutes=minutes)

    print(f"리미트 복구 타이머 설정: {minutes}분 후 ({target.strftime('%H:%M')})")
    print(f"Pushover 알림이 전송됩니다. 이 터미널을 닫지 마세요.")

    time.sleep(minutes * 60)

    send_pushover(
        "Claude Code 리미트 복구!",
        f"사용량이 리셋되었습니다. ({datetime.now().strftime('%H:%M')})\n다시 작업을 시작하세요!",
        priority=1
    )
    print("알림 전송 완료!")

if __name__ == "__main__":
    main()
```

**사용:**
```bash
# 리미트 도달 시 - 5시간(300분) 후 알림
python .claude/hooks/limit-timer.py 300

# 또는 리셋 메시지의 시간에 맞춰
python .claude/hooks/limit-timer.py 263  # "Resets in: 4 hours 23 minutes"
```

### 방법 B: 기존 Pushover 통합 오픈소스 활용

이미 만들어진 프로젝트를 바로 사용할 수 있다.

```bash
# 설치
git clone https://github.com/teito-dev/claudecode-pushover-integration.git
cd claudecode-pushover-integration
pip install -r requirements.txt

# 설정
cp .env.example .env
# .env에 PUSHOVER_USER_KEY, PUSHOVER_APP_TOKEN 입력

# 데몬 시작 (백그라운드 실행)
python3 claude_pushover_daemon.py
```

기능:
- Claude Code idle/permission 이벤트 자동 감지
- 30초당 최대 1개 알림 (스팸 방지)
- 우선순위 큐 (중요 이벤트 우선 전송)

> 출처: [claudecode-pushover-integration](https://github.com/teito-dev/claudecode-pushover-integration)

### 방법 C: Telegram Bot

포트 노출 없이 Telegram 메시지로 알림을 받는 방법.

```bash
# 설치
git clone https://github.com/JessyTsui/Claude-Code-Remote.git
cd Claude-Code-Remote
# 설정 후 Telegram Bot Token 입력
```

- Telegram Bot이 Claude Code 상태를 폴링
- 작업 완료/리미트 도달 시 메시지 전송
- 답장으로 새 명령 전달 가능

> 출처: [Claude-Code-Remote](https://github.com/JessyTsui/Claude-Code-Remote)

---

## 3. 리미트 중 다른 AI로 작업 이어가기

### 방법 A: OpenAI Codex CLI (가장 현실적인 대안)

Claude Code와 유사한 터미널 기반 AI 코딩 에이전트. ChatGPT Plus 구독에 포함되어 있다.

#### 설치

```bash
# npm으로 설치
npm i -g @openai/codex

# 또는 Homebrew (Mac)
brew install --cask codex
```

#### 사용

```bash
# 실행 (ChatGPT 계정 또는 API 키로 인증)
codex

# 프로젝트 디렉토리에서 실행
cd trading-sandbox && codex
```

#### 비교

| 항목 | Claude Code | OpenAI Codex |
|------|------------|-------------|
| 모델 | Claude Opus/Sonnet | GPT-5.3-Codex |
| 가격 | Pro $20/월 | Plus $20/월 (포함) |
| 리미트 | 5시간 단위 리셋 | 거의 도달하지 않음 |
| 강점 | 복잡한 SW 엔지니어링 (72.7%) | 코드 생성 속도, 안정성 |
| 약점 | 리미트 빈번 | 복잡한 의사결정 |

**추천 활용법:**
- Claude Code: 조사, 설계, 복잡한 의사결정
- Codex: 코드 작성, 반복 작업, Claude 리미트 시 대체

#### ChatGPT Plus 가입

Codex는 ChatGPT Plus ($20/월) 이상 구독에 포함되므로, 이미 가입되어 있다면 추가 비용 없이 사용 가능하다.

### 방법 B: 9Router (자동 폴백 프록시)

여러 AI 모델을 자동으로 전환하는 프록시. 리미트에 도달하면 자동으로 다른 모델로 전환된다.

```
Claude Code 요청 → 9Router → Tier 1: Claude (구독)
                              → Tier 2: GPT (저가)
                              → Tier 3: 무료 모델 (Kimi K2 등)
```

#### 설치

```bash
# 9Router 설치 및 실행
# localhost:20128에서 프록시 실행
# Claude Code의 API endpoint를 9Router로 지정
```

기능:
- 모델별 쿼타 자동 추적
- 리미트 도달 시 자동 폴백 (다운타임 0)
- Claude, GPT, Gemini, 무료 모델 지원

> 출처: [9Router](https://github.com/decolua/9router)

### 방법 C: Claude Code Router (OpenRouter 경유)

Claude Code의 모델을 OpenRouter를 통해 다양한 모델로 전환 가능.

```bash
# 환경변수로 API endpoint 변경
export ANTHROPIC_BASE_URL=http://localhost:PORT/v1
```

OpenRouter를 통해 GPT-4o, Gemini, Llama 등 다양한 모델을 Claude Code 인터페이스로 사용 가능.

> 출처: [claude-code-router](https://github.com/musistudio/claude-code-router)

---

## 4. 실전 운영 전략

### 리미트 최소화 전략

| 전략 | 설명 |
|------|------|
| **작업 배치** | 큰 작업을 한 번에 지시 (왕복 횟수 줄이기) |
| **컨텍스트 관리** | CLAUDE.md에 프로젝트 정보 정리 → 불필요한 탐색 감소 |
| **Sub-agent 활용** | Task tool로 하위 작업 분리 → 메인 컨텍스트 보존 |
| **모델 지정** | 단순 작업은 `--model haiku` 사용 (리미트 별도) |

### 리미트 도달 시 대응 플로우

```
리미트 도달
  ↓
1. 리셋 시간 확인 (/usage 또는 claude.ai)
  ↓
2. limit-timer.py 실행 (리셋 시간 입력)
  ↓
3. 긴급 작업이 있다면?
  ├── Yes → Codex CLI로 전환하여 작업 계속
  └── No → 다른 작업 후 Pushover 알림 대기
  ↓
4. 알림 수신 → Claude Code 복귀
```

### 이 프로젝트에서의 활용

```bash
# 시나리오: 모닝 브리핑 생성 중 리미트 도달

# 1. 리셋 타이머 설정 (5시간)
python .claude/hooks/limit-timer.py 300

# 2. Codex로 전환하여 작업 계속
codex
> "trading-sandbox 프로젝트에서 python scripts/main.py --type morning 실행해줘"

# 3. 5시간 후 Pushover 알림 수신 → Claude Code 복귀
```

---

## 5. 추천 조합

| 우선순위 | 도구 | 용도 |
|---------|------|------|
| 1 | **Pushover + limit-timer.py** | 리미트 복구 알림 (폰) |
| 2 | **OpenAI Codex CLI** | 리미트 중 대체 AI 코딩 |
| 3 | **Claude Code Hooks** | idle/permission 실시간 알림 |
| 4 | **9Router** (고급) | 자동 모델 폴백 (다운타임 0) |

---

## 참고 자료

- [Claude Help Center - Using Claude Code with Pro/Max](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Claude Code Notification Hooks 설정](https://alexop.dev/posts/claude-code-notification-hooks/)
- [Pushover Integration (GitHub)](https://github.com/teito-dev/claudecode-pushover-integration)
- [Rate Limit 확인 및 Reset Time](https://inventivehq.com/knowledge-base/claude/how-to-fix-rate-limits)
- [Feature Request: Usage Limit Visibility (GitHub)](https://github.com/anthropics/claude-code/issues/17431)
- [OpenAI Codex CLI (공식)](https://github.com/openai/codex)
- [9Router - AI Proxy](https://github.com/decolua/9router)
- [Claude Code Router](https://github.com/musistudio/claude-code-router)

---

*작성일: 2026년 2월 9일*
