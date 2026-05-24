#!/usr/bin/env python3
"""
watch_input_pdfs.py — input/pdfs/ 폴더를 감시하고 새 PDF가 완전히 수신되면 처리 파이프라인 실행.

launchd에 의해 Mac mini 시작 시 자동 실행됨.
"""

import time
import logging
import subprocess
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ROOT = Path(__file__).parent.parent
INPUT_PDFS = ROOT / "input" / "pdfs"
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS / "watcher.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

STABILITY_WAIT = 3.0  # 파일 크기 안정화 대기 (초)
STABILITY_CHECKS = 3  # 안정화 확인 횟수


def is_stable(path: Path) -> bool:
    """파일 크기가 안정됐는지 확인 (Syncthing 수신 완료 판단)."""
    try:
        size = path.stat().st_size
        for _ in range(STABILITY_CHECKS):
            time.sleep(STABILITY_WAIT)
            if path.stat().st_size != size:
                return False
        return size > 0
    except FileNotFoundError:
        return False


class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() != ".pdf":
            return
        self._handle(path)

    def on_moved(self, event):
        # Syncthing은 .syncthing-*.tmp → 최종 파일명으로 rename하기도 함
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix.lower() != ".pdf":
            return
        self._handle(path)

    def _handle(self, path: Path):
        log.info(f"새 PDF 감지: {path.name}")
        if not is_stable(path):
            log.warning(f"파일 불안정 — 건너뜀: {path.name}")
            return
        log.info(f"처리 시작: {path.name}")
        result = subprocess.run(
            ["python", str(ROOT / "scripts" / "process_pdf.py"), str(path)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            log.info(f"처리 완료: {path.name}")
        else:
            log.error(f"처리 실패: {path.name}\n{result.stderr}")


def main():
    INPUT_PDFS.mkdir(parents=True, exist_ok=True)
    log.info(f"감시 시작: {INPUT_PDFS}")

    handler = PDFHandler()
    observer = Observer()
    observer.schedule(handler, str(INPUT_PDFS), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        log.info("감시 종료")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
