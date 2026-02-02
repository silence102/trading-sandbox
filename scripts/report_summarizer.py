"""
리포트 요약기

Claude API를 사용하여 리서치 리포트를 종합 요약합니다.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from anthropic import Anthropic
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
DATA_EXTRACTED_PATH = PROJECT_ROOT / "notes" / "auto_reports"
RESULTS_PATH = PROJECT_ROOT / "results" / "daily_reports"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 요약 프롬프트 템플릿
SUMMARY_PROMPT = """당신은 투자 분석 전문가입니다. 아래 한국투자증권 리서치 리포트들을 분석하여 종합 일일 리포트를 작성해주세요.

## 분석 요청사항

1. **핵심 요약**: 오늘의 주요 이슈 3-5개를 간결하게 정리
2. **테마별 분석**: 각 리포트의 주요 내용을 테마(경제, 채권, 글로벌, 중국 등)로 분류
3. **연관관계 분석**: 여러 리포트에서 공통적으로 언급되는 이슈나 상호 연관된 내용 파악
4. **투자 인사이트**: 실질적인 투자 판단에 도움이 되는 핵심 포인트
5. **주의사항**: 리스크 요인이나 불확실성 요소

## 출력 형식

마크다운 형식으로 작성해주세요:
- 헤더(#, ##, ###)를 활용한 구조화
- 불릿 포인트로 핵심 내용 정리
- 중요한 수치나 날짜는 강조(**굵게**)
- 투자 인사이트는 > 인용 블록 사용

## 리포트 내용

{report_contents}
"""


class ReportSummarizer:
    """리포트 요약기 (Claude API)"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        output_path: Optional[Path] = None
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

        self.client = Anthropic(api_key=self.api_key)
        self.output_path = output_path or RESULTS_PATH
        self.output_path.mkdir(parents=True, exist_ok=True)

    def load_extracted_texts(
        self,
        date: Optional[datetime] = None,
        folder: Optional[Path] = None
    ) -> dict[str, str]:
        """
        추출된 텍스트 파일 로드

        Args:
            date: 대상 날짜 (파일명 필터링용)
            folder: 텍스트 파일 폴더

        Returns:
            {파일명: 텍스트 내용} 딕셔너리
        """
        folder = folder or DATA_EXTRACTED_PATH
        texts = {}

        for txt_file in folder.glob("*.txt"):
            # 날짜 필터링 (선택적)
            if date:
                date_str = date.strftime("%Y%m%d")
                if date_str not in txt_file.name:
                    continue

            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    texts[txt_file.stem] = f.read()
                logger.info(f"텍스트 로드: {txt_file.name}")
            except Exception as e:
                logger.error(f"파일 읽기 오류: {txt_file.name} - {e}")

        logger.info(f"총 {len(texts)}개 텍스트 파일 로드")
        return texts

    def summarize(self, texts: dict[str, str]) -> str:
        """
        Claude API를 사용하여 리포트 요약

        Args:
            texts: {파일명: 텍스트 내용} 딕셔너리

        Returns:
            요약 결과 (마크다운)
        """
        if not texts:
            logger.warning("요약할 텍스트가 없습니다")
            return ""

        # 리포트 내용 조합
        report_contents = ""
        for name, content in texts.items():
            report_contents += f"\n\n### {name}\n\n{content[:15000]}"  # 토큰 제한 고려

        # 프롬프트 생성
        prompt = SUMMARY_PROMPT.format(report_contents=report_contents)

        logger.info("Claude API 요청 중...")

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = message.content[0].text
            logger.info(f"요약 완료: {len(summary)} 문자")
            return summary

        except Exception as e:
            logger.error(f"Claude API 오류: {e}")
            return ""

    def create_daily_report(
        self,
        date: Optional[datetime] = None,
        texts: Optional[dict[str, str]] = None
    ) -> Optional[Path]:
        """
        일일 종합 리포트 생성

        Args:
            date: 리포트 날짜 (기본값: 오늘)
            texts: 텍스트 딕셔너리 (None이면 자동 로드)

        Returns:
            생성된 리포트 파일 경로
        """
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")

        # 텍스트 로드
        if texts is None:
            texts = self.load_extracted_texts(date)

        if not texts:
            logger.warning(f"날짜 {date_str}에 해당하는 리포트가 없습니다")
            return None

        # 요약 생성
        summary = self.summarize(texts)

        if not summary:
            return None

        # 리포트 헤더 추가
        report_content = f"""# 일일 리서치 리포트 종합

**날짜**: {date_str}
**생성 시간**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**분석 리포트 수**: {len(texts)}개

---

{summary}

---

## 원본 리포트

| 파일명 | 상태 |
|--------|------|
"""
        for name in texts.keys():
            report_content += f"| {name} | 분석 완료 |\n"

        report_content += f"""
---

*이 리포트는 Claude API를 사용하여 자동 생성되었습니다.*
*리포트 원본의 저작권은 한국투자증권에 있습니다.*
"""

        # 파일 저장
        output_file = self.output_path / f"{date_str}_종합리포트.md"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)

            logger.info(f"일일 리포트 저장: {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"파일 저장 오류: {e}")
            return None


def main():
    """CLI 실행"""
    import argparse

    parser = argparse.ArgumentParser(description="리서치 리포트 요약기")
    parser.add_argument(
        "--date",
        type=str,
        help="대상 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)"
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="텍스트 파일 폴더 경로"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="출력 경로"
    )
    args = parser.parse_args()

    # 날짜 파싱
    target_date = None
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")

    # 경로 설정
    folder = Path(args.folder) if args.folder else None
    output_path = Path(args.output) if args.output else None

    # 요약기 실행
    try:
        summarizer = ReportSummarizer(output_path=output_path)
        texts = summarizer.load_extracted_texts(target_date, folder)
        report_file = summarizer.create_daily_report(target_date, texts)

        if report_file:
            print(f"\n일일 리포트 생성 완료: {report_file}")
        else:
            print("\n리포트 생성 실패")

    except ValueError as e:
        print(f"\n오류: {e}")
        print("ANTHROPIC_API_KEY를 .env 파일에 설정하세요.")


if __name__ == "__main__":
    main()
