"""
DART (전자공시시스템) 데이터 수집기

DART API를 통해 기업 공시 정보를 수집합니다.
- 실적 발표, 배당, M&A, 유상증자 등 주요 공시
- 관심 종목의 최신 공시 모니터링

API 키 발급: https://opendart.fss.or.kr/
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import OpenDartReader
    DART_AVAILABLE = True
except ImportError:
    DART_AVAILABLE = False
    print("Warning: OpenDartReader not installed. Run: pip install opendartreader")

from config import DART_API_KEY, WATCHLIST_STOCKS


class DartCollector:
    """DART 공시 데이터 수집기"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: DART API 키. None이면 환경변수에서 로드
        """
        self.api_key = api_key or DART_API_KEY
        self.dart = None

        if DART_AVAILABLE and self.api_key:
            self.dart = OpenDartReader(self.api_key)

    def is_available(self) -> bool:
        """API 사용 가능 여부 확인"""
        return self.dart is not None

    def get_recent_disclosures(
        self,
        corp_code: Optional[str] = None,
        days_back: int = 1
    ) -> list[dict]:
        """
        최근 공시 목록 조회

        Args:
            corp_code: 종목 코드 (None이면 전체)
            days_back: 며칠 전까지 조회할지

        Returns:
            공시 목록 (dict의 list)
        """
        if not self.is_available():
            return []

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        try:
            # 공시 목록 조회
            if corp_code:
                df = self.dart.list(corp_code,
                                   start=start_date.strftime("%Y%m%d"),
                                   end=end_date.strftime("%Y%m%d"))
            else:
                df = self.dart.list(start=start_date.strftime("%Y%m%d"),
                                   end=end_date.strftime("%Y%m%d"))

            if df is None or df.empty:
                return []

            # DataFrame을 dict 리스트로 변환
            disclosures = df.to_dict("records")
            return disclosures

        except Exception as e:
            print(f"DART 공시 조회 오류: {e}")
            return []

    def get_watchlist_disclosures(self, days_back: int = 1) -> list[dict]:
        """
        관심 종목의 공시 조회

        Args:
            days_back: 며칠 전까지 조회할지

        Returns:
            관심 종목 공시 목록
        """
        all_disclosures = []

        for stock_code in WATCHLIST_STOCKS:
            disclosures = self.get_recent_disclosures(stock_code, days_back)
            all_disclosures.extend(disclosures)

        # 날짜 기준 정렬 (최신순)
        all_disclosures.sort(key=lambda x: x.get("rcept_dt", ""), reverse=True)
        return all_disclosures

    def get_company_info(self, corp_code: str) -> dict:
        """
        기업 기본 정보 조회

        Args:
            corp_code: 종목 코드

        Returns:
            기업 정보 dict
        """
        if not self.is_available():
            return {}

        try:
            info = self.dart.company(corp_code)
            if info is not None:
                return info.to_dict()
            return {}
        except Exception as e:
            print(f"기업 정보 조회 오류: {e}")
            return {}

    def get_financial_statements(
        self,
        corp_code: str,
        year: int,
        report_code: str = "11011"  # 11011=사업보고서
    ) -> dict:
        """
        재무제표 조회

        Args:
            corp_code: 종목 코드
            year: 조회 연도
            report_code: 보고서 코드 (11011=사업, 11012=반기, 11013=1분기, 11014=3분기)

        Returns:
            재무제표 데이터
        """
        if not self.is_available():
            return {}

        try:
            fs = self.dart.finstate(corp_code, year, reprt_code=report_code)
            if fs is not None and not fs.empty:
                return fs.to_dict("records")
            return {}
        except Exception as e:
            print(f"재무제표 조회 오류: {e}")
            return {}

    def format_for_briefing(self, disclosures: list[dict], max_items: int = 20) -> str:
        """
        브리핑용 마크다운 포맷 생성

        Args:
            disclosures: 공시 목록
            max_items: 최대 표시 개수

        Returns:
            마크다운 문자열
        """
        if not disclosures:
            return "공시 내역이 없습니다."

        lines = []
        for i, disc in enumerate(disclosures[:max_items]):
            corp_name = disc.get("corp_name", "알 수 없음")
            report_nm = disc.get("report_nm", "")
            rcept_dt = disc.get("rcept_dt", "")

            # 날짜 포맷팅
            if rcept_dt:
                formatted_date = f"{rcept_dt[:4]}-{rcept_dt[4:6]}-{rcept_dt[6:]}"
            else:
                formatted_date = ""

            lines.append(f"- **{corp_name}**: {report_nm} ({formatted_date})")

        if len(disclosures) > max_items:
            lines.append(f"\n... 외 {len(disclosures) - max_items}건")

        return "\n".join(lines)


# 테스트용 코드
if __name__ == "__main__":
    collector = DartCollector()

    if not collector.is_available():
        print("DART API를 사용할 수 없습니다.")
        print("1. OpenDartReader 설치: pip install opendartreader")
        print("2. .env 파일에 DART_API_KEY 설정")
    else:
        print("DART API 연결 성공!")

        # 최근 공시 조회 테스트
        print("\n=== 최근 공시 (전체) ===")
        disclosures = collector.get_recent_disclosures(days_back=1)
        print(f"총 {len(disclosures)}건의 공시")

        # 관심 종목 공시 조회
        print("\n=== 관심 종목 공시 ===")
        watchlist = collector.get_watchlist_disclosures(days_back=7)
        print(collector.format_for_briefing(watchlist, max_items=5))
