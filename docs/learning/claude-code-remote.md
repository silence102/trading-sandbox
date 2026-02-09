# Claude Code 모바일 원격 제어 가이드

> 폰에서 PC의 Claude Code를 원격으로 제어하여, 외출 중에도 코딩 작업을 지시하고 모니터링할 수 있다.

---

## 방법 비교

| 방법 | 난이도 | 비용 | 장점 | 단점 |
|------|--------|------|------|------|
| **Happy Coder** | 쉬움 | 무료 | QR 페어링, 음성 제어, 다중 세션 | 별도 앱 필요 |
| **SSH + Tailscale + tmux** | 보통 | 무료 | 완전한 터미널 제어, 가장 안정적 | 초기 설정 복잡 |
| **공식 Claude iOS 앱** | 매우 쉬움 | 무료 | 설정 불필요, GitHub 통합 | iOS만, GitHub 중심 |
| **Telegram Bot** | 보통 | 무료 | 포트 노출 없음, 알림 편리 | 인터랙티브 제한 |
| **CodeRemote** | 보통 | 무료 | 웹 UI, Tailscale 기반 자체 호스팅 | Tailscale 필요 |

---

## 방법 1: Happy Coder (추천 - 가장 간편)

오픈소스 모바일/웹 클라이언트. QR코드 페어링으로 설정이 가장 간단하다.

### 설치

```bash
# PC에서 CLI 설치 및 실행
npm i -g happy-coder && happy
```

### 모바일 앱

- **iOS**: App Store에서 "Happy Claude Code Client" 검색
- **Android**: Google Play Store에서 다운로드

### 사용 흐름

```
1. PC에서 `happy` 실행 → QR코드 표시
2. 폰 앱에서 QR코드 스캔 → 페어링 완료
3. 폰에서 명령 입력 or 음성 명령
4. PC의 Claude Code가 실행 → 결과 실시간 동기화
```

### 주요 기능

- 다중 Claude Code 세션 동시 관리 (프로젝트별 전환)
- 음성으로 명령 가능 (voice-to-action)
- End-to-End 암호화 (릴레이 서버도 내용 확인 불가)
- CLI / 모바일 / 웹 간 실시간 동기화

### 아키텍처

```
[폰 앱] ←→ [릴레이 서버 (암호화 전달만)] ←→ [PC CLI] ←→ [Claude Code]
```

