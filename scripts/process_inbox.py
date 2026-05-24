#!/usr/bin/env python3
"""
process_inbox.py — inbox/ 에 있는 PDF들을 일괄 재처리.

Usage:
    python scripts/process_inbox.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
INBOX = ROOT / "inbox"


def main():
    pdfs = list(INBOX.glob("*.pdf"))
    if not pdfs:
        print("inbox/ 가 비어 있습니다.")
        return

    print(f"{len(pdfs)}개 PDF 재처리 시작...")
    for pdf in pdfs:
        print(f"  처리 중: {pdf.name}")
        result = subprocess.run(
            ["python", str(ROOT / "scripts" / "process_pdf.py"), str(pdf)],
            capture_output=True,
            text=True,
        )
        status = "완료" if result.returncode == 0 else "실패"
        print(f"  [{status}] {pdf.name}")
        if result.returncode != 0:
            print(f"    {result.stderr[:200]}")


if __name__ == "__main__":
    main()
