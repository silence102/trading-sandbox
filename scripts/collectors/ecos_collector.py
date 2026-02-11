"""
ECOS (한국은행 경제통계시스템) 데이터 수집기

한국은행 ECOS API를 통해 거시경제 지표를 수집합니다.
- 기준금리 (한국)
- 환율 (원/달러, 원/100엔, 원/유로, 원/파운드)
- 국고채 금리 (3년)
- 미국 기준금리 / 미국 10년물 국채 (FRED 공개 API)

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
        원/달러 환율 조회 (장시간 매매기준율)

        Args:
            days_back: 며칠 전 데이터까지

        Returns:
            환율 데이터
        """
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        # 원/달러 장시간 매매기준율
        return self.get_stat_data(
            stat_code="731Y003",
            item_code="0000002",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_jpy_rate(self, days_back: int = 7) -> list[dict]:
        """원/100엔 환율 조회"""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        return self.get_stat_data(
            stat_code="731Y003",
            item_code="0000006",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_eur_rate(self, days_back: int = 7) -> list[dict]:
        """원/유로 환율 조회"""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        return self.get_stat_data(
            stat_code="731Y003",
            item_code="0000007",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_gbp_rate(self, days_back: int = 7) -> list[dict]:
        """원/파운드 환율 조회 (영국 파운드 스털링)"""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        # 731Y001: 주요국통화의대원화환율, 0000014=영국 파운드
        return self.get_stat_data(
            stat_code="731Y001",
            item_code="0000014",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_bond_yield_3y(self, days_back: int = 7) -> list[dict]:
        """국고채 3년 금리 조회"""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
        return self.get_stat_data(
            stat_code="817Y002",
            item_code="010190000",
            start_date=start_date,
            end_date=end_date,
            period="D"
        )

    def get_us_rates(self) -> dict:
        """
        미국 기준금리 및 10년물 국채 수익률 조회 (FRED 공개 API)

        Returns:
            {"fed_funds": float, "us10y": float}
        """
        result = {}

        # 미국 기준금리 (FEDFUNDS, 월별)
        try:
            r = requests.get(
                "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS",
                timeout=8
            )
            if r.status_code == 200:
                lines = [l for l in r.text.strip().split("\n") if l and not l.startswith("DATE")]
                if lines:
                    last = lines[-1].split(",")
                    result["fed_funds"] = {
                        "value": float(last[1]),
                        "date": last[0],
                        "unit": "%"
                    }
        except Exception:
            pass

        # 미국 10년물 국채 (DGS10, 일별)
        try:
            r2 = requests.get(
                "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10",
                timeout=8
            )
            if r2.status_code == 200:
                lines2 = [l for l in r2.text.strip().split("\n") if l and not l.startswith("DATE")]
                # 마지막 유효 데이터 (. 이 아닌 값)
                for line in reversed(lines2):
                    parts = line.split(",")
                    if len(parts) == 2 and parts[1].strip() not in (".", ""):
                        result["us10y"] = {
                            "value": float(parts[1]),
                            "date": parts[0],
                            "unit": "%"
                        }
                        break
        except Exception:
            pass

        return result

    def get_latest_indicators(self) -> dict:
        """
        최신 주요 경제지표 조회

        Returns:
            주요 지표 dict
        """
        indicators = {}

        # 한국 기준금리
        base_rate = self.get_base_rate(days_back=30)
        if base_rate:
            latest = base_rate[-1]
            indicators["base_rate"] = {
                "value": float(latest.get("DATA_VALUE", 0)),
                "date": latest.get("TIME", ""),
                "unit": "%",
                "label": "한국 기준금리"
            }

        # 원/달러 환율
        exchange = self.get_exchange_rate(days_back=7)
        if exchange:
            latest = exchange[-1]
            prev = exchange[-2] if len(exchange) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            indicators["usd_krw"] = {
                "value": current_val,
                "change": current_val - prev_val,
                "date": latest.get("TIME", ""),
                "unit": "원",
                "label": "원/달러"
            }

        # 원/100엔 환율
        jpy = self.get_jpy_rate(days_back=7)
        if jpy:
            latest = jpy[-1]
            prev = jpy[-2] if len(jpy) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            indicators["jpy_krw"] = {
                "value": current_val,
                "change": current_val - prev_val,
                "date": latest.get("TIME", ""),
                "unit": "원",
                "label": "원/100엔"
            }

        # 원/유로 환율
        eur = self.get_eur_rate(days_back=7)
        if eur:
            latest = eur[-1]
            prev = eur[-2] if len(eur) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            indicators["eur_krw"] = {
                "value": current_val,
                "change": current_val - prev_val,
                "date": latest.get("TIME", ""),
                "unit": "원",
                "label": "원/유로"
            }

        # 원/파운드 환율
        gbp = self.get_gbp_rate(days_back=7)
        if gbp:
            latest = gbp[-1]
            prev = gbp[-2] if len(gbp) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            indicators["gbp_krw"] = {
                "value": current_val,
                "change": current_val - prev_val,
                "date": latest.get("TIME", ""),
                "unit": "원",
                "label": "원/파운드"
            }

        # 국고채 3년
        bond3y = self.get_bond_yield_3y(days_back=7)
        if bond3y:
            latest = bond3y[-1]
            prev = bond3y[-2] if len(bond3y) > 1 else latest
            current_val = float(latest.get("DATA_VALUE", 0))
            prev_val = float(prev.get("DATA_VALUE", 0))
            indicators["bond_3y"] = {
                "value": current_val,
                "change": current_val - prev_val,
                "date": latest.get("TIME", ""),
                "unit": "%",
                "label": "국고채 3년"
            }

        # 미국 기준금리 + 10년물 (FRED)
        us_rates = self.get_us_rates()
        indicators.update(us_rates)

        return indicators

    def format_for_briefing(self) -> str:
        """
        브리핑용 마크다운 포맷 생성

        Returns:
            마크다운 문자열
        """
        indicators = self.get_latest_indicators()

        if not indicators:
            if not self.is_available():
                return "ECOS API 키가 설정되지 않았습니다. .env 파일에 ECOS_API_KEY를 설정하세요."
            return "거시경제 지표를 조회할 수 없습니다."

        lines = []

        # --- 금리 ---
        lines.append("### 금리")

        if "base_rate" in indicators:
            rate = indicators["base_rate"]
            lines.append(f"- **한국 기준금리**: {rate['value']:.2f}%")

        if "bond_3y" in indicators:
            b = indicators["bond_3y"]
            sign = "+" if b["change"] >= 0 else ""
            lines.append(f"- **국고채 3년**: {b['value']:.3f}% ({sign}{b['change']:+.3f}%p)")

        if "fed_funds" in indicators:
            ff = indicators["fed_funds"]
            lines.append(f"- **미국 기준금리(FF)**: {ff['value']:.2f}% ({ff['date']} 기준)")

        if "us10y" in indicators:
            u10 = indicators["us10y"]
            lines.append(f"- **미국 10년물 국채**: {u10['value']:.3f}% ({u10['date']} 기준)")

        # --- 환율 ---
        lines.append("")
        lines.append("### 환율")

        if "usd_krw" in indicators:
            fx = indicators["usd_krw"]
            sign = "+" if fx["change"] >= 0 else ""
            lines.append(f"- **원/달러**: {fx['value']:,.1f}원 ({sign}{fx['change']:,.1f}원)")

        if "jpy_krw" in indicators:
            jpy = indicators["jpy_krw"]
            sign = "+" if jpy["change"] >= 0 else ""
            lines.append(f"- **원/100엔**: {jpy['value']:,.2f}원 ({sign}{jpy['change']:,.2f}원)")

        if "eur_krw" in indicators:
            eur = indicators["eur_krw"]
            sign = "+" if eur["change"] >= 0 else ""
            lines.append(f"- **원/유로**: {eur['value']:,.2f}원 ({sign}{eur['change']:,.2f}원)")

        if "gbp_krw" in indicators:
            gbp = indicators["gbp_krw"]
            sign = "+" if gbp["change"] >= 0 else ""
            lines.append(f"- **원/파운드**: {gbp['value']:,.2f}원 ({sign}{gbp['change']:,.2f}원)")

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