> 출처: [Happy Engineering](https://happy.engineering/)

---

## 방법 2: SSH + Tailscale + tmux (가장 안정적)

전통적인 SSH 접속 방식. 완전한 터미널 제어가 가능하고 가장 안정적이다.

### 필요 도구

| 도구 | 역할 | 설치 |
|------|------|------|
| **Tailscale** | 어디서든 PC에 접속 가능한 VPN | [tailscale.com](https://tailscale.com/) |
| **tmux** | 터미널 세션 유지 (PC 앞에 없어도 유지) | `brew install tmux` (Mac) |
| **mosh** (선택) | 네트워크 변경에도 끊기지 않는 SSH | `brew install mosh` (Mac) |
| **Blink Shell** (iOS) | 폰용 터미널 앱 (mosh 지원) | App Store |
| **Termius** (대안) | 폰용 SSH 클라이언트 | App Store / Play Store |

### 설정 단계

#### Step 1: PC와 폰에 Tailscale 설치

```bash
# Mac
brew install tailscale

# 또는 tailscale.com에서 다운로드
```

- 폰에도 Tailscale 앱 설치 후 같은 계정으로 로그인
- 이제 같은 네트워크에 있지 않아도 PC에 접속 가능

#### Step 2: PC에서 SSH 서버 설정

**Mac의 경우:**

```bash
# SSH 공개키 등록
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# 폰에서 생성한 공개키를 authorized_keys에 추가
echo "폰의_공개키_내용" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**SSH 데몬 설정** (`/etc/ssh/sshd_config`):

```
PubkeyAuthentication yes
PasswordAuthentication no
```

```bash
# SSH 서비스 재시작
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```

**Windows의 경우:**

```powershell
# OpenSSH 서버 설치 (관리자 PowerShell)
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# SSH 서비스 시작 및 자동 시작 설정
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

#### Step 3: tmux 설정

`~/.tmux.conf` 파일 생성/편집:

```bash
# 스크롤 히스토리 확대 (Claude Code 출력이 길어질 수 있으므로)
set -g history-limit 1000000

# 마우스 지원 (폰에서 스크롤 가능)
set -g mouse on
```

#### Step 4: 사용 흐름

```bash
# 1. PC에서 tmux 세션 시작
tmux new-session -A -s claude

# 2. tmux 안에서 Claude Code 실행
claude

# 3. PC에서 자리 비우기 (세션 분리)
# Ctrl+B, D (tmux detach)

# 4. 폰에서 SSH 접속
ssh 사용자명@PC의_Tailscale_주소

# 5. tmux 세션 재접속
tmux attach -t claude

# 6. Claude Code가 그대로 실행 중 → 폰에서 상호작용
```

#### Step 5: mosh로 업그레이드 (선택)

SSH는 와이파이↔LTE 전환 시 끊기지만, mosh는 네트워크가 바뀌어도 연결을 유지한다.

```bash
# PC에서 mosh-server 설치
brew install mosh    # Mac
# Windows는 WSL에서 설치 가능

# 폰에서 mosh로 접속 (Blink Shell 등)
mosh 사용자명@PC의_Tailscale_주소 -- tmux attach -t claude
```

### 주의사항

- tmux 세션 분리는 반드시 `Ctrl+B, D` 사용 (Ctrl+D는 세션 종료 = Claude Code도 종료)
- AFK 전에 반드시 tmux 세션 안에서 Claude Code를 실행할 것
- Tailscale은 무료 플랜으로 개인 사용 충분

> 출처: [adim.in - Remote controlling Claude Code](https://adim.in/p/remote-control-claude-code/), [Harper Reed's Blog](https://harper.blog/2026/01/05/claude-code-is-better-on-your-phone/)

---

## 방법 3: 공식 Claude iOS 앱

Anthropic이 공식 지원하는 방법. 별도 설정 없이 가장 빠르게 시작할 수 있다.

### 사용법

1. App Store에서 "Claude" 앱 설치
2. Anthropic 계정으로 로그인
3. Claude Code 기능 활성화
4. GitHub 저장소 연결

### 제한사항

- iOS만 지원 (Android 미지원)
- GitHub 연동 중심 (로컬 프로젝트 직접 접근 제한)
- PC에서 실행 중인 Claude Code와 동기화되지 않음 (별도 세션)

> 출처: [Sealos Blog - Claude Code on Phone](https://sealos.io/blog/claude-code-on-phone)

---

## 방법 4: Telegram Bot

Telegram 메시지로 Claude Code에 명령을 보내고 결과를 받는 방식.

### 장점

- 포트 노출 없음 (Bot이 Telegram 서버를 폴링)
- 고정 IP나 DNS 불필요
- 데스크톱/모바일 모두 사용 가능

### 설치

GitHub 저장소: [JessyTsui/Claude-Code-Remote](https://github.com/JessyTsui/Claude-Code-Remote)

- Telegram, Discord, Email 등 다양한 채널 지원
- 작업 완료 시 알림 → 답장으로 새 명령 전달

> 출처: [Medium - Claude Code with Telegram Bot](https://medium.com/@amirilovic/how-to-use-claude-code-from-your-phone-with-a-telegram-bot-dde2ac8783d0)

---

## 우리 프로젝트에서의 활용 시나리오

### 1. 외출 중 모닝 브리핑 생성

```
폰에서 → "python scripts/main.py --type morning --ai" 실행
→ PC에서 데이터 수집 + AI 분석 → 브리핑 파일 생성
→ 폰에서 결과 확인
```

### 2. 장중 실시간 시장 체크

```
폰에서 → Claude Code에게 "시장 상황 알려줘" 요청
→ KRX + 뉴스 수집 → 실시간 요약 제공
```

### 3. 장 마감 후 애프터마켓 브리핑

```
퇴근길에 → "python scripts/main.py --type aftermarket" 실행
→ 금일 시장 요약 + 공시 확인
```

### 4. 긴급 코드 수정

```
외출 중 버그 발견 → 폰에서 Claude Code 접속
→ 수정 지시 → 커밋/푸시까지 원격 수행
```

---

## 추천 조합

| 상황 | 추천 방법 |
|------|----------|
| **처음 시작** | Happy Coder (설정 최소) |
| **안정적 장시간 작업** | SSH + Tailscale + tmux |
| **간단한 확인/명령** | Telegram Bot |
| **iOS 사용자 (GitHub 중심)** | 공식 Claude 앱 |

### 우리 프로젝트 추천

1. **Happy Coder** 우선 도입 (간편, 무료, 음성 제어)
2. 필요 시 **SSH + Tailscale + tmux**로 확장 (완전한 제어)

---

## 참고 자료

- [adim.in - Remote controlling Claude Code](https://adim.in/p/remote-control-claude-code/)
- [Harper Reed's Blog - Remote Claude Code](https://harper.blog/2026/01/05/claude-code-is-better-on-your-phone/)
- [Happy Engineering - Mobile Client](https://happy.engineering/)
- [CodeRemote](https://coderemote.dev/)
- [Claude-Code-Remote (GitHub)](https://github.com/JessyTsui/Claude-Code-Remote)
- [Sealos Blog - Claude Code on Phone](https://sealos.io/blog/claude-code-on-phone)
- [Moshi App - SSH Terminal for Claude Code](https://getmoshi.app/)

---

*작성일: 2026년 2월 9일*
