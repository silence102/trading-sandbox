"""
일일 마켓 브리핑 생성기

수집된 데이터를 통합하여 일일 마켓 브리핑을 생성합니다.
Claude API를 사용하여 AI 기반 분석 및 요약을 제공합니다.
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic not installed. Run: pip install anthropic")

from config import ANTHROPIC_API_KEY, RESULTS_DIR, BRIEFING_SETTINGS
from collectors import DartCollector, KrxCollector, EcosCollector, NewsCollector


class BriefingGenerator:
    """일일 마켓 브리핑 생성기"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Anthropic API 키. None이면 환경변수에서 로드
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.client = None

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # 데이터 수집기 초기화
        self.dart = DartCollector()
        self.krx = KrxCollector()
        self.ecos = EcosCollector()
        self.news = NewsCollector()

    def collect_all_data(self) -> dict:
        """
        모든 데이터 수집

        Returns:
            수집된 데이터 dict
        """
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sections": {}
        }

        # DART 공시
        print("  - DART 공시 수집 중...")
        if self.dart.is_available():
            disclosures = self.dart.get_recent_disclosures(days_back=1)
            watchlist_disc = self.dart.get_watchlist_disclosures(days_back=1)
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
                "market_summary": self.krx.get_market_summary(),
                "watchlist": self.krx.get_watchlist_data(),
                "formatted": self.krx.format_for_briefing()
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
            news_items = self.news.get_investment_news(max_hours=24)
            data["sections"]["news"] = {
                "count": len(news_items),
                "items": news_items[:BRIEFING_SETTINGS["max_news"]],
                "formatted": self.news.format_for_briefing(BRIEFING_SETTINGS["max_news"])
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
        sections = data.get("sections", {})

        briefing = f"""# 일일 마켓 브리핑

**생성일시**: {data.get('timestamp', '')}

---

## 1. 시장 동향

{sections.get('krx', {}).get('formatted', '데이터 없음')}

---

## 2. 거시경제 지표

{sections.get('ecos', {}).get('formatted', '데이터 없음')}

---

## 3. 주요 공시 (DART)

{sections.get('dart', {}).get('formatted', '데이터 없음')}

---

## 4. 주요 뉴스

{sections.get('news', {}).get('formatted', '데이터 없음')}

---

*본 브리핑은 자동 생성되었습니다. 투자 판단은 본인 책임 하에 이루어져야 합니다.*
"""
        return briefing

    def generate_ai_briefing(self, data: dict) -> str:
        """
        AI 기반 브리핑 생성 (Claude API 사용)

        Args:
            data: 수집된 데이터

        Returns:
            AI 분석이 포함된 마크다운 브리핑
        """
        if not self.client:
            print("Claude API를 사용할 수 없습니다. 기본 브리핑을 생성합니다.")
            return self.generate_basic_briefing(data)

        # 기본 브리핑 먼저 생성
        basic_briefing = self.generate_basic_briefing(data)

        # AI 분석 요청
        prompt = f"""다음은 오늘의 시장 데이터입니다. 이를 바탕으로 간결한 투자 포인트를 3-5개 정리해주세요.

{basic_briefing}

## 요청사항:
1. 오늘 시장의 핵심 포인트 3-5개
2. 관심 종목 관련 주요 이슈 (있다면)
3. 주의해야 할 리스크 요인 (있다면)

간결하고 실용적으로 작성해주세요. 마크다운 형식으로 출력해주세요."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            ai_analysis = message.content[0].text

            # AI 분석을 기본 브리핑에 추가
            final_briefing = f"""{basic_briefing}

---

## 5. AI 분석 요약

{ai_analysis}

---

*AI 분석은 Claude (Anthropic)에 의해 생성되었습니다.*
"""
            return final_briefing

        except Exception as e:
            print(f"AI 분석 생성 오류: {e}")
            return basic_briefing

    def generate_and_save(self, use_ai: bool = False) -> str:
        """
        브리핑 생성 및 저장

        Args:
            use_ai: AI 분석 사용 여부

        Returns:
            저장된 파일 경로
        """
        print("브리핑 생성 시작...")

        # 데이터 수집
        print("1. 데이터 수집 중...")
        data = self.collect_all_data()

        # 브리핑 생성
        print("2. 브리핑 생성 중...")
        if use_ai:
            briefing = self.generate_ai_briefing(data)
        else:
            briefing = self.generate_basic_briefing(data)

        # 파일 저장
        print("3. 파일 저장 중...")
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

        filename = f"{data['date']}_마켓브리핑.md"
        filepath = RESULTS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(briefing)

        print(f"브리핑 저장 완료: {filepath}")
        return str(filepath)


# 테스트용 코드
if __name__ == "__main__":
    generator = BriefingGenerator()

    print("=== 브리핑 생성 테스트 ===\n")

    # 기본 브리핑 (AI 없이)
    filepath = generator.generate_and_save(use_ai=False)

    print(f"\n생성된 파일: {filepath}")
    print("\nAI 분석을 포함하려면 use_ai=True로 실행하세요.")
    print("(ANTHROPIC_API_KEY 설정 필요)")
