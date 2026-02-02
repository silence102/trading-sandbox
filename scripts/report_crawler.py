"""
한국투자증권 리서치 리포트 크롤러

전략/이슈 리포트 페이지에서 PDF 파일을 자동으로 다운로드합니다.
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_PATH = PROJECT_ROOT / "notes" / "auto_reports"
DOWNLOAD_LOG_PATH = PROJECT_ROOT / "notes" / "auto_reports" / "download_log.json"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 리서치 페이지 URL
RESEARCH_URL = "https://securities.koreainvestment.com/main/research/research/Strategy.jsp?jkGubun=6"


class ReportCrawler:
    """한국투자증권 리서치 리포트 크롤러"""

    def __init__(self, download_path: Optional[Path] = None):
        self.download_path = download_path or DATA_RAW_PATH
        self.download_path.mkdir(parents=True, exist_ok=True)
        self.driver = None
        self.download_log = self._load_download_log()

    def _load_download_log(self) -> dict:
        """다운로드 기록 로드"""
        if DOWNLOAD_LOG_PATH.exists():
            with open(DOWNLOAD_LOG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"downloaded": []}

    def _save_download_log(self):
        """다운로드 기록 저장"""
        DOWNLOAD_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DOWNLOAD_LOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.download_log, f, ensure_ascii=False, indent=2)

    def _init_driver(self):
        """Selenium WebDriver 초기화"""
        chrome_options = Options()

        # 다운로드 설정
        prefs = {
            "download.default_directory": str(self.download_path.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,  # PDF 뷰어 대신 다운로드
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # 헤드리스 모드 (선택)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # User-Agent 설정
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        logger.info("WebDriver 초기화 완료")

    def _close_driver(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver 종료")

    def fetch_report_list(self, target_date: Optional[datetime] = None) -> list[dict]:
        """
        리포트 목록 가져오기

        Args:
            target_date: 가져올 날짜 (None이면 오늘)

        Returns:
            리포트 정보 리스트 [{"title": ..., "date": ..., "link": ...}, ...]
        """
        if not self.driver:
            self._init_driver()

        target_date = target_date or datetime.now()
        target_str = target_date.strftime("%Y.%m.%d")

        logger.info(f"리서치 페이지 접속: {RESEARCH_URL}")
        self.driver.get(RESEARCH_URL)

        reports = []

        try:
            # 페이지 로딩 대기
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table, .board-list, .list-table"))
            )
            time.sleep(2)  # 동적 콘텐츠 로딩 대기

            # 리포트 목록 파싱 (사이트 구조에 따라 조정 필요)
            # 일반적인 테이블 구조 시도
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr, .board-list li, .list-item")

            for row in rows:
                try:
                    # 날짜 추출
                    date_elem = row.find_element(By.CSS_SELECTOR, ".date, td:last-child, .reg-date")
                    date_text = date_elem.text.strip()

                    # 제목 및 링크 추출
                    title_elem = row.find_element(By.CSS_SELECTOR, "a, .title")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href") if title_elem.tag_name == "a" else ""

                    # 날짜 필터링
                    if target_str in date_text or date_text == target_str:
                        reports.append({
                            "title": title,
                            "date": date_text,
                            "link": link
                        })
                        logger.info(f"리포트 발견: {title} ({date_text})")

                except NoSuchElementException:
                    continue

            logger.info(f"총 {len(reports)}개 리포트 발견 (날짜: {target_str})")

        except TimeoutException:
            logger.warning("페이지 로딩 타임아웃")
        except Exception as e:
            logger.error(f"리포트 목록 파싱 오류: {e}")

        return reports

    def download_report(self, report: dict) -> Optional[Path]:
        """
        개별 리포트 PDF 다운로드

        Args:
            report: 리포트 정보 딕셔너리

        Returns:
            다운로드된 파일 경로 (실패 시 None)
        """
        if not report.get("link"):
            logger.warning(f"다운로드 링크 없음: {report.get('title')}")
            return None

        # 중복 다운로드 방지
        report_id = f"{report['date']}_{report['title']}"
        if report_id in self.download_log["downloaded"]:
            logger.info(f"이미 다운로드됨: {report['title']}")
            return None

        try:
            # 링크 클릭 또는 직접 접근
            if report["link"].endswith(".pdf"):
                self.driver.get(report["link"])
            else:
                # JavaScript 기반 다운로드 처리
                self.driver.execute_script(f"window.open('{report['link']}', '_blank');")

            # 다운로드 완료 대기
            time.sleep(3)

            # 다운로드된 파일 확인
            downloaded_files = list(self.download_path.glob("*.pdf"))
            if downloaded_files:
                latest_file = max(downloaded_files, key=lambda p: p.stat().st_mtime)

                # 다운로드 기록 저장
                self.download_log["downloaded"].append(report_id)
                self._save_download_log()

                logger.info(f"다운로드 완료: {latest_file.name}")
                return latest_file

        except Exception as e:
            logger.error(f"다운로드 오류: {e}")

        return None

    def crawl(self, target_date: Optional[datetime] = None) -> list[Path]:
        """
        크롤링 실행 (메인 함수)

        Args:
            target_date: 대상 날짜 (None이면 오늘)

        Returns:
            다운로드된 파일 경로 리스트
        """
        downloaded_files = []

        try:
            self._init_driver()

            # 리포트 목록 가져오기
            reports = self.fetch_report_list(target_date)

            # 각 리포트 다운로드
            for report in reports:
                file_path = self.download_report(report)
                if file_path:
                    downloaded_files.append(file_path)
                time.sleep(2)  # 과도한 요청 방지

            logger.info(f"크롤링 완료: {len(downloaded_files)}개 파일 다운로드")

        finally:
            self._close_driver()

        return downloaded_files


def main():
    """CLI 실행"""
    import argparse

    parser = argparse.ArgumentParser(description="한국투자증권 리서치 리포트 크롤러")
    parser.add_argument(
        "--date",
        type=str,
        help="대상 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="다운로드 경로"
    )
    args = parser.parse_args()

    # 날짜 파싱
    target_date = None
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    # 다운로드 경로
    download_path = Path(args.output) if args.output else None

    # 크롤러 실행
    crawler = ReportCrawler(download_path=download_path)
    files = crawler.crawl(target_date)

    print(f"\n다운로드된 파일:")
    for f in files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
