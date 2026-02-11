#!/usr/bin/env python3
"""
투자 정보 자동화 파이프라인 - 메인 실행 파일

사용법:
    # 모닝 브리핑 생성 (장 시작 전)
    python main.py --type morning

    # 미드데이 브리핑 생성 (장중)
    python main.py --type midday

    # 애프터 마켓 브리핑 생성 (장 마감 후, 기본값)
    python main.py --type aftermarket
    python main.py

    # 스케줄러로 자동 실행 (08:00 모닝, 12:30 미드데이, 18:00 애프터마켓)
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


def run_briefing(briefing_type: str = "aftermarket", use_ai: bool = False):
    """브리핑 생성 실행"""
    generator = BriefingGenerator()
    filepath = generator.generate_and_save(briefing_type=briefing_type, use_ai=use_ai)
    print(f"\n완료! 파일 위치: {filepath}")


def run_scheduler():
    """스케줄러로 자동 실행 (모닝 08:00, 미드데이 12:30, 애프터마켓 18:00)"""
    try:
        import schedule
        import time
    except ImportError:
        print("schedule 라이브러리가 필요합니다.")
        print("설치: pip install schedule")
        return

    def morning_job():
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 모닝 브리핑 생성 시작...")
        run_briefing(briefing_type="morning")

    def midday_job():
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 미드데이 브리핑 생성 시작...")
        run_briefing(briefing_type="midday")

    def aftermarket_job():
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 애프터 마켓 브리핑 생성 시작...")
        run_briefing(briefing_type="aftermarket")

    # 매일 08:00 모닝, 12:30 미드데이, 18:00 애프터마켓
    schedule.every().day.at("08:00").do(morning_job)
    schedule.every().day.at("12:30").do(midday_job)
    schedule.every().day.at("18:00").do(aftermarket_job)

    print("스케줄러 시작")
    print("  - 08:00 모닝 브리핑")
    print("  - 12:30 미드데이 브리핑")
    print("  - 18:00 애프터 마켓 브리핑")
    print("종료하려면 Ctrl+C를 누르세요.\n")

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
    dart_status = "[O] 사용 가능" if dart.is_available() else "[X] API 키 필요"
    print(f"DART (전자공시): {dart_status}")

    # KRX
    krx = KrxCollector()
    krx_status = "[O] 사용 가능" if krx.is_available() else "[X] PyKRX 설치 필요"
    print(f"KRX (주식시세): {krx_status}")

    # ECOS
    ecos = EcosCollector()
    ecos_status = "[O] 사용 가능" if ecos.is_available() else "[X] API 키 필요"
    print(f"ECOS (경제지표): {ecos_status}")

    # News
    news = NewsCollector()
    news_status = "[O] 사용 가능" if news.is_available() else "[X] feedparser 설치 필요"
    print(f"뉴스 RSS: {news_status}")

    # OpenAI
    from config import OPENAI_API_KEY, AI_ENABLED, AI_MODEL
    ai_key_ok = "[O]" if OPENAI_API_KEY else "[X]"
    ai_on_off = "ON" if AI_ENABLED else "OFF"
    print(f"OpenAI (ChatGPT): {ai_key_ok} API 키 {'등록됨' if OPENAI_API_KEY else '필요'} | AI 분석: {ai_on_off} | 모델: {AI_MODEL}")

    print("\n---")
    print("설정 방법: .env.example을 .env로 복사 후 API 키 입력")


def main():
    parser = argparse.ArgumentParser(
        description="투자 정보 자동화 파이프라인",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python main.py                          애프터 마켓 브리핑 생성 (기본)
  python main.py --type morning           모닝 브리핑 생성
  python main.py --type midday            미드데이 브리핑 생성
  python main.py --type aftermarket       애프터 마켓 브리핑 생성
  python main.py --type midday --ai       AI 분석 포함 미드데이 브리핑
  python main.py --schedule               스케줄러로 자동 실행
  python main.py --test dart              DART 수집기 테스트
  python main.py --status                 현재 설정 상태 확인
        """
    )

    parser.add_argument(
        "--type",
        type=str,
        choices=["morning", "midday", "aftermarket"],
        default="aftermarket",
        help="브리핑 유형: morning(모닝), midday(미드데이), aftermarket(애프터마켓, 기본값)"
    )
    parser.add_argument(
        "--ai",
        action="store_true",
        help="AI 분석 포함"
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="스케줄러로 자동 실행 (08:00 모닝 / 18:00 애프터마켓)"
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
        run_briefing(briefing_type=args.type, use_ai=args.ai)


if __name__ == "__main__":
    main()
