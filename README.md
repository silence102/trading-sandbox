# Trading Sandbox

## 0. 프로젝트 목적

본 프로젝트는 **주식 투자 자동매매 시스템**을 구축하기 위한 기반을 다지는 과정입니다.

실제 투자 프로그램을 활용하여 직접 투자하고, 증권사 리포트를 분석하며 투자 판단을 내리는 경험을 축적하고 있습니다. AI 에이전트를 적극 활용하여 투자 경험을 획기적으로 개선하고, 이 과정에서 얻은 인사이트를 바탕으로 실질적인 서비스를 구축하고자 합니다.

개인적인 투자 역량 강화뿐만 아니라, **다른 투자자들에게도 도움이 되는 서비스를 만들어 보기 위한 초석**을 다지는 경험이기도 합니다.

### 자동화의 핵심 목적

> **"간단한 조작만으로 거래를 수행하고, 다양한 시나리오에 대비하며, 여러 관점에서 분석하여 인지 부담을 줄이면서도 상황을 명확히 파악할 수 있도록 한다."**

| 목표 | 설명 |
|------|------|
| **간단한 조작** | 복잡한 매매 과정을 단순화하여 빠르게 실행 |
| **시나리오 대비** | 목표가 설정, 하락 대비, 트리거 상황 등 사전 준비 |
| **다각도 분석** | 여러 관점에서 종목과 시장을 분석 |
| **인지 부담 경감** | 정보 과부하 없이 핵심 상황만 명확히 파악 |

## 1. 현재 단계

> **기능 구현 단계** - 일일 마켓 브리핑 자동화 파이프라인 가동 중

### 완료 항목
- [x] 한국투자증권 ISA 계좌 개설
- [x] KIS Developers 실전투자 API Key 발급
- [x] KIS Developers 모의투자 API Key 발급
- [x] 2026년 1월 모의투자 완료 (**+9.29% 수익률**)
- [x] eFriend Plus(HTS)를 활용한 실제 투자 진행
- [x] 한국투자증권 리포트 분석 및 기록 (8개 파일, 01/08~01/31)
- [x] 투자 과정에서의 문제점 및 개선 사항 도출
- [x] 일일 마켓 브리핑 자동화 파이프라인 구축 (KRX + DART + ECOS + 뉴스 RSS)
- [x] 모닝 / 미드데이 / 애프터마켓 3종 브리핑 체계 구현
- [x] OpenAI GPT 기반 AI 시장 분석 연동 (ON/OFF 토글)
- [x] GitHub Actions 자동 스케줄 설정 (08:00 / 12:30 / 18:00 KST)
- [x] AI 프롬프트 품질 개선 (금지 표현 목록 + 수치 근거 필수 규칙)
- [x] CLAUDE.md 개발 원칙 + 커밋 컨벤션 정의

### 진행 중
- [ ] 투자 Pain Points 정리 및 문서화 → `notes/pain_points/`
- [ ] 개발 기능 정의 및 자동화 대상 정리

### 예정
- [ ] 공모주 일정 및 투자 자동화 → `plan/ipo-system.md`
- [ ] KIS API 커스터마이징 → `plan/kis-api-customization.md`
- [ ] AI 에이전트 기반 자동매매 시스템 개발
- [ ] 모의투자 → 실전투자 단계적 적용

## 2. 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| **1. 문제 정의** | 실제 투자 경험 + 리포트 분석을 통한 개선점 도출 | ✅ 완료 |
| **2. 기능 정의** | 자동화 대상 정리 및 개발 기능 명세 | 🔄 진행 중 |
| **3. 구현** | 일일 브리핑 자동화, AI 분석, 데이터 수집 파이프라인 | 🔄 진행 중 |
| **4. 검증** | 모의투자 → 실전투자 단계적 적용 | ⏳ 예정 |

## 3. 기술 스택

