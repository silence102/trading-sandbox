#!/usr/bin/env python3
"""
투자 정보 자동화 파이프라인 - 메인 실행 파일

사용법:
    # 기본 브리핑 생성 (AI 없이)
    python main.py

    # AI 분석 포함 브리핑 생성
    python main.py --ai

    # 스케줄러로 자동 실행
    python main.py --schedule

    # 개별 수집기 테스트
    python main.py --test dart
    python main.py --test krx
    python main.py --test ecos
    python main.py --test news
"""
import sys
import argparse
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from briefing_generator import BriefingGenerator
from collectors import DartCollector, KrxCollector, EcosCollector, NewsCollector


def run_briefing(use_ai: bool = False):
    """브리핑 생성 실행"""
    generator = BriefingGenerator()
    filepath = generator.generate_and_save(use_ai=use_ai)
    print(f"\n완료! 파일 위치: {filepath}")


def run_scheduler():
    """스케줄러로 자동 실행"""
    try:
        import schedule
        import time
    except ImportError:
        print("schedule 라이브러리가 필요합니다.")
        print("설치: pip install schedule")
        return

    def job():
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 브리핑 생성 시작...")
        run_briefing(use_ai=False)

    # 매일 18:00에 실행
    schedule.every().day.at("18:00").do(job)

    print("스케줄러 시작 (매일 18:00에 브리핑 생성)")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    # 즉시 한 번 실행
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)


def test_collector(collector_name: str):
    """개별 수집기 테스트"""
    print(f"=== {collector_name.upper()} 수집기 테스트 ===\n")

    if collector_name == "dart":
        collector = DartCollector()
        if not collector.is_available():
            print("DART API 키가 설정되지 않았습니다.")
            print("1. https://opendart.fss.or.kr/ 에서 API 키 발급")
            print("2. .env 파일에 DART_API_KEY 설정")
            return

        print("최근 공시 조회 중...")
        disclosures = collector.get_recent_disclosures(days_back=1)
        print(f"총 {len(disclosures)}건의 공시\n")
        print(collector.format_for_briefing(disclosures[:5]))

    elif collector_name == "krx":
        collector = KrxCollector()
        if not collector.is_available():
            print("PyKRX가 설치되지 않았습니다.")
            print("설치: pip install pykrx")
            return

        print("시장 데이터 조회 중...")
        print(collector.format_for_briefing())

    elif collector_name == "ecos":
        collector = EcosCollector()
        if not collector.is_available():
            print("ECOS API 키가 설정되지 않았습니다.")
            print("1. https://ecos.bok.or.kr/api/ 에서 API 키 발급")
            print("2. .env 파일에 ECOS_API_KEY 설정")
            return

        print("경제지표 조회 중...")
        print(collector.format_for_briefing())

    elif collector_name == "news":
        collector = NewsCollector()
        if not collector.is_available():
            print("feedparser가 설치되지 않았습니다.")
            print("설치: pip install feedparser")
            return

        print("뉴스 RSS 수집 중...")
        print(collector.format_for_briefing(max_items=5))

    else:
        print(f"알 수 없는 수집기: {collector_name}")
        print("사용 가능: dart, krx, ecos, news")


def show_status():
    """현재 설정 상태 표시"""
    print("=== 투자 정보 자동화 파이프라인 상태 ===\n")

    # DART
    dart = DartCollector()
    dart_status = "✓ 사용 가능" if dart.is_available() else "✗ API 키 필요"
    print(f"DART (전자공시): {dart_status}")

    # KRX
    krx = KrxCollector()
    krx_status = "✓ 사용 가능" if krx.is_available() else "✗ PyKRX 설치 필요"
    print(f"KRX (주식시세): {krx_status}")

    # ECOS
    ecos = EcosCollector()
    ecos_status = "✓ 사용 가능" if ecos.is_available() else "✗ API 키 필요"
    print(f"ECOS (경제지표): {ecos_status}")

    # News
    news = NewsCollector()
    news_status = "✓ 사용 가능" if news.is_available() else "✗ feedparser 설치 필요"
    print(f"뉴스 RSS: {news_status}")

    # Anthropic
    try:
        import anthropic
        from config import ANTHROPIC_API_KEY
        ai_status = "✓ 사용 가능" if ANTHROPIC_API_KEY else "✗ API 키 필요"
    except ImportError:
        ai_status = "✗ anthropic 설치 필요"
    print(f"Claude AI: {ai_status}")

    print("\n---")
    print("설정 방법: .env.example을 .env로 복사 후 API 키 입력")


def main():
    parser = argparse.ArgumentParser(
        description="투자 정보 자동화 파이프라인",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python main.py              기본 브리핑 생성
  python main.py --ai         AI 분석 포함 브리핑
  python main.py --schedule   스케줄러로 자동 실행
  python main.py --test dart  DART 수집기 테스트
  python main.py --status     현재 설정 상태 확인
        """
    )

    parser.add_argument(
        "--ai",
        action="store_true",
        help="Claude AI 분석 포함"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="스케줄러로 자동 실행 (매일 18:00)"
    )
    parser.add_argument(
        "--test",
        type=str,
        choices=["dart", "krx", "ecos", "news"],
        help="개별 수집기 테스트"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="현재 설정 상태 확인"
    )

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.test:
        test_collector(args.test)
    elif args.schedule:
        run_scheduler()
    else:
        run_briefing(use_ai=args.ai)


if __name__ == "__main__":
    main()
