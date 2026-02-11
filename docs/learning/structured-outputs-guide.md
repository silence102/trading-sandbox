# OpenAI Structured Outputs 활용 가이드

> LLM 응답을 줄글이 아닌 **구조화된 JSON**으로 받아서 서비스에 활용하는 방법을 정리합니다.

## 1. 한눈에 보는 개념

### 줄글 응답 vs 구조화 응답

지금 우리 프로젝트의 AI 분석은 이렇게 생겼다:

```
## 금일 시장 총평
금일 KOSPI는 소폭 상승(+0.07%)하며 5,301.69로 마감했으나,
KOSDAQ은 하락(-1.10%)하여...

## 관심 종목 리뷰
- **삼성전자**: 165,800원으로 거래되며 안정적인 거래량...
```

사람이 읽기에는 좋지만, **프로그램에서 특정 값을 뽑아쓰기 어렵다.**

Structured Outputs를 쓰면 같은 분석을 이렇게 받을 수 있다:

```json
{
  "market_summary": "KOSPI 소폭 상승, KOSDAQ 하락. 시장 혼조세",
  "sentiment": "중립",
  "key_issues": [
    "삼성전자 노조 성과급 20% 요구",
    "구글 200억달러 AI 투자, 미국 반도체 관세 면제"
  ],
  "watchlist_insights": [
    {
      "name": "삼성전자",
      "signal": "관망",
      "reason": "노조 이슈로 단기 하락 위험"
    },
    {
      "name": "삼양식품",
      "signal": "매수",
      "reason": "배당 관련 공시 다수, 긍정적"
    }
  ],
  "tomorrow_strategy": "KOSDAQ 방어적 대응, 삼성전자 노조 이슈 모니터링"
}
```

**핵심**: 같은 LLM, 같은 비용인데 응답 형태만 바뀐다. 스키마를 지정하면 그 구조를 100% 준수하는 JSON이 나온다.

---

## 2. 왜 필요한가 - 현재 프로젝트의 한계

현재 `briefing_generator.py`의 AI 분석 흐름:

```
수집 데이터 → OpenAI API (줄글 요청) → 마크다운 텍스트 → 파일 저장
```

**문제점:**
- AI 분석 결과에서 "삼성전자의 시그널이 뭔지" 프로그래밍으로 추출 불가
- 종목별 분석을 따로 DB에 저장하려면 텍스트 파싱이 필요 (불안정)
- 대시보드, 알림 등 서비스 확장 시 데이터 재가공이 필수

**Structured Outputs 적용 후:**

```
수집 데이터 → OpenAI API (스키마 지정) → Python 객체 → 마크다운 + JSON 동시 저장
                                            ↘ DB 저장
                                            ↘ 대시보드 표시
                                            ↘ 알림 발송
```

하나의 API 호출로 **마크다운 브리핑**도 만들고 **구조화 데이터**도 동시에 확보할 수 있다.

---

## 3. 두 가지 방식 비교

OpenAI에서 구조화 응답을 받는 방법은 두 가지다.

### 방식 A: json_schema (저수준)

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "market_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "sentiment": {"type": "string"},
                    "summary": {"type": "string"}
                },
                "required": ["sentiment", "summary"],
                "additionalProperties": False
            }
        }
    }
)

# 결과: JSON 문자열 → 직접 파싱 필요
import json
result = json.loads(response.choices[0].message.content)
print(result["sentiment"])  # "중립"
```

### 방식 B: Pydantic + parse() (권장)

```python
from pydantic import BaseModel
from openai import OpenAI

class MarketAnalysis(BaseModel):
    sentiment: str
    summary: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[...],
    response_format=MarketAnalysis,  # Pydantic 클래스를 바로 전달
)

# 결과: 바로 Python 객체로 사용
result = completion.choices[0].message.parsed
print(result.sentiment)  # "중립" - IDE 자동완성도 됨
```

### 비교표

| 항목 | 방식 A (json_schema) | 방식 B (Pydantic parse) |
|------|---------------------|------------------------|
| 스키마 정의 | JSON dict 직접 작성 | Python 클래스로 정의 |
| 응답 타입 | JSON 문자열 (수동 파싱) | Python 객체 (자동 파싱) |
| IDE 자동완성 | 불가 | 가능 |
| 타입 안전성 | 없음 | 있음 |
| 스트리밍 | 지원 | 미지원 |
| 추천 대상 | 동적 스키마가 필요할 때 | **대부분의 경우 (권장)** |

---

## 4. 우리 프로젝트 적용 방안

### Step 1: Pydantic 모델 설계

```python
# scripts/models.py (신규 파일)

