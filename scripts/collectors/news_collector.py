"""
뉴스 RSS 피드 수집기

경제/금융 뉴스 RSS 피드를 수집하여 시장 동향을 파악합니다.
- 한국경제, 매일경제, 이데일리 등

설치: pip install feedparser
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import re

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    print("Warning: feedparser not installed. Run: pip install feedparser")

from config import NEWS_RSS_FEEDS


class NewsCollector:
    """뉴스 RSS 피드 수집기"""

    # 투자 관련 키워드 (필터링용)
    INVESTMENT_KEYWORDS = [
        "주식", "코스피", "코스닥", "증시", "금리", "환율",
        "삼성전자", "SK하이닉스", "반도체", "배당", "실적",
        "외국인", "기관", "매수", "매도", "상승", "하락",
        "IPO", "공모", "상장", "투자", "펀드", "ETF",
        "금통위", "기준금리", "인플레이션", "GDP"
    ]

    def __init__(self, feeds: Optional[dict] = None):
        """
        Args:
            feeds: RSS 피드 URL dict. None이면 기본 설정 사용
        """
        self.feeds = feeds or NEWS_RSS_FEEDS
        self.available = FEEDPARSER_AVAILABLE

    def is_available(self) -> bool:
        """라이브러리 사용 가능 여부"""
        return self.available

    def fetch_feed(self, url: str) -> list[dict]:
        """
        단일 RSS 피드 가져오기

        Args:
            url: RSS 피드 URL

        Returns:
            뉴스 기사 리스트
        """
        if not self.is_available():
            return []

        try:
            feed = feedparser.parse(url)
            articles = []

            for entry in feed.entries:
                # 발행일 파싱
                published = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d %H:%M")

                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": self._clean_html(entry.get("summary", "")),
                    "published": published,
                })

            return articles

        except Exception as e:
            print(f"RSS 피드 조회 오류 ({url}): {e}")
            return []

    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        clean = re.sub(r"<[^>]+>", "", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean[:200] + "..." if len(clean) > 200 else clean

    def fetch_all_feeds(self) -> dict[str, list[dict]]:
        """
        모든 RSS 피드 가져오기

        Returns:
            매체별 뉴스 기사 dict
        """
        all_news = {}

        for source_name, url in self.feeds.items():
            articles = self.fetch_feed(url)
            all_news[source_name] = articles

        return all_news

    def get_investment_news(self, max_hours: int = 24) -> list[dict]:
        """
        투자 관련 뉴스 필터링

        Args:
            max_hours: 최근 몇 시간 이내 뉴스만

        Returns:
            투자 관련 뉴스 리스트
        """
        all_news = self.fetch_all_feeds()
        investment_news = []
        cutoff_time = datetime.now() - timedelta(hours=max_hours)

        for source, articles in all_news.items():
            for article in articles:
                # 키워드 필터링
                title = article.get("title", "")
                summary = article.get("summary", "")
                content = f"{title} {summary}"

                is_investment_related = any(
                    keyword in content for keyword in self.INVESTMENT_KEYWORDS
                )

                if is_investment_related:
                    article["source"] = source
                    investment_news.append(article)

        # 최신순 정렬
        investment_news.sort(key=lambda x: x.get("published", ""), reverse=True)
        return investment_news

    def format_for_briefing(self, max_items: int = 10, max_hours: int = 24) -> str:
        """
        브리핑용 마크다운 포맷 생성

        Args:
            max_items: 최대 표시 개수
            max_hours: 최근 몇 시간 이내 뉴스

        Returns:
            마크다운 문자열
        """
        lines = ["### 주요 뉴스"]

        if not self.is_available():
            return "feedparser가 설치되지 않았습니다. pip install feedparser"

        news = self.get_investment_news(max_hours=max_hours)

        if not news:
            return "최근 투자 관련 뉴스가 없습니다."

        for i, article in enumerate(news[:max_items]):
            title = article.get("title", "")
            source = article.get("source", "")
            link = article.get("link", "")

            lines.append(f"- [{title}]({link}) - {source}")

        if len(news) > max_items:
            lines.append(f"\n... 외 {len(news) - max_items}건")

        return "\n".join(lines)


# 테스트용 코드
if __name__ == "__main__":
    collector = NewsCollector()

    if not collector.is_available():
        print("feedparser를 사용할 수 없습니다.")
        print("설치: pip install feedparser")
    else:
        print("뉴스 RSS 수집 테스트...")

        # 전체 피드 가져오기
        print("\n=== 전체 뉴스 피드 ===")
        all_news = collector.fetch_all_feeds()
        for source, articles in all_news.items():
            print(f"\n{source}: {len(articles)}건")
            if articles:
                print(f"  최신: {articles[0].get('title', '')[:50]}...")

        # 투자 관련 뉴스
        print("\n=== 투자 관련 뉴스 ===")
        investment = collector.get_investment_news(max_hours=24)
        print(f"총 {len(investment)}건")
        for article in investment[:5]:
            print(f"- {article.get('title', '')[:50]}...")

        # 브리핑 포맷
        print("\n=== 브리핑 포맷 ===")
        print(collector.format_for_briefing(max_items=5))
