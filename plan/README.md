# 개발 계획 — 실행 가이드

> 이 파일은 모든 계획의 **우선순위 마스터 가이드**입니다.
> 작업을 시작하기 전 이 파일을 먼저 확인하세요.

---

## 전체 실행 로드맵

```
Phase 1 ✅ 완료 (2026-02-11)
  └── P1-A: AI 프롬프트 금지 표현 추가 (briefing_generator.py)
  └── P1-B: CLAUDE.md 생성 (프로젝트 루트)
  └── P1-C: GitHub Actions AI_ENABLED/OPENAI_API_KEY 추가 (daily-briefing.yml)

Phase 2 ✅ 완료 (2026-02-11)
  └── P2-A: collect_all_data() 병렬화 (briefing_generator.py)
  └── P2-B: plan/templates/feature-design.md 생성
  └── P2-C: 모닝/미드데이 프롬프트 품질 규칙 추가

Phase 3 ← 다음 작업
  └── P3-A: Structured Outputs (Pydantic 모델 + JSON 이중 저장)

Phase 4 ~ (대형 기능)
  └── 브리핑 확장 (해외 증시, 원자재, 알림)
  └── 공모주 시스템
  └── 자동매매 (KIS API)
```

---

## 우선순위 실행 목록

### 🔴 우선순위 1 — Phase 2: 성능 + 개발 인프라 (즉시 실행 가능)

