"""
PDF 텍스트 추출기

PyMuPDF를 사용하여 PDF에서 텍스트를 추출합니다.
"""

import logging
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_PATH = PROJECT_ROOT / "notes" / "auto_reports"
DATA_EXTRACTED_PATH = PROJECT_ROOT / "notes" / "auto_reports"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """PDF 텍스트 추출기"""

    def __init__(self, output_path: Optional[Path] = None):
        self.output_path = output_path or DATA_EXTRACTED_PATH
        self.output_path.mkdir(parents=True, exist_ok=True)

    def extract_text(self, pdf_path: Path) -> str:
        """
        PDF에서 텍스트 추출

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            추출된 텍스트
        """
        if not pdf_path.exists():
            logger.error(f"파일이 존재하지 않습니다: {pdf_path}")
            return ""

        text_parts = []

        try:
            doc = fitz.open(pdf_path)
            logger.info(f"PDF 열기 성공: {pdf_path.name} ({len(doc)} 페이지)")

            for page_num, page in enumerate(doc, 1):
                # 텍스트 추출
                page_text = page.get_text("text")

                if page_text.strip():
                    text_parts.append(f"\n--- 페이지 {page_num} ---\n")
                    text_parts.append(page_text)

            doc.close()

            full_text = "".join(text_parts)
            logger.info(f"텍스트 추출 완료: {len(full_text)} 문자")

            return full_text

        except Exception as e:
            logger.error(f"PDF 추출 오류: {e}")
            return ""

    def extract_with_layout(self, pdf_path: Path) -> str:
        """
        레이아웃을 유지하며 텍스트 추출 (테이블 등)

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            추출된 텍스트 (레이아웃 유지)
        """
        if not pdf_path.exists():
            logger.error(f"파일이 존재하지 않습니다: {pdf_path}")
            return ""

        text_parts = []

        try:
            doc = fitz.open(pdf_path)

            for page_num, page in enumerate(doc, 1):
                # 블록 단위로 추출 (레이아웃 유지)
                blocks = page.get_text("blocks")

                text_parts.append(f"\n{'='*50}\n페이지 {page_num}\n{'='*50}\n")

                for block in blocks:
                    if block[6] == 0:  # 텍스트 블록
                        text = block[4].strip()
                        if text:
                            text_parts.append(text)
                            text_parts.append("\n")

            doc.close()

            return "".join(text_parts)

        except Exception as e:
            logger.error(f"PDF 추출 오류: {e}")
            return ""

    def extract_and_save(self, pdf_path: Path) -> Optional[Path]:
        """
        PDF에서 텍스트를 추출하고 파일로 저장

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            저장된 텍스트 파일 경로
        """
        text = self.extract_text(pdf_path)

        if not text:
            return None

        # 출력 파일명 생성
        output_file = self.output_path / f"{pdf_path.stem}.txt"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)

            logger.info(f"텍스트 저장 완료: {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"파일 저장 오류: {e}")
            return None

    def extract_batch(self, pdf_folder: Optional[Path] = None) -> list[Path]:
        """
        폴더 내 모든 PDF 파일 일괄 추출

        Args:
            pdf_folder: PDF 폴더 경로 (기본값: data/raw)

        Returns:
            저장된 텍스트 파일 경로 리스트
        """
        pdf_folder = pdf_folder or DATA_RAW_PATH
        saved_files = []

        pdf_files = list(pdf_folder.glob("*.pdf"))
        logger.info(f"{len(pdf_files)}개 PDF 파일 발견")

        for pdf_path in pdf_files:
            output_file = self.extract_and_save(pdf_path)
            if output_file:
                saved_files.append(output_file)

        logger.info(f"일괄 추출 완료: {len(saved_files)}개 파일")
        return saved_files


def main():
    """CLI 실행"""
    import argparse

    parser = argparse.ArgumentParser(description="PDF 텍스트 추출기")
    parser.add_argument(
        "--file",
        type=str,
        help="추출할 PDF 파일 경로"
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="일괄 추출할 폴더 경로"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="출력 경로"
    )
    parser.add_argument(
        "--layout",
        action="store_true",
        help="레이아웃 유지 모드"
    )
    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None
    extractor = PDFExtractor(output_path=output_path)

    if args.file:
        pdf_path = Path(args.file)
        if args.layout:
            text = extractor.extract_with_layout(pdf_path)
            print(text)
        else:
            output_file = extractor.extract_and_save(pdf_path)
            if output_file:
                print(f"저장됨: {output_file}")

    elif args.folder:
        pdf_folder = Path(args.folder)
        files = extractor.extract_batch(pdf_folder)
        print(f"\n추출된 파일:")
        for f in files:
            print(f"  - {f}")

    else:
        # 기본: data/raw 폴더 일괄 추출
        files = extractor.extract_batch()
        print(f"\n추출된 파일:")
        for f in files:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