| 구분 | 내용 |
|------|------|
| 증권사 | 한국투자증권 |
| API | KIS Developers (실전/모의) |
| HTS | eFriend Plus |
| 계좌 | ISA 계좌 |
| 언어 | Python 3.12+ |
| AI | OpenAI GPT (gpt-4o-mini) |

### 데이터 수집 API

| API | 용도 | 상태 | 비용 |
|-----|------|------|------|
| [DART](https://opendart.fss.or.kr/) | 기업 공시, 재무제표 | ✅ 연동 완료 | 무료 |
| [PyKRX](https://github.com/sharebook-kr/pykrx) | 주식 시세, 거래량, 지수 | ✅ 연동 완료 | 무료 |
| [ECOS](https://ecos.bok.or.kr/api/) | 기준금리, 환율 등 경제지표 | ✅ 연동 완료 | 무료 |
| 뉴스 RSS | 한국경제, 매일경제, 이데일리 | ✅ 연동 완료 | 무료 |
| [OpenAI](https://platform.openai.com/) | AI 시장 분석 (GPT) | ✅ 연동 완료 | 유료 (ON/OFF) |

---

## 4. 프로젝트 구조

```
trading-sandbox/
├── .env                         # 🔒 API 키 (git 제외)
├── .env.example                 # API 키 템플릿
├── .gitignore                   # git 제외 파일 설정
├── CLAUDE.md                    # Claude Code 개발 원칙 (커밋 컨벤션, 작업 순서)
├── README.md                    # 본 문서
├── requirements.txt             # Python 의존성 목록
│
├── config/                      # ⚙️ 설정
│   ├── __init__.py
│   └── settings.py              # API 키, AI 설정, 브리핑 설정
│
├── scripts/                     # 🐍 자동화 파이프라인
│   ├── __init__.py
│   ├── main.py                  # CLI 진입점 (모닝/미드데이/애프터마켓 브리핑)
│   ├── briefing_generator.py    # 브리핑 생성기 + OpenAI AI 분석
│   └── collectors/              # 데이터 수집기 모듈
│       ├── __init__.py
│       ├── dart_collector.py    # DART 공시 수집 (opendartreader)
│       ├── krx_collector.py     # KRX 주식 시세/지수 수집 (pykrx)
│       ├── ecos_collector.py    # ECOS 경제지표 수집 (한국은행 + FRED)
│       └── news_collector.py    # 뉴스 RSS 수집 (feedparser)
│
├── hooks/                       # 🎯 Claude Code 작업 지침 문서 (자동화 코드 아님)
│   ├── README.md
│   ├── market-briefing.md       # "마켓 브리핑 생성해줘"
│   ├── market-check.md          # "시장 상황 알려줘"
│   ├── issue-log.md             # "이슈 로그 등록해줘"
│   ├── report-update.md         # "리포트 기록 업데이트해줘"
│   ├── readme-update.md         # "README 업데이트해줘"
│   └── commit.md                # "커밋해줘" / "푸시해줘"
│
├── automation/                  # 🤖 로컬 자동화 절차 문서
│   ├── README.md
│   ├── github-issue-log.md      # GitHub Issue 작업 로그 절차
│   └── readme-update.md         # README.md 구조 최신화 절차
│
├── plan/                        # 📋 개발 계획 (우선순위순 번호 파일명)
│   ├── README.md                # 전체 실행 로드맵 + 우선순위 가이드
│   ├── 01-skills-insight-application.md  # Skills 인사이트 적용 (Phase 1 완료)
│   ├── 02-daily-briefing-expansion.md    # 일일 브리핑 확장
│   ├── 03-ipo-system.md                  # 공모주 자동화
│   ├── 04-kis-api-customization.md       # KIS API 커스터마이징
│   └── 05-pain-points-improvement.md     # 투자 불편 사항 개선
│
├── notes/                       # 📝 투자 기록 및 산출물
│   ├── daily_briefing/          # 📈 일일 마켓 브리핑 (자동 생성)
│   │   ├── YYYY-MM-DD_모닝브리핑.md
│   │   ├── YYYY-MM-DD_미드데이브리핑.md
│   │   └── YYYY-MM-DD_애프터마켓브리핑.md
│   ├── watchlist.md             # 관심 종목 목록 + 변경 이력
│   ├── reports/                 # 📄 증권사 리포트 분석 기록
│   │   ├── README.md
│   │   └── YY-MM-DD~DD_기록.pdf
│   └── pain_points/             # 💡 투자 문제점 및 개선 사항
│       └── README.md
│
├── docs/                        # 📚 학습 및 참고 문서
│   ├── README.md
│   ├── learning/                # 학습 자료
│   │   ├── api-comparison.md              # 증권사 API 비교
│   │   ├── trading-systems.md             # HTS/MTS/WTS 비교
│   │   ├── github-issue-guide.md          # GitHub Issue 가이드
│   │   ├── structured-outputs-guide.md    # OpenAI Structured Outputs 활용
│   │   ├── claude-code-skills-guide.md    # Claude Code Skills 인사이트
│   │   ├── claude-opus4-agent-teams.md    # Claude Opus 4.6 & Agent Teams
│   │   └── github-auto-push-guide.md      # GitHub 자동 업로드 원리
│   └── references/              # 외부 라이브러리 주의사항
│       └── pykrx-notice.md      # PyKRX 면책 및 저작권
│
├── results/                     # 📊 투자 결과물
│   ├── README.md
│   ├── 2026-01_모의투자_결과.md
│   └── 1월_모의투자_결과.png
│
├── troubleshooting_log/         # 🔧 문제 해결 기록
│   └── YYYY-MM-DD_이슈명.md
│
└── .github/
    └── workflows/
        └── daily-briefing.yml   # ⏰ GitHub Actions 자동 브리핑 (3회/일)
```

---

## 4-1. 아키텍처 시각화

> 이 섹션은 전체 시스템 흐름을 한눈에 파악하기 위한 다이어그램입니다.
> 구조 변경 시 이 섹션도 함께 업데이트하세요.

### 데이터 수집 → AI 분석 → 저장 파이프라인

```
[스케줄 트리거]
GitHub Actions (cron) 또는 python scripts/main.py --type X
        │
        ▼
[브리핑 유형 결정]
  ┌─────────────────────────────────┐
  │  모닝 (08:00)   장 시작 전 준비  │
  │  미드데이 (12:30) 장중 점검      │
  │  애프터마켓 (18:00) 장 마감 복기 │
  └─────────────────────────────────┘
        │
        ▼
[데이터 수집 — 4개 Collector 순차 실행]  ← Phase 2에서 병렬화 예정
  ├── krx_collector.py    →  KOSPI/KOSDAQ 지수, 관심 종목 OHLCV (pykrx)
  ├── ecos_collector.py   →  기준금리, 환율(원/달러·엔·위안·파운드) (ECOS + FRED)
  ├── dart_collector.py   →  관심 종목 공시 (DART API)
  └── news_collector.py   →  뉴스 헤드라인 (한국경제/매일경제/이데일리 RSS)
        │                  ※ 관심 종목 목록 → notes/watchlist.md 참고
        │
        ▼
[briefing_generator.py — 브리핑 조립]
  ├── 마크다운 섹션 조합 (시장 현황 → 거시경제 → 공시 → 뉴스)
  └── AI_ENABLED=true 이면 → OpenAI gpt-4o-mini 분석 추가
        │
        ▼
[저장]
  notes/daily_briefing/YYYY-MM-DD_XX브리핑.md    ← 현재 구조
  (Phase 3 완료 후) + YYYY-MM-DD_XX브리핑.json  ← Structured Outputs 예정
        │
        ▼
[GitHub Actions: 자동 커밋 & 푸시]
  git commit -m "docs: XX 브리핑 자동 생성 (YYYY-MM-DD)"
  git push → GitHub 저장소에 브리핑 파일 누적
```

### 자동화 인프라 레이어 구조

```
┌────────────────────────────────────────────────────────────┐
│  GitHub Actions (.github/workflows/daily-briefing.yml)     │
│  스케줄: 08:00 / 12:30 / 18:00 KST (월~금)                │
│  제어: BRIEFING_ENABLED, AI_ENABLED (Repository Variables)  │
└────────────────────────┬───────────────────────────────────┘
                         │ python scripts/main.py --type X
┌────────────────────────▼───────────────────────────────────┐
│  scripts/briefing_generator.py  (핵심 파이프라인)           │
│  collect_all_data() → generate_with_ai() or basic()        │
└──────┬──────────────┬──────────────┬──────────────┬────────┘
       │              │              │              │
  KRX  ▼         ECOS ▼        DART ▼        뉴스 ▼
 pykrx          ECOS API      DART API       RSS Feed
 (무료)         +FRED API     (무료)         (무료)
                (무료)
```

### 설정 관리 구조

```
.env (로컬, git 제외)          GitHub Actions
  └── DART_API_KEY               └── Secrets: DART_API_KEY
  └── ECOS_API_KEY                             ECOS_API_KEY
  └── OPENAI_API_KEY                           OPENAI_API_KEY
  └── AI_ENABLED=true/false      └── Variables: AI_ENABLED
  └── WATCHLIST_STOCKS                         BRIEFING_ENABLED
         │
         ▼
  config/settings.py  (환경변수 로드 + 기본값 정의)
```

### 개발 계획 로드맵 (현재 상태)

```
Phase 1 ✅ 완료 (2026-02-11)
  ├── AI 프롬프트 금지 표현 추가 (Humanizer)
  ├── CLAUDE.md 개발 원칙 정의 (Superpowers)
  └── GitHub Actions AI_ENABLED/OPENAI_API_KEY 연동

Phase 2 ← 현재 대기 중
  ├── collect_all_data() 병렬화 (ThreadPoolExecutor x4)
  ├── plan/templates/feature-design.md 생성
  └── 브리핑별 프롬프트 금지 표현 보강

Phase 3
  └── Structured Outputs (Pydantic + .md + .json 이중 저장)

Phase 4+  (대형 기능)
  ├── 해외 증시 / 섹터 수급 데이터 수집
  ├── 공모주 일정 자동화 (03-ipo-system.md)
  └── KIS API 자동매매 (04-kis-api-customization.md)
```

---

## 5. 폴더별 상세 설명

### `config/` - 설정 관리

| 파일 | 역할 |
|------|------|
| `settings.py` | 모든 설정값의 중앙 관리 (API 키, AI 모델, 관심 종목, 브리핑 유형별 설정) |

**주요 설정값:**

| 설정 | 파일 | 설명 |
|------|------|------|
| API 키 (DART, ECOS, OpenAI) | `.env` | 환경변수로 관리, git 제외 |
| AI ON/OFF | `.env` → `AI_ENABLED` | `true`/`false`, 유료 API이므로 기본 OFF |
| AI 모델 | `settings.py` → `AI_MODEL` | 기본: `gpt-4o-mini` |
| AI 응답 톤 | `settings.py` → `AI_TEMPERATURE` | 기본: 0.3 (낮을수록 일관적) |
| 관심 종목 | `.env` → `WATCHLIST_STOCKS` | 쉼표 구분 종목코드 |

### `scripts/` - 자동화 파이프라인

데이터 수집부터 브리핑 생성까지의 전체 파이프라인을 담당합니다.

**동작 흐름:**
```
main.py (CLI)
  ↓ --type morning/aftermarket, --ai
briefing_generator.py
  ↓ 데이터 수집 요청
collectors/ (DART + KRX + ECOS + News)
  ↓ 수집 데이터 반환
briefing_generator.py
  ↓ 마크다운 브리핑 조립
  ↓ (--ai 시) OpenAI GPT에 분석 요청
notes/daily_briefing/YYYY-MM-DD_모닝브리핑.md 저장
```

| 파일 | 역할 |
|------|------|
| `main.py` | CLI 진입점. `--type`, `--ai`, `--status`, `--test`, `--schedule` 지원 |
| `briefing_generator.py` | 수집 데이터 통합 → 모닝/애프터마켓 브리핑 생성 + AI 분석 |
| `collectors/dart_collector.py` | DART API로 관심 종목 공시 수집 (opendartreader) |
| `collectors/krx_collector.py` | KOSPI/KOSDAQ 지수 + 관심 종목 시세 수집 (pykrx) |
| `collectors/ecos_collector.py` | 기준금리, 환율 등 경제지표 수집 (한국은행 ECOS) |
| `collectors/news_collector.py` | 한국경제/매일경제/이데일리 RSS 뉴스 수집 |

### `hooks/` - Claude 트리거 진입점

사용자의 특정 요청을 감지하면 Claude가 이 폴더의 파일을 먼저 읽고 절차를 따릅니다.

| 사용자 요청 | Hook 파일 | 실행 작업 |
|------------|-----------|----------|
| "모닝 브리핑 생성해줘" | `market-briefing.md` | 모닝 브리핑 생성 |
| "애프터 마켓 브리핑 생성해줘" | `market-briefing.md` | 애프터마켓 브리핑 생성 |
| "지금 시장 상황 알려줘" | `market-check.md` | 실시간 시세/뉴스 조회 |
| "이슈 로그 등록해줘" | `issue-log.md` | GitHub Issue에 작업 로그 등록 |
| "리포트 기록 업데이트해줘" | `report-update.md` | 새 리포트 PDF OCR 후 README 업데이트 |
| "커밋해줘" / "푸시해줘" | `commit.md` | 커밋 컨벤션에 따라 커밋 및 푸시 |

### `plan/` - 개발 계획

전체 실행 로드맵은 [plan/README.md](plan/README.md)에 우선순위별로 정리되어 있습니다.

| 파일 | 주제 | 상태 |
|------|------|------|
| `01-skills-insight-application.md` | Skills 인사이트 적용 | 🔄 진행 중 (Phase 1 완료) |
| `02-daily-briefing-expansion.md` | 일일 브리핑 자동화 확장 | 🔄 진행 중 |
| `03-ipo-system.md` | 공모주 일정 및 투자 자동화 | 📝 계획 중 |
| `04-kis-api-customization.md` | 증권사 API 커스터마이징 | 📝 계획 중 |
| `05-pain-points-improvement.md` | 투자 불편 사항 개선 | 🔄 진행 중 |

### `notes/` - 투자 기록 및 산출물

| 하위 폴더 | 역할 |
|-----------|------|
| `daily_briefing/` | 자동 생성된 일일 마켓 브리핑 저장 (모닝/애프터마켓) |
| `reports/` | 한국투자증권 리포트 수기 분석 기록 (PDF) |
| `pain_points/` | 투자 중 겪은 문제점 및 개선 아이디어 |

### `docs/` - 학습 및 참고 문서

| 하위 폴더 | 역할 |
|-----------|------|
| `learning/` | 증권사 API 비교, HTS/MTS 비교 등 학습 자료 |
| `references/` | 외부 라이브러리 주의사항 (PyKRX 면책 등) |

### `.github/workflows/` - GitHub Actions 자동화

`daily-briefing.yml`이 매일 자동으로 브리핑을 생성합니다.

| 스케줄 | 시간 (KST) | 브리핑 유형 |
|--------|-----------|------------|
| `cron: '0 23 * * 0-4'` | 월~금 08:00 | 모닝 브리핑 |
| `cron: '30 3 * * 1-5'` | 월~금 12:30 | 미드데이 브리핑 |
| `cron: '0 9 * * 1-5'` | 월~금 18:00 | 애프터마켓 브리핑 |

현재 상태: **ON** (`BRIEFING_ENABLED=true`, `AI_ENABLED=true`)

설정 위치:
- GitHub 저장소 → Settings → Secrets and variables → Actions
- Variables: `BRIEFING_ENABLED=true`, `AI_ENABLED=true`
- Secrets: `DART_API_KEY`, `ECOS_API_KEY`, `OPENAI_API_KEY`

---

## 6. 일일 마켓 브리핑

### 브리핑 유형

| 유형 | 시간 | 목적 | 데이터 기준 |
|------|------|------|------------|
| **모닝 브리핑** | 08:00 KST | 장 시작 전 투자 준비 | 전일 데이터 |
| **미드데이 브리핑** | 12:30 KST | 장중 시장 점검 | 당일 오전 데이터 |
| **애프터 마켓 브리핑** | 18:00 KST | 장 마감 후 시장 복기 | 당일 전체 데이터 |

### 브리핑 구성

| 섹션 | 모닝 브리핑 | 미드데이 브리핑 | 애프터마켓 브리핑 | 데이터 소스 |
|------|-----------|--------------|----------------|------------|
| 1 | 전일 시장 마감 | 장중 시장 현황 | 금일 시장 동향 | KRX (PyKRX) |
| 2 | 환율 / 금리 | 환율 / 금리 | 거시경제 지표 | ECOS + FRED |
| 3 | 주요 공시 | 공시 업데이트 | 금일 주요 공시 | DART |
| 4 | 오전 주요 뉴스 | 점심 주요 뉴스 | 오후 주요 뉴스 | 뉴스 RSS |
| 5 | AI 시장 분석 (선택) | AI 시장 분석 (선택) | AI 시장 분석 (선택) | OpenAI GPT |

### 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성 후 API 키 입력
cp .env.example .env

# 모닝 브리핑 생성
python scripts/main.py --type morning

# 애프터 마켓 브리핑 생성
python scripts/main.py --type aftermarket

# AI 분석 포함 (AI_ENABLED=true 필요)
python scripts/main.py --type morning --ai

# 현재 파이프라인 상태 확인
python scripts/main.py --status

# 개별 수집기 테스트
python scripts/main.py --test dart
python scripts/main.py --test krx
python scripts/main.py --test ecos
python scripts/main.py --test news
```

### AI 분석 설정

OpenAI API는 유료이므로 **ON/OFF 이중 잠금** 방식으로 동작합니다.

```
AI 실행 조건: --ai 플래그 + AI_ENABLED=true (둘 다 충족 필요)
```

| 설정 | 위치 | 기본값 | 설명 |
|------|------|--------|------|
| AI ON/OFF | `.env` → `AI_ENABLED` | `false` | `true`로 변경 시 활성화 |
| 모델 | `config/settings.py` → `AI_MODEL` | `gpt-4o-mini` | 비용 효율적 모델 |
| 최대 토큰 | `config/settings.py` → `AI_MAX_TOKENS` | `1500` | 응답 길이 제한 |
| 분석 톤 | `config/settings.py` → `AI_TEMPERATURE` | `0.3` | 낮을수록 일관적 |
| 시스템 프롬프트 | `scripts/briefing_generator.py` | - | 한국 주식시장 애널리스트 역할 |
| 모닝 프롬프트 | `scripts/briefing_generator.py` | - | 전일 요약 + 관전 포인트 + 전략 |
| 애프터 프롬프트 | `scripts/briefing_generator.py` | - | 시장 총평 + 이슈 분석 + 내일 전략 |

---

## 7. 기록 예정 항목

분석 완료 후 다음 내용을 추가할 예정입니다:
- 프로젝트 기능 및 기술 상세
- 개선하고자 하는 사항
- 실제 개선 결과

## 참고사항

- 본 프로젝트는 개인 학습 및 서비스 개발 목적으로 진행됨
- 리포트 원본의 저작권은 한국투자증권에 있음
- 투자 판단은 본인 책임 하에 이루어져야 함

---

*마지막 업데이트: 2026년 2월 11일*
