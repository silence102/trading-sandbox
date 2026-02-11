"""
일일 마켓 브리핑 생성기

수집된 데이터를 통합하여 모닝/미드데이/애프터마켓 브리핑을 생성합니다.
- 모닝 브리핑 (08:00): 전일 종가, 환율/금리, 오전 뉴스
- 미드데이 브리핑 (장중): 장중 시세, 공시, 뉴스 실시간 점검
- 애프터 마켓 브리핑 (18:00): 금일 시장 동향, 공시, 오후 뉴스
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    OPENAI_API_KEY, RESULTS_DIR, BRIEFING_SETTINGS,
    AI_ENABLED, AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE,
)
from collectors import DartCollector, KrxCollector, EcosCollector, NewsCollector

# AI 분석용 시스템 프롬프트
AI_SYSTEM_PROMPT = """당신은 한국 주식시장 전문 애널리스트입니다.
수집된 시장 데이터를 바탕으로 간결하고 실용적인 투자 인사이트를 제공합니다.

분석 원칙:
1. 객관적 데이터 기반 분석 (감정적 표현 지양)
2. 국내 시장뿐 아니라 글로벌 매크로(미국 금리, 달러 강세/약세, 유가 등)와 국내 시장의 연관성을 반드시 짚어주세요
3. 뉴스에서 주요 정책 발표, 정치 이벤트, 외교/회담, 중앙은행 발언 등을 포착해 시장 영향력을 평가하세요
4. 관심 종목 분석 시 반드시 데이터(등락률, 고가/저가, 거래량)를 근거로 서술하세요
5. 면책 조항이나 "투자 판단은 본인 책임" 같은 문구는 절대 포함하지 마세요 (별도로 추가됨)

## 절대 금지 표현
- "~할 것으로 예상됩니다" → 수치 기반 서술로 대체 (예: "전일 대비 +1.2% 상승했다")
- "안정적인 [상승/하락]세" → 실제 등락률 % 명시 (예: "+0.8%로 소폭 상승했다")
- "긍정적/부정적인 영향" → 구체적 지표와 수치로 대체 (예: "달러 인덱스 0.3p 하락이 원화 강세 요인으로 작용했다")
- "큰 변동성을 보였습니다" → 고가-저가 스프레드 % 명시 (예: "고가 대비 저가 차이 4.2%의 변동폭을 기록했다")
- "주목할 필요가 있습니다" → 근거 없으면 삭제, 있으면 근거와 함께 서술

## 필수 규칙
- 모든 평가 문장에 수치 근거 포함 (수치 없는 평가 문장 작성 금지)
- 등락률 ±3% 이상 종목은 원인 분석 필수 (단순 수치 나열 금지)
- 각 종목은 서로 다른 관점으로 서술 (동일 톤·패턴 반복 금지)

