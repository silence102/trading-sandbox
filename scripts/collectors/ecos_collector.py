"""
ECOS (한국은행 경제통계시스템) 데이터 수집기

한국은행 ECOS API를 통해 거시경제 지표를 수집합니다.
- 기준금리
- 원/달러 환율
- 주요 경제지표

API 키 발급: https://ecos.bok.or.kr/api/
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import requests

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import ECOS_API_KEY, ECOS_STAT_CODES


class EcosCollector:
    """한국은행 ECOS 경제통계 수집기"""

    BASE_URL = "https://ecos.bok.or.kr/api/StatisticSearch"

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: ECOS API 키. None이면 환경변수에서 로드
        """
        self.api_key = api_key or ECOS_API_KEY

    def is_available(self) -> bool:
        """API 사용 가능 여부 확인"""
        return bool(self.api_key)

    def get_stat_data(
        self,
        stat_code: str,
        item_code: str,
        start_date: str,
        end_date: str,
        period: str = "D"  # D=일별, M=월별, Q=분기별, A=연도별
    ) -> list[dict]:
        """
        통계 데이터 조회

        Args:
            stat_code: 통계표코드
            item_code: 통계항목코드
            start_date: 시작일 (YYYYMMDD 또는 YYYYMM)
            end_date: 종료일
            period: 주기 (D/M/Q/A)

        Returns:
            통계 데이터 리스트
        """
        if not self.is_available():
            return []

        url = (
            f"{self.BASE_URL}/{self.api_key}/json/kr/1/100/"
            f"{stat_code}/{period}/{start_date}/{end_date}/{item_code}"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "StatisticSearch" in data:
                rows = data["StatisticSearch"].get("row", [])
                return rows
            return []

        except Exception as e:
            print(f"ECOS 조회 오류: {e}")
            return []

    def get_base_rate(self, days_back: int = 30) -> list[dict]:
        """
        한국은행 기준금리 조회

        Args:
            days_back: 며칠 전 데이터까지

        Returns:
            기준금리 데이터
        """
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        # 기준금리 통계코드
        return self.get_stat_data(
            stat_code="722Y001",
            item_code="0101000",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_exchange_rate(self, days_back: int = 7) -> list[dict]:
        """
        원/달러 환율 조회

        Args:
            days_back: 며칠 전 데이터까지

        Returns:
            환율 데이터
        """
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        # 원/달러 환율 통계코드
        return self.get_stat_data(
            stat_code="731Y003",
            item_code="0000001",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_latest_indicators(self) -> dict:
        """
        최신 주요 경제지표 조회

        Returns:
            주요 지표 dict
        """
        indicators = {}

        # 기준금리
        base_rate = self.get_base_rate(days_back=30)
        if base_rate:
            latest = base_rate[-1]
            indicators["base_rate"] = {
                "value": float(latest.get("DATA_VALUE", 0)),
                "date": latest.get("TIME", ""),
                "unit": "%"
            }

        # 환율
        exchange = self.get_exchange_rate(days_back=7)
        if exchange:
            latest = exchange[-1]
            prev = exchange[-2] if len(exchange) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            change = current_val - prev_val

            indicators["usd_krw"] = {
                "value": current_val,
                "change": change,
                "date": latest.get("TIME", ""),
                "unit": "원"
            }

        return indicators

    def format_for_briefing(self) -> str:
        """
        브리핑용 마크다운 포맷 생성

        Returns:
            마크다운 문자열
        """
        lines = ["### 거시경제 지표"]
        indicators = self.get_latest_indicators()

        if not indicators:
            if not self.is_available():
                return "ECOS API 키가 설정되지 않았습니다. .env 파일에 ECOS_API_KEY를 설정하세요."
            return "거시경제 지표를 조회할 수 없습니다."

        # 기준금리
        if "base_rate" in indicators:
            rate = indicators["base_rate"]
            lines.append(f"- **기준금리**: {rate['value']:.2f}%")

        # 환율
        if "usd_krw" in indicators:
            fx = indicators["usd_krw"]
            change_sign = "+" if fx["change"] >= 0 else ""
            lines.append(
                f"- **원/달러 환율**: {fx['value']:,.2f}원 "
                f"({change_sign}{fx['change']:,.2f}원)"
            )

        return "\n".join(lines)


# 테스트용 코드
if __name__ == "__main__":
    collector = EcosCollector()

    if not collector.is_available():
        print("ECOS API를 사용할 수 없습니다.")
        print("1. https://ecos.bok.or.kr/api/ 에서 API 키 발급")
        print("2. .env 파일에 ECOS_API_KEY 설정")
    else:
        print("ECOS API 연결 테스트...")

        # 최신 지표 조회
        print("\n=== 최신 경제지표 ===")
        indicators = collector.get_latest_indicators()
        for key, value in indicators.items():
            print(f"{key}: {value}")

        # 브리핑 포맷
        print("\n=== 브리핑 포맷 ===")
        print(collector.format_for_briefing())