| # | 항목 | 파일 | 난이도 | 참고 |
|---|------|------|--------|------|
| 1 | `collect_all_data()` 병렬화 | `scripts/briefing_generator.py` | 중간 | [P2-A 상세](#p2-a-collectalldata-병렬화) |
| 2 | 기능 설계 템플릿 생성 | `plan/templates/feature-design.md` | 낮음 | [P2-B 상세](#p2-b-기능-설계-템플릿) |
| 3 | 각 브리핑 타입별 프롬프트 금지 표현 보강 | `scripts/briefing_generator.py` | 낮음 | [상세](#p2-c-프롬프트-금지-표현-보강) |

---

### 🟠 우선순위 2 — Phase 3: AI 분석 구조화 (Phase 2 후)

| # | 항목 | 파일 | 난이도 | 참고 |
|---|------|------|--------|------|
| 4 | Pydantic 모델 설계 (StockInsight, MarketAnalysis) | `scripts/briefing_generator.py` | 중간 | [P3-A 상세](#p3-a-structured-outputs) |
| 5 | `generate_with_ai_structured()` 구현 | `scripts/briefing_generator.py` | 높음 | [P3-A 상세](#p3-a-structured-outputs) |
| 6 | `.md + .json` 이중 저장 구조 | `scripts/briefing_generator.py` | 중간 | [P3-A 상세](#p3-a-structured-outputs) |
| 7 | 등락률 ±5% 콘솔 경고 알림 | `scripts/briefing_generator.py` | 낮음 | P3-A 의존 |

---

### 🟡 우선순위 3 — 브리핑 확장 (Phase 3 후, 선택적)

| # | 항목 | 파일 | 난이도 | 참고 |
|---|------|------|--------|------|
| 8 | 해외 증시 데이터 수집 모듈 | `scripts/collectors/global_market.py` | 높음 | [02-daily-briefing-expansion.md](02-daily-briefing-expansion.md) |
| 9 | 섹터별 자금 흐름 / 수급 분석 | `scripts/collectors/sector_analysis.py` | 높음 | [02-daily-briefing-expansion.md](02-daily-briefing-expansion.md) |
| 10 | 급등/급락 알림 시스템 | `scripts/briefing_generator.py` | 중간 | P3-A 선행 필요 |
| 11 | 주간 트렌드 분석 | `scripts/briefing_generator.py` | 중간 | [02-daily-briefing-expansion.md](02-daily-briefing-expansion.md) |

---

### 🟢 우선순위 4 — 신규 대형 기능 (독립적, 장기)

| # | 항목 | 파일 | 난이도 | 참고 |
|---|------|------|--------|------|
| 12 | 공모주 일정 수집 및 알림 | `scripts/collectors/ipo_collector.py` | 높음 | [03-ipo-system.md](03-ipo-system.md) |
| 13 | KIS API 계좌/잔고 조회 | `scripts/kis/` (신규 디렉토리) | 높음 | [04-kis-api-customization.md](04-kis-api-customization.md) |
| 14 | KIS API 조건부 주문 / 손절·익절 자동화 | `scripts/kis/` | 매우 높음 | [04-kis-api-customization.md](04-kis-api-customization.md) |

---

### ⚪ 우선순위 5 — 불편 사항 개선 (경험 후 기록)

| # | 항목 | 파일 | 비고 |
|---|------|------|------|
| 15 | 투자 불편 사항 직접 기록 후 개선 | [05-pain-points-improvement.md](05-pain-points-improvement.md) | 항목 아직 없음 — 사용 중 발견 시 추가 |

---

## 세부 실행 가이드

### P2-A: `collect_all_data()` 병렬화

**목적**: 순차 실행 중인 4개 collector를 동시 실행 → 수집 시간 50% 단축 목표

**대상 파일**: `scripts/briefing_generator.py` — `collect_all_data()` 메서드

**구현 코드**:
```python
from concurrent.futures import ThreadPoolExecutor
import time

def collect_all_data(self, briefing_type):
    settings = BRIEFING_SETTINGS[briefing_type]
    start = time.time()

    def fetch_krx():
        return self.krx.format_for_briefing()

    def fetch_ecos():
        return self.ecos.format_for_briefing()

    def fetch_dart():
        return self.dart.format_for_briefing(
            days_back=settings["days_back"],
            max_items=settings["max_disclosures"]
        )

    def fetch_news():
        return self.news.format_for_briefing(
            max_items=settings["max_news"],
            max_hours=settings["news_max_hours"]
        )

    tasks = {
        "krx": fetch_krx,
        "ecos": fetch_ecos,
        "dart": fetch_dart,
        "news": fetch_news,
    }

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {key: executor.submit(fn) for key, fn in tasks.items()}
        for key, future in futures.items():
            try:
                results[key] = future.result(timeout=30)
            except Exception as e:
                print(f"[경고] {key} 수집 실패: {e}")
                results[key] = f"## {key} 데이터 수집 실패\n수집 중 오류가 발생했습니다."

    elapsed = time.time() - start
    print(f"[수집 완료] {elapsed:.1f}초 소요")
    return results
```

**필수 안전 조건**:
- `future.result(timeout=30)` — 30초 초과 시 포기
- `try-except` — 하나 실패해도 나머지 브리핑은 정상 생성
- fallback 문자열 — AI가 "수집 실패" 텍스트를 받아 처리 가능

**검증 방법**:
```bash
python scripts/main.py --type aftermarket
# 수집 완료 X.Xs 소요 로그 확인
# 기존 대비 시간 비교
```

---

### P2-B: 기능 설계 템플릿

**목적**: 새 기능 작업 시 사전 설계 문서 표준화

**생성 파일**: `plan/templates/feature-design.md`

**내용**:
```markdown
# [기능명] 설계 문서

## 목적
한 줄로 무엇을 왜 만드는지 서술

## 현재 동작 (Before)
현재 코드/흐름 설명

## 변경 후 동작 (After)
변경 후 코드/흐름 설명

## 수정 대상 파일
- 파일명: 변경 내용

## 예상 부작용
- 기존 기능과의 충돌 가능성

## 롤백 방법
- 어떻게 되돌릴 수 있는지
```

---

### P2-C: 프롬프트 금지 표현 보강

**목적**: `AI_SYSTEM_PROMPT`에 추가된 금지 표현을 모닝/미드데이/애프터마켓 개별 프롬프트에도 적용

**대상**: `scripts/briefing_generator.py`
- `AI_MORNING_PROMPT`
- `AI_MIDDAY_PROMPT`
- `AI_AFTERMARKET_PROMPT`

**추가할 내용** (각 프롬프트 마지막 줄 앞에):
```
작성 시 반드시 준수: 수치 없는 평가 문장 금지, ±3% 이상 종목은 원인 분석 포함
```

---

### P3-A: Structured Outputs

**목적**: AI 분석 결과를 `.md`(사람용) + `.json`(기계용) 동시 저장 → 알림·DB 확장 가능

**선행 조건**: P2-A 완료 후 진행 권장

**Pydantic 모델 설계**:
```python
from pydantic import BaseModel

class StockInsight(BaseModel):
    ticker: str        # "005930"
    name: str          # "삼성전자"
    close: int         # 167800
    change_pct: float  # +1.21
    assessment: str    # "상승" | "하락" | "보합"
    key_reason: str    # 등락 원인 한 줄 요약
    watch_point: str   # 내일 주목 포인트

class MarketAnalysis(BaseModel):
    date: str               # "2026-02-11"
    briefing_type: str      # "aftermarket"
    kospi_trend: str        # 시장 전반 한 줄 요약
    key_macro_event: str    # 오늘 주요 거시 이벤트
    stocks: list[StockInsight]
    tomorrow_strategy: str  # 내일 전략 요약
```

**저장 구조**:
```
notes/daily_briefing/
├── 2026-02-11_애프터마켓브리핑.md    ← 기존 (마크다운)
└── 2026-02-11_애프터마켓브리핑.json  ← 신규 (구조화 데이터)
```

**참고 문서**: [docs/learning/structured-outputs-guide.md](../docs/learning/structured-outputs-guide.md)

---

## 계획 파일 목록

| 파일 | 주제 | 상태 |
|------|------|------|
| [01-skills-insight-application.md](01-skills-insight-application.md) | Skills 인사이트 적용 (Phase 1 완료) | 🔄 진행 중 |
| [02-daily-briefing-expansion.md](02-daily-briefing-expansion.md) | 일일 브리핑 자동화 확장 | 🔄 진행 중 |
| [03-ipo-system.md](03-ipo-system.md) | 공모주 일정 및 투자 자동화 | 📝 계획 중 |
| [04-kis-api-customization.md](04-kis-api-customization.md) | 증권사 API 커스터마이징 (자동매매) | 📝 계획 중 |
| [05-pain-points-improvement.md](05-pain-points-improvement.md) | 투자 불편 사항 개선 | 📝 계획 중 |

## 상태 표기

| 상태 | 설명 |
|------|------|
| 📝 계획 중 | 아이디어 수집 및 계획 수립 단계 |
| 🔄 진행 중 | 구현 진행 중 |
| ✅ 완료 | 구현 완료 |
| ⏸️ 보류 | 일시 중단 |

---

*마지막 업데이트: 2026년 2월 11일*
