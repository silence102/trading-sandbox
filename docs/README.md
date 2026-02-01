# 문서 (docs)

> 프로젝트 관련 조사 및 분석 문서 모음

## 문서 목록

| 파일 | 설명 | 주요 내용 |
|------|------|----------|
| [api-comparison.md](api-comparison.md) | 증권사 API 비교 분석 | 한국투자증권 vs 키움증권 Open API 장단점 비교 |
| [trading-systems.md](trading-systems.md) | 트레이딩 시스템 비교 | HTS/MTS/WTS 개념 및 증권사별 서비스 비교 |
| [github-issue-guide.md](github-issue-guide.md) | GitHub Issue 자동화 가이드 | 작업 로그를 Issue로 관리하는 방법 |

## 문서 요약

### 1. 증권사 API 비교 분석 (`api-comparison.md`)

한국투자증권 KIS Developers와 키움증권 Open API+를 비교 분석한 문서입니다.

**핵심 결론:**
- **권장**: 한국투자증권 KIS Developers
- **이유**: REST API 기본 제공, 크로스플랫폼 지원, AI 에이전트 연동 용이

| 구분 | 한국투자증권 | 키움증권 |
|------|-------------|---------|
| API 방식 | REST API | OCX + REST API |
| OS 지원 | Mac/Linux 포함 | REST API만 크로스플랫폼 |
| 조건검색 | ❌ | ✅ |
| 해외파생 | ✅ | ❌ |

### 2. 트레이딩 시스템 비교 (`trading-systems.md`)

HTS, MTS, WTS 개념과 주요 증권사 서비스를 비교 분석한 문서입니다.

**트레이딩 시스템 개념:**
| 구분 | HTS | MTS | WTS |
|------|-----|-----|-----|
| 정의 | PC용 프로그램 | 모바일 앱 | 웹 브라우저 |
| 설치 | 필요 | 앱 설치 | 불필요 |
| OS | Windows 전용 | iOS/Android | 범용 |

**주요 서비스:**
| 증권사 | HTS | MTS |
|--------|-----|-----|
| 한국투자증권 | eFriend Plus | eFriend Smart |
| 키움증권 | 영웅문 (시장점유율 1위) | 영웅문S# |

### 3. GitHub Issue 자동화 가이드 (`github-issue-guide.md`)

작업 로그를 GitHub Issue로 간편하게 관리하는 방법을 정리한 문서입니다.

**사용 방법:**
1. GitHub CLI 설치 및 로그인
2. 로그 이슈 생성 (최초 1회)
3. 작업 완료 후 `gh issue comment` 명령으로 로그 추가

**Claude에게 요청:**
> "오늘 작업 이슈 로그 등록해줘"

---

*마지막 업데이트: 2026년 2월 1일*
