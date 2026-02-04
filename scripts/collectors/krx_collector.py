"""
KRX (한국거래소) 주식 데이터 수집기

PyKRX 라이브러리를 통해 주식 시세 데이터를 수집합니다.
- KOSPI/KOSDAQ 지수
- 개별 종목 시세, 거래량
- 업종별 등락률

설치: pip install pykrx
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from pykrx import stock
    PYKRX_AVAILABLE = True
except ImportError:
    PYKRX_AVAILABLE = False
    print("Warning: pykrx not installed. Run: pip install pykrx")

from config import WATCHLIST_STOCKS


class KrxCollector:
    """KRX 주식 데이터 수집기"""

    def __init__(self):
        self.available = PYKRX_AVAILABLE

    def is_available(self) -> bool:
        """라이브러리 사용 가능 여부"""
        return self.available

    def get_market_ohlcv(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> list[dict]:
        """
        종목 OHLCV(시가/고가/저가/종가/거래량) 조회

        Args:
            ticker: 종목 코드 (예: "005930")
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)

        Returns:
            OHLCV 데이터 리스트
        """
        if not self.is_available():
            return []

        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")

        try:
            df = stock.get_market_ohlcv(start_date, end_date, ticker)
            if df is None or df.empty:
                return []

            # 인덱스(날짜)를 컬럼으로 변환
            df = df.reset_index()
            df["날짜"] = df["날짜"].dt.strftime("%Y-%m-%d")
            return df.to_dict("records")

        except Exception as e:
            print(f"OHLCV 조회 오류 ({ticker}): {e}")
            return []

    def get_index_ohlcv(
        self,
        index_ticker: str = "1001",  # 1001=KOSPI, 2001=KOSDAQ
        days_back: int = 7
    ) -> list[dict]:
        """
        지수 OHLCV 조회

        Args:
            index_ticker: 지수 코드 (1001=KOSPI, 2001=KOSDAQ)
            days_back: 며칠 전 데이터까지

        Returns:
            지수 OHLCV 데이터
        """
        if not self.is_available():
            return []

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        try:
            df = stock.get_index_ohlcv(start_date, end_date, index_ticker)
            if df is None or df.empty:
                return []

            df = df.reset_index()
            df["날짜"] = df["날짜"].dt.strftime("%Y-%m-%d")
            return df.to_dict("records")

        except Exception as e:
            print(f"지수 조회 오류 ({index_ticker}): {e}")
            return []

    def get_market_cap(self, date: Optional[str] = None) -> list[dict]:
        """
        시가총액 상위 종목 조회

        Args:
            date: 조회 날짜 (YYYYMMDD), None이면 최근 영업일

        Returns:
            시가총액 데이터
        """
        if not self.is_available():
            return []

        if date is None:
            date = datetime.now().strftime("%Y%m%d")

        try:
            df = stock.get_market_cap(date)
            if df is None or df.empty:
                return []

            df = df.reset_index()
            return df.head(20).to_dict("records")  # 상위 20종목

        except Exception as e:
            print(f"시가총액 조회 오류: {e}")
            return []

    def get_ticker_name(self, ticker: str) -> str:
        """종목 코드로 종목명 조회"""
        if not self.is_available():
            return ticker

        try:
            return stock.get_market_ticker_name(ticker)
        except Exception:
            return ticker

    def get_watchlist_data(self, days_back: int = 1) -> list[dict]:
        """
        관심 종목의 최근 시세 조회

        Args:
            days_back: 며칠 전 데이터까지

        Returns:
            관심 종목 시세 데이터
        """
        results = []

        for ticker in WATCHLIST_STOCKS:
            ohlcv = self.get_market_ohlcv(
                ticker,
                start_date=(datetime.now() - timedelta(days=days_back + 5)).strftime("%Y%m%d"),
                end_date=datetime.now().strftime("%Y%m%d")
            )

            if ohlcv:
                latest = ohlcv[-1] if ohlcv else {}
                name = self.get_ticker_name(ticker)

                results.append({
                    "ticker": ticker,
                    "name": name,
                    "date": latest.get("날짜", ""),
                    "close": latest.get("종가", 0),
                    "change": latest.get("등락률", 0) if "등락률" in latest else 0,
                    "volume": latest.get("거래량", 0),
                })

        return results

    def get_market_summary(self) -> dict:
        """
        시장 전체 요약 (KOSPI, KOSDAQ)

        Returns:
            시장 요약 데이터
        """
        summary = {
            "kospi": {},
            "kosdaq": {},
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        # KOSPI 지수
        kospi = self.get_index_ohlcv("1001", days_back=3)
        if kospi:
            latest = kospi[-1]
            prev = kospi[-2] if len(kospi) > 1 else latest
            summary["kospi"] = {
                "close": latest.get("종가", 0),
                "change": latest.get("종가", 0) - prev.get("종가", 0),
                "change_pct": ((latest.get("종가", 0) / prev.get("종가", 1)) - 1) * 100 if prev.get("종가", 0) else 0,
            }

        # KOSDAQ 지수
        kosdaq = self.get_index_ohlcv("2001", days_back=3)
        if kosdaq:
            latest = kosdaq[-1]
            prev = kosdaq[-2] if len(kosdaq) > 1 else latest
            summary["kosdaq"] = {
                "close": latest.get("종가", 0),
                "change": latest.get("종가", 0) - prev.get("종가", 0),
                "change_pct": ((latest.get("종가", 0) / prev.get("종가", 1)) - 1) * 100 if prev.get("종가", 0) else 0,
            }

        return summary

    def format_for_briefing(self) -> str:
        """
        브리핑용 마크다운 포맷 생성

        Returns:
            마크다운 문자열
        """
        lines = []

        # 시장 요약
        summary = self.get_market_summary()
        kospi = summary.get("kospi", {})
        kosdaq = summary.get("kosdaq", {})

        lines.append("### 시장 지수")
        if kospi:
            change_sign = "+" if kospi.get("change", 0) >= 0 else ""
            lines.append(
                f"- **KOSPI**: {kospi.get('close', 0):,.2f} "
                f"({change_sign}{kospi.get('change', 0):,.2f}, "
                f"{change_sign}{kospi.get('change_pct', 0):.2f}%)"
            )
        if kosdaq:
            change_sign = "+" if kosdaq.get("change", 0) >= 0 else ""
            lines.append(
                f"- **KOSDAQ**: {kosdaq.get('close', 0):,.2f} "
                f"({change_sign}{kosdaq.get('change', 0):,.2f}, "
                f"{change_sign}{kosdaq.get('change_pct', 0):.2f}%)"
            )

        # 관심 종목
        watchlist = self.get_watchlist_data()
        if watchlist:
            lines.append("\n### 관심 종목")
            for item in watchlist:
                lines.append(
                    f"- **{item['name']}** ({item['ticker']}): "
                    f"{item['close']:,}원 (거래량: {item['volume']:,})"
                )

        return "\n".join(lines)


# 테스트용 코드
if __name__ == "__main__":
    collector = KrxCollector()

    if not collector.is_available():
        print("PyKRX를 사용할 수 없습니다.")
        print("설치: pip install pykrx")
    else:
        print("PyKRX 연결 성공!")

        # 시장 요약
        print("\n=== 시장 요약 ===")
        summary = collector.get_market_summary()
        print(f"KOSPI: {summary['kospi']}")
        print(f"KOSDAQ: {summary['kosdaq']}")

        # 관심 종목
        print("\n=== 관심 종목 ===")
        watchlist = collector.get_watchlist_data()
        for item in watchlist:
            print(f"{item['name']}: {item['close']:,}원")

        # 브리핑 포맷
        print("\n=== 브리핑 포맷 ===")
        print(collector.format_for_briefing())