from pydantic import BaseModel


class StockInsight(BaseModel):
    """개별 종목 분석"""
    name: str           # 종목명 (예: "삼성전자")
    code: str           # 종목코드 (예: "005930")
    signal: str         # "매수" / "관망" / "매도"
    reason: str         # 판단 근거 한 줄


class MarketAnalysis(BaseModel):
    """시장 전체 분석 결과"""
    market_summary: str                     # 시장 한줄 요약
    sentiment: str                          # "긍정" / "중립" / "부정"
    key_issues: list[str]                   # 핵심 이슈 (3~5개)
    watchlist_insights: list[StockInsight]  # 관심 종목별 분석
    strategy: str                           # 전략 제안
```

### Step 2: briefing_generator.py 변경

**Before (현재 코드):**

```python
# 줄글 마크다운으로 응답 받음
response = client.chat.completions.create(
    model=AI_MODEL,
    messages=[
        {"role": "system", "content": AI_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
    max_tokens=AI_MAX_TOKENS,
    temperature=AI_TEMPERATURE,
)

analysis = response.choices[0].message.content  # 마크다운 줄글
```

**After (Structured Outputs 적용):**

```python
from models import MarketAnalysis

# 구조화된 Python 객체로 응답 받음
completion = client.beta.chat.completions.parse(
    model=AI_MODEL,
    messages=[
        {"role": "system", "content": AI_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ],
    response_format=MarketAnalysis,
    temperature=AI_TEMPERATURE,
)

result = completion.choices[0].message.parsed  # MarketAnalysis 객체

# 구조화 데이터에서 마크다운 생성
analysis_md = format_analysis_to_markdown(result)

# 동시에 JSON으로도 저장
analysis_json = result.model_dump_json(indent=2, ensure_ascii=False)
```

### Step 3: 구조화 데이터 → 마크다운 변환

```python
def format_analysis_to_markdown(analysis: MarketAnalysis) -> str:
    """구조화된 분석 결과를 마크다운으로 변환"""

    # 감성 이모지 매핑
    sentiment_map = {"긍정": "🟢", "중립": "🟡", "부정": "🔴"}
    emoji = sentiment_map.get(analysis.sentiment, "⚪")

    # 종목별 시그널
    signal_map = {"매수": "🟢", "관망": "🟡", "매도": "🔴"}

    lines = [
        f"## 시장 총평 {emoji}",
        f"{analysis.market_summary}",
        "",
        "## 핵심 이슈",
    ]

    for issue in analysis.key_issues:
        lines.append(f"- {issue}")

    lines.append("")
    lines.append("## 관심 종목 분석")
    lines.append("")
    lines.append("| 종목 | 시그널 | 근거 |")
    lines.append("|------|--------|------|")

    for stock in analysis.watchlist_insights:
        s_emoji = signal_map.get(stock.signal, "⚪")
        lines.append(f"| {stock.name} | {s_emoji} {stock.signal} | {stock.reason} |")

    lines.append("")
    lines.append(f"## 전략\n{analysis.strategy}")

    return "\n".join(lines)
```

### Step 4: JSON 동시 저장

```python
# 마크다운 브리핑 저장 (기존)
with open("notes/daily_briefing/2026-02-10_애프터마켓브리핑.md", "w") as f:
    f.write(briefing_md)

# 구조화 데이터 JSON 저장 (신규)
with open("notes/daily_briefing/2026-02-10_애프터마켓브리핑.json", "w") as f:
    f.write(result.model_dump_json(indent=2, ensure_ascii=False))
```

저장되는 JSON 예시:

```json
{
  "market_summary": "KOSPI 소폭 상승(+0.07%), KOSDAQ 하락(-1.10%). 혼조세 마감",
  "sentiment": "중립",
  "key_issues": [
    "삼성전자 노조 영업이익 20% 성과급 요구, 이견 지속",
    "구글 200억달러 AI 투자 계획 발표",
    "미국 빅테크 수입 반도체 관세 면제"
  ],
  "watchlist_insights": [
    {
      "name": "삼성전자",
      "code": "005930",
      "signal": "관망",
      "reason": "노조 갈등 이슈로 단기 불확실성 존재"
    },
    {
      "name": "SK하이닉스",
      "code": "000660",
      "signal": "관망",
      "reason": "반도체 관세 면제 호재이나 주가 반영 제한적"
    },
    {
      "name": "삼양식품",
      "code": "003230",
      "signal": "매수",
      "reason": "배당 관련 공시 다수, 주주환원 기대감"
    }
  ],
  "strategy": "KOSDAQ 방어적 대응. 삼성전자 노조 이슈 추이 모니터링 후 대응"
}
```

---

## 5. 활용 시나리오

구조화된 데이터가 확보되면 다양한 확장이 가능하다.

### 시나리오 1: 대시보드 표시

```python
# sentiment 값으로 시장 분위기 아이콘 자동 매칭
if result.sentiment == "긍정":
    show_green_indicator()

# 종목별 시그널을 카드 UI에 바로 매핑
for stock in result.watchlist_insights:
    render_stock_card(
        name=stock.name,
        signal=stock.signal,    # "매수" → 녹색 배지
        reason=stock.reason
    )
```

### 시나리오 2: DB 저장 및 추적

```python
# 일별 시그널 변화 추적
for stock in result.watchlist_insights:
    db.save({
        "date": "2026-02-10",
        "stock_code": stock.code,
        "signal": stock.signal,
        "reason": stock.reason,
        "sentiment": result.sentiment
    })

# 나중에: "삼성전자 시그널이 관망→매수로 바뀐 날" 조회 가능
```

### 시나리오 3: 조건부 알림

```python
# 매수/매도 시그널이 나오면 알림 발송
for stock in result.watchlist_insights:
    if stock.signal in ["매수", "매도"]:
        send_notification(
            title=f"[{stock.signal}] {stock.name}",
            body=stock.reason
        )
```

### 시나리오 4: 시그널 정확도 백테스트

```python
# JSON 이력이 쌓이면 AI 시그널의 정확도를 사후 검증할 수 있음
signals = db.query("SELECT * FROM signals WHERE stock_code = '005930'")

for s in signals:
    actual_return = get_next_day_return(s.stock_code, s.date)
    was_correct = (s.signal == "매수" and actual_return > 0) or \
                  (s.signal == "매도" and actual_return < 0)
    # 정확도 통계 산출
```

---

## 6. 주의사항

### 모델 지원

| 모델 | Structured Outputs 지원 |
|------|------------------------|
| gpt-4o-mini | 지원 (현재 프로젝트 사용 중) |
| gpt-4o | 지원 |
| gpt-3.5-turbo | **미지원** |

### 스키마 제약

- 전체 속성 수 최대 5,000개
- 중첩 깊이 최대 10단계
- `additionalProperties`는 반드시 `False`
- enum 값 최대 1,000개

### 비용

- 추가 비용 없음 (기존 API 호출과 동일 토큰 과금)
- 단, 첫 번째 요청 시 스키마 처리로 약간의 지연 발생 (이후 캐시됨)

### 에러 처리

```python
completion = client.beta.chat.completions.parse(...)
message = completion.choices[0].message

# 1. 모델이 응답을 거부한 경우
if message.refusal:
    print(f"거부됨: {message.refusal}")
    return

# 2. 응답이 잘린 경우 (토큰 초과)
if completion.choices[0].finish_reason == "length":
    print("응답이 잘림 - max_tokens 늘려야 함")
    return

# 3. 정상 파싱
result = message.parsed
```

### Pydantic 의존성

`requirements.txt`에 pydantic 추가 필요:

```
pydantic>=2.0.0
```

> 참고: `openai>=1.0.0` 설치 시 pydantic이 함께 설치되므로, 현재 프로젝트에서는 별도 설치 없이 바로 사용 가능하다.

---

## 7. 참고 자료

- [OpenAI Structured Outputs 공식 문서](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI Python SDK - Structured Outputs](https://github.com/openai/openai-python/blob/main/helpers.md)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)

---

*마지막 업데이트: 2026년 2월 10일*