출력 형식: 마크다운 (## 소제목 사용)"""

AI_MORNING_PROMPT = """아래는 오늘 모닝 브리핑을 위해 수집된 시장 데이터입니다.

{briefing_data}

위 데이터를 바탕으로 다음 4개 섹션을 작성해주세요:

1. **전일 글로벌 & 국내 시장 요약**
   - 전일 미국 시장 분위기, 달러/금리 움직임, 글로벌 주요 이벤트를 뉴스와 거시지표를 근거로 서술하세요
   - KOSPI/KOSDAQ 전일 마감과의 연관성을 짚어주세요

2. **오늘의 관전 포인트**
   - 장 시작 전 주목할 국내외 이슈 2~3가지
   - 오늘 발표 예정인 경제지표나 이벤트(뉴스 기반)가 있으면 포함하세요

3. **관심 종목 시사점**
   - 데이터에 있는 관심 종목 **전종목**을 반드시 언급하세요
   - 전일 등락률, 고가/저가, 공시 여부를 근거로 오늘 장 주목 포인트를 서술하세요

4. **오늘 전략**
   - 시장 색깔에 맞는 대응 전략 2~3가지

간결하게 핵심만 작성해주세요."""

AI_MIDDAY_PROMPT = """아래는 오늘 미드데이 브리핑을 위해 수집된 장중 시장 데이터입니다.

{briefing_data}

위 데이터를 바탕으로 다음 4개 섹션을 작성해주세요:

1. **장중 시장 흐름**
   - 오전장 KOSPI/KOSDAQ 움직임과 현재 시장 분위기
   - 환율·금리 움직임이 장중 흐름에 미치는 영향을 서술하세요
   - 오늘 오전 발표된 주요 이슈나 뉴스(국내외)를 반영하세요

2. **주목할 변화**
   - 오전장 기준 눈에 띄는 변동 종목이나 업종 흐름
   - 오전 발표된 공시나 뉴스 중 장에 영향을 준 이슈

3. **관심 종목 체크**
   - 데이터에 있는 관심 종목 **전종목**을 반드시 언급하세요
   - 현재 등락률, 고가/저가 스프레드, 거래량을 근거로 장중 흐름과 대응 포인트를 작성하세요

4. **오후장 전망**
   - 후장에 주목할 포인트와 시나리오 2가지(상승/하락 시 대응)

간결하게 핵심만 작성해주세요."""

AI_AFTERMARKET_PROMPT = """아래는 오늘 애프터 마켓 브리핑을 위해 수집된 시장 데이터입니다.

{briefing_data}

위 데이터를 바탕으로 다음 4개 섹션을 작성해주세요:

1. **글로벌 & 국내 시장 총평**
   - 오늘 글로벌 주요 이슈(미국 금리·달러 움직임, 주요국 정책 발표, 외교/회담, 지정학 리스크 등)와 그것이 국내 시장에 미친 영향을 먼저 서술하세요
   - KOSPI/KOSDAQ 지수 흐름과 금리·환율 데이터를 연결해 오늘 장의 전반적인 색깔을 평가하세요
   - 뉴스에서 포착된 주요 정책·이벤트(국내외 불문)를 1~2문장으로 요약하세요

2. **주요 이슈 분석**
   - 시장에 영향을 준 이슈를 2~4개 항목으로 정리하세요
   - 각 이슈가 업종/종목에 미치는 실질 영향을 짧게 서술하세요

3. **관심 종목 리뷰**
   - 데이터에 있는 관심 종목 **전종목**을 반드시 언급하세요
   - 종가(등락률), 고가/저가 스프레드, 거래량을 근거로 당일 흐름을 평가하세요
   - 등락률 ±3% 이상이거나 고저 스프레드가 5% 이상인 종목은 원인을 반드시 분석하세요

4. **내일 전략**
   - 내일 주목할 매크로 이벤트 또는 종목 이슈를 짚어주세요
   - 구체적 대응 포인트 2~3개로 마무리하세요

간결하게 핵심만 작성해주세요."""


class BriefingGenerator:
    """일일 마켓 브리핑 생성기"""

    def __init__(self):
        # 데이터 수집기 초기화
        self.dart = DartCollector()
        self.krx = KrxCollector()
        self.ecos = EcosCollector()
        self.news = NewsCollector()

    def collect_all_data(self, briefing_type: str = "aftermarket") -> dict:
        """
        모든 데이터 수집

        Args:
            briefing_type: "morning", "midday", 또는 "aftermarket"

        Returns:
            수집된 데이터 dict
        """
        settings = BRIEFING_SETTINGS[briefing_type]
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "briefing_type": briefing_type,
            "sections": {}
        }

        # KRX 대상 날짜 결정
        if briefing_type == "morning":
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            krx_target_date = yesterday
        else:  # midday, aftermarket
            krx_target_date = datetime.now().strftime("%Y%m%d")

        dart_days_back = settings["days_back"]

        # DART 공시
        print("  - DART 공시 수집 중...")
        if self.dart.is_available():
            disclosures = self.dart.get_recent_disclosures(days_back=dart_days_back)
            watchlist_disc = self.dart.get_watchlist_disclosures(days_back=dart_days_back)
            data["sections"]["dart"] = {
                "all_disclosures": len(disclosures),
                "watchlist_disclosures": watchlist_disc,
                "formatted": self.dart.format_for_briefing(watchlist_disc)
            }
        else:
            data["sections"]["dart"] = {"formatted": "DART API 키가 설정되지 않았습니다."}

        # KRX 시세
        print("  - KRX 시세 수집 중...")
        if self.krx.is_available():
            data["sections"]["krx"] = {
                "market_summary": self.krx.get_market_summary(target_date=krx_target_date),
                "watchlist": self.krx.get_watchlist_data(target_date=krx_target_date),
                "formatted": self.krx.format_for_briefing(target_date=krx_target_date)
            }
        else:
            data["sections"]["krx"] = {"formatted": "PyKRX가 설치되지 않았습니다."}

        # ECOS 경제지표
        print("  - ECOS 경제지표 수집 중...")
        if self.ecos.is_available():
            data["sections"]["ecos"] = {
                "indicators": self.ecos.get_latest_indicators(),
                "formatted": self.ecos.format_for_briefing()
            }
        else:
            data["sections"]["ecos"] = {"formatted": "ECOS API 키가 설정되지 않았습니다."}

        # 뉴스
        print("  - 뉴스 RSS 수집 중...")
        if self.news.is_available():
            news_hours = settings["news_max_hours"]
            max_news = settings["max_news"]
            news_items = self.news.get_investment_news(max_hours=news_hours)
            data["sections"]["news"] = {
                "count": len(news_items),
                "items": news_items[:max_news],
                "formatted": self.news.format_for_briefing(max_news, max_hours=news_hours)
            }
        else:
            data["sections"]["news"] = {"formatted": "feedparser가 설치되지 않았습니다."}

        return data

    def generate_basic_briefing(self, data: dict) -> str:
        """
        기본 브리핑 생성 (AI 없이)

        Args:
            data: 수집된 데이터

        Returns:
            마크다운 브리핑 문자열
        """
        briefing_type = data.get("briefing_type", "aftermarket")

        if briefing_type == "morning":
            return self._generate_morning_briefing(data)
        elif briefing_type == "midday":
            return self._generate_midday_briefing(data)
        else:
            return self._generate_aftermarket_briefing(data)

    def _generate_morning_briefing(self, data: dict) -> str:
        """모닝 브리핑 템플릿"""
        sections = data.get("sections", {})
        settings = BRIEFING_SETTINGS["morning"]

        return f"""# {settings['title']}

**생성일시**: {data.get('timestamp', '')}
**목적**: {settings['description']}

---

## 1. 전일 시장 마감

{sections.get('krx', {}).get('formatted', '데이터 없음')}

---

## 2. 환율 / 금리

{sections.get('ecos', {}).get('formatted', '데이터 없음')}

---

## 3. 주요 공시 (DART)

{sections.get('dart', {}).get('formatted', '데이터 없음')}

---

## 4. 오전 주요 뉴스

{sections.get('news', {}).get('formatted', '데이터 없음')}

---

*본 모닝 브리핑은 자동 생성되었습니다. 투자 판단은 본인 책임 하에 이루어져야 합니다.*
"""

    def _generate_midday_briefing(self, data: dict) -> str:
        """미드데이 브리핑 템플릿"""
        sections = data.get("sections", {})
        settings = BRIEFING_SETTINGS["midday"]

        return f"""# {settings['title']}

**생성일시**: {data.get('timestamp', '')}
**목적**: {settings['description']}

---

## 1. 장중 시장 현황

{sections.get('krx', {}).get('formatted', '데이터 없음')}

---

## 2. 거시경제 지표

{sections.get('ecos', {}).get('formatted', '데이터 없음')}

---

## 3. 금일 주요 공시 (DART)

{sections.get('dart', {}).get('formatted', '데이터 없음')}

---

## 4. 주요 뉴스

{sections.get('news', {}).get('formatted', '데이터 없음')}

---

*본 미드데이 브리핑은 자동 생성되었습니다. 투자 판단은 본인 책임 하에 이루어져야 합니다.*
"""

    def _generate_aftermarket_briefing(self, data: dict) -> str:
        """애프터 마켓 브리핑 템플릿"""
        sections = data.get("sections", {})
        settings = BRIEFING_SETTINGS["aftermarket"]

        return f"""# {settings['title']}

**생성일시**: {data.get('timestamp', '')}
**목적**: {settings['description']}

---

## 1. 금일 시장 동향

{sections.get('krx', {}).get('formatted', '데이터 없음')}

---

## 2. 거시경제 지표

{sections.get('ecos', {}).get('formatted', '데이터 없음')}

---

## 3. 금일 주요 공시 (DART)

{sections.get('dart', {}).get('formatted', '데이터 없음')}

---

## 4. 오후 주요 뉴스

{sections.get('news', {}).get('formatted', '데이터 없음')}

---

*본 애프터 마켓 브리핑은 자동 생성되었습니다. 투자 판단은 본인 책임 하에 이루어져야 합니다.*
"""

    def generate_ai_analysis(self, briefing: str, briefing_type: str) -> str:
        """
        OpenAI API를 사용한 AI 분석 생성

        Args:
            briefing: 기본 브리핑 텍스트
            briefing_type: "morning" 또는 "aftermarket"

        Returns:
            AI 분석 마크다운 문자열
        """
        if not AI_ENABLED:
            return ""

        if not OPENAI_API_KEY:
            print("  [AI] OpenAI API 키가 설정되지 않았습니다.")
            return ""

        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)

            # 브리핑 유형별 프롬프트 선택
            if briefing_type == "morning":
                user_prompt = AI_MORNING_PROMPT.format(briefing_data=briefing)
            elif briefing_type == "midday":
                user_prompt = AI_MIDDAY_PROMPT.format(briefing_data=briefing)
            else:
                user_prompt = AI_AFTERMARKET_PROMPT.format(briefing_data=briefing)

            print(f"  [AI] {AI_MODEL} 모델로 분석 요청 중...")

            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": AI_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE,
            )

            analysis = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else "N/A"
            print(f"  [AI] 분석 완료 (토큰 사용: {tokens_used})")

            return f"""

---

## 5. AI 시장 분석

> 모델: `{AI_MODEL}` | 토큰: {tokens_used}

{analysis}
"""

        except ImportError:
            print("  [AI] openai 라이브러리가 설치되지 않았습니다. pip install openai")
            return ""
        except Exception as e:
            print(f"  [AI] 분석 오류: {e}")
            return ""

    def generate_and_save(self, briefing_type: str = "aftermarket", use_ai: bool = False) -> str:
        """
        브리핑 생성 및 저장

        Args:
            briefing_type: "morning", "midday", 또는 "aftermarket"
            use_ai: AI 분석 사용 여부 (--ai 플래그). AI_ENABLED=true일 때만 실제 동작

        Returns:
            저장된 파일 경로
        """
        settings = BRIEFING_SETTINGS[briefing_type]
        print(f"{settings['title']} 생성 시작...")

        # 데이터 수집
        print("1. 데이터 수집 중...")
        data = self.collect_all_data(briefing_type=briefing_type)

        # 브리핑 생성
        print("2. 브리핑 생성 중...")
        briefing = self.generate_basic_briefing(data)

        # AI 분석 (use_ai 플래그 + AI_ENABLED 설정 모두 필요)
        ai_section = ""
        if use_ai:
            if AI_ENABLED:
                print("3. AI 분석 생성 중...")
                ai_section = self.generate_ai_analysis(briefing, briefing_type)
            else:
                print("3. AI 분석 건너뜀 (AI_ENABLED=false)")
                print("   활성화: .env 파일에서 AI_ENABLED=true로 변경")

        # AI 분석을 면책조항 바로 앞에 삽입
        if ai_section:
            # "---\n\n*본 " 패턴을 찾아 그 앞에 AI 분석 삽입
            marker = "\n---\n\n*본 "
            if marker in briefing:
                idx = briefing.rfind(marker)
                briefing = briefing[:idx] + ai_section + briefing[idx:]
            else:
                briefing += ai_section

        # 파일 저장
        step_num = "4" if use_ai else "3"
        print(f"{step_num}. 파일 저장 중...")
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

        filename = f"{data['date']}_{settings['file_suffix']}.md"
        filepath = RESULTS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(briefing)

        print(f"브리핑 저장 완료: {filepath}")
        return str(filepath)


# 테스트용 코드
if __name__ == "__main__":
    generator = BriefingGenerator()

    print("=== 브리핑 생성 테스트 ===\n")

    # 모닝 브리핑
    filepath = generator.generate_and_save(briefing_type="morning")
    print(f"\n생성된 파일: {filepath}")
