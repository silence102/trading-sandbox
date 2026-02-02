"""
리서치 리포트 자동화 파이프라인

크롤링 → PDF 추출 → AI 요약 전체 과정을 실행합니다.
"""

import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

from report_crawler import ReportCrawler
from pdf_extractor import PDFExtractor
from report_summarizer import ReportSummarizer

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            PROJECT_ROOT / "logs" / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)


class ReportPipeline:
    """리서치 리포트 자동화 파이프라인"""

    def __init__(self):
        # 로그 폴더 생성
        (PROJECT_ROOT / "logs").mkdir(exist_ok=True)

        self.crawler = ReportCrawler()
        self.extractor = PDFExtractor()
        self.summarizer = None  # API 키가 필요할 때 초기화

    def run(
        self,
        target_date: Optional[datetime] = None,
        skip_crawl: bool = False,
        skip_extract: bool = False
    ) -> Optional[Path]:
        """
        전체 파이프라인 실행

        Args:
            target_date: 대상 날짜 (기본값: 오늘)
            skip_crawl: 크롤링 단계 스킵 (이미 PDF가 있는 경우)
            skip_extract: 추출 단계 스킵 (이미 텍스트가 있는 경우)

        Returns:
            생성된 종합 리포트 경로
        """
        target_date = target_date or datetime.now()
        date_str = target_date.strftime("%Y-%m-%d")

        logger.info(f"{'='*50}")
        logger.info(f"리서치 리포트 자동화 파이프라인 시작")
        logger.info(f"대상 날짜: {date_str}")
        logger.info(f"{'='*50}")

        # Step 1: 크롤링
        if not skip_crawl:
            logger.info("\n[Step 1/3] 리포트 크롤링")
            try:
                downloaded_files = self.crawler.crawl(target_date)
                logger.info(f"다운로드 완료: {len(downloaded_files)}개 파일")
            except Exception as e:
                logger.error(f"크롤링 실패: {e}")
                logger.info("크롤링을 건너뛰고 기존 파일로 계속합니다")
        else:
            logger.info("\n[Step 1/3] 크롤링 스킵")

        # Step 2: PDF 텍스트 추출
        if not skip_extract:
            logger.info("\n[Step 2/3] PDF 텍스트 추출")
            try:
                extracted_files = self.extractor.extract_batch()
                logger.info(f"추출 완료: {len(extracted_files)}개 파일")
            except Exception as e:
                logger.error(f"PDF 추출 실패: {e}")
                return None
        else:
            logger.info("\n[Step 2/3] 추출 스킵")

        # Step 3: AI 요약
        logger.info("\n[Step 3/3] AI 요약 생성")
        try:
            self.summarizer = ReportSummarizer()
            report_file = self.summarizer.create_daily_report(target_date)

            if report_file:
                logger.info(f"종합 리포트 생성 완료: {report_file}")
            else:
                logger.warning("종합 리포트 생성 실패")

            return report_file

        except ValueError as e:
            logger.error(f"요약 실패: {e}")
            logger.info("ANTHROPIC_API_KEY를 .env 파일에 설정하세요")
            return None
        except Exception as e:
            logger.error(f"요약 실패: {e}")
            return None

    def run_scheduled(self):
        """
        스케줄러용 실행 함수

        매일 정해진 시간에 자동 실행됩니다.
        """
        import schedule
        import time

        def job():
            logger.info("스케줄된 작업 시작")
            self.run()
            logger.info("스케줄된 작업 완료")

        # 매일 오전 8시 실행
        schedule.every().day.at("08:00").do(job)

        logger.info("스케줄러 시작 (매일 08:00 실행)")
        logger.info("중지하려면 Ctrl+C를 누르세요")

        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """CLI 실행"""
    parser = argparse.ArgumentParser(
        description="한국투자증권 리서치 리포트 자동화 파이프라인"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="대상 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)"
    )
    parser.add_argument(
        "--skip-crawl",
        action="store_true",
        help="크롤링 단계 스킵"
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="PDF 추출 단계 스킵"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="스케줄러 모드 (매일 자동 실행)"
    )
    args = parser.parse_args()

    pipeline = ReportPipeline()

    if args.schedule:
        pipeline.run_scheduled()
    else:
        # 날짜 파싱
        target_date = None
        if args.date:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")

        # 파이프라인 실행
        report_file = pipeline.run(
            target_date=target_date,
            skip_crawl=args.skip_crawl,
            skip_extract=args.skip_extract
        )

        if report_file:
            print(f"\n{'='*50}")
            print(f"종합 리포트 생성 완료!")
            print(f"파일: {report_file}")
            print(f"{'='*50}")
        else:
            print("\n리포트 생성 실패")


if __name__ == "__main__":
    main()
