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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# AI 분석 설정
AI_ENABLED = os.getenv("AI_ENABLED", "false").lower() == "true"
AI_MODEL = "gpt-4o-mini"  # 비용 효율적 모델 (변경 가능: gpt-4o, gpt-4-turbo 등)
AI_MAX_TOKENS = 1500
AI_TEMPERATURE = 0.3  # 낮을수록 일관된 분석, 높을수록 창의적

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

# 브리핑 유형별 설정
BRIEFING_SETTINGS = {
    "morning": {
        "max_disclosures": 20,
        "max_news": 10,
        "news_max_hours": 16,       # 전일 오후 ~ 당일 오전 뉴스
        "days_back": 1,             # 전일 데이터
        "title": "모닝 브리핑",
        "file_suffix": "모닝브리핑",
        "description": "장 시작 전 투자 준비",
    },
    "aftermarket": {
        "max_disclosures": 20,
        "max_news": 10,
        "news_max_hours": 12,       # 당일 뉴스
        "days_back": 0,             # 당일 데이터
        "title": "애프터 마켓 브리핑",
        "file_suffix": "애프터마켓브리핑",
        "description": "금일 시장 마감 요약",
    },
}
