# Claude Code Skills 활용 가이드

> AI 에이전트 생산성을 끌어올리는 Skills 생태계와, 우리 프로젝트에 실제로 적용할 수 있는 방안을 정리합니다.

---

## 1. Skills란 무엇인가

Claude Code(및 다양한 AI 에이전트)에는 **Skills**라는 확장 메커니즘이 있습니다.
일반적인 플러그인과 다른 점은, Skill이 "무엇을 해라"라는 지시문(프롬프트 + 규칙 집합)을 에이전트의 동작 방식 자체에 주입한다는 것입니다.

```
일반 도구: 에이전트 → 도구 호출 → 결과 반환
Skill:     에이전트의 사고 방식과 워크플로우 자체를 바꿈
```

GitHub에 등록된 오픈소스 Skill만 10만 개 이상이며, [skills.sh](https://skills.sh/)에서 검색하고 설치할 수 있습니다.

---

## 2. 실전에서 살아남은 4개의 Skills

### 2-1. Superpowers — 개발 프로세스 자체를 바꾸는 프레임워크

| 항목 | 내용 |
|------|------|
| GitHub Stars | 4.1만 개 (Skill 생태계 1위) |
| 설치 | `npx skills add obra/superpowers` |
| 핵심 특징 | 코드 작성 전에 설계부터 강제하는 7단계 워크플로우 |

**동작 방식:**
1. 에이전트가 코드를 짜기 전에 "무엇을 만들려는가"를 먼저 질문
2. 브레인스토밍 → 설계 문서 작성 → TDD → 코드 작성 → 리뷰 순으로 진행
3. 작업을 2~5분 단위로 쪼개 하위 에이전트에 병렬 배분
4. 2단계 자동 리뷰(셀프 검토 + 에이전트 간 크로스 리뷰) 수행

**핵심 인사이트:**
AI가 코드부터 짜는 게 아니라 **설계 → 계획 → 구현** 순서를 지키게 만든다.
큰 작업에서 방향을 잃지 않으면서 자율적으로 오랜 시간 작업이 가능한 이유가 여기 있다.

---

### 2-2. Humanizer — AI 냄새 24가지를 잡아내는 텍스트 필터

| 항목 | 내용 |
|------|------|
| 기반 | 위키피디아 Wiki Project AI Cleanup 팀의 실증 분석 |
| 설치 | `npx skills add blader/humanizer` |
| 핵심 특징 | AI 특유의 어휘·패턴 24종 자동 검출 및 교정 |

**검출 패턴 예시:**
- "testament", "landscape", "showcasing" 같은 AI 특유 어휘
- 의미를 부풀리는 수식어 남발
- 세 단어 나열 구조 ("빠르고, 정확하고, 효율적인")
- 엠대시(—) 과용, 이모지 오남용

**핵심 인사이트:**
AI가 생성한 텍스트는 통계적으로 가장 빈번하게 등장하는 표현을 쓴다.
사람의 글쓰기는 맥락에 맞게 덜 쓰이는 표현을 선택하기도 한다.
*한국어에는 별도 커스터마이징이 필요하다.*

---

### 2-3. UI/UX Pro Max — 업종별 디자인 시스템 자동 생성

| 항목 | 내용 |
|------|------|
| 내장 규칙 | 67개 UI 스타일, 96개 색상 팔레트, 57개 폰트 조합, 100개 업종별 추론 규칙 |
| 설치 | `npx skills add nextlevelbuilder/ui-ux-pro-max-skill` |
| 지원 스택 | React, Next.js, Vue, SwiftUI, Flutter 등 13개 |

**핵심 인사이트:**
AI가 만드는 UI에서 티가 나는 이유는 "기본값"을 그대로 사용하기 때문이다.
업종별 안티패턴(보라+분홍 그라디언트, 기본 템플릿 레이아웃 등)을 명시적으로 금지 목록으로 정의해두면 결과물이 달라진다.

---

### 2-4. Find Skills (Vercel 공식) — Skill 관리 자동화 CLI

| 항목 | 내용 |
|------|------|
| 제작 | Vercel Labs 공식 |
| 설치 | `npx skills add vercel-labs/skills` |
| 지원 에이전트 | Claude Code, Codex, Cursor, Gemini CLI, Windsurf 등 27개 |

**주요 명령어:**
```bash
npx skills find <키워드>   # 검색
npx skills add <repo>      # 설치
npx skills check           # 업데이트 확인
npx skills update          # 일괄 갱신
```

**핵심 인사이트:**
Skill이 많아질수록 관리 비용이 생긴다.
Find Skills는 Skill 설치·검색·업데이트를 하나의 워크플로우로 묶어준다.

---

## 3. "1인 관제탑" 작업 모델

글에서 소개된 Peter(OpenClaw 창시자)의 작업 환경은 시사하는 바가 크다.

```
[사람] — 관제탑 역할 (조율·의사결정)
  ├── 에이전트 A: 코드 작성
  ├── 에이전트 B: 디자인 생성
  └── 에이전트 C: 문서 정리
```

핵심은 **사람이 모든 걸 직접 하는 게 아니라, 에이전트들을 병렬로 지휘하는 구조**다.
이 구조를 가능하게 하는 게 바로 Superpowers 같은 Skill이다.
에이전트가 계획 없이 코드부터 짜면 관제탑이 개입할 여지가 없어진다.
설계 단계에서 사람이 방향을 잡고, 실행은 에이전트에 넘기는 것.

---

## 4. 설치 요약

```bash
# Skill 관리 도구 먼저 설치
npx skills add vercel-labs/skills

# 핵심 Skills 설치
npx skills add obra/superpowers
npx skills add blader/humanizer
npx skills add nextlevelbuilder/ui-ux-pro-max-skill
```

탐색: https://skills.sh/

---

*마지막 업데이트: 2026년 2월 11일*
