"""
투자 정보 자동화 파이프라인 설정
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 경로
BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "notes" / "daily_briefing"

# API 키
DART_API_KEY = os.getenv("DART_API_KEY", "")
ECOS_API_KEY = os.getenv("ECOS_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# 관심 종목 리스트
WATCHLIST_STOCKS = os.getenv("WATCHLIST_STOCKS", "005930,000660").split(",")

# 뉴스 RSS 피드 URL
NEWS_RSS_FEEDS = {
    "한국경제": "https://www.hankyung.com/feed/all-news",
    "매일경제": "https://www.mk.co.kr/rss/30000001/",
    "이데일리": "https://rss.edaily.co.kr/edaily_economy.xml",
}

# ECOS 통계 코드 (자주 사용하는 지표)
ECOS_STAT_CODES = {
    "기준금리": "722Y001",      # 한국은행 기준금리
    "원달러환율": "731Y003",    # 원/달러 환율
    "코스피지수": "802Y001",    # KOSPI 지수
}

# 브리핑 생성 설정
BRIEFING_SETTINGS = {
    "max_disclosures": 20,      # 최대 공시 개수
    "max_news": 10,             # 최대 뉴스 개수
    "days_back": 1,             # 몇 일 전 데이터까지
}
