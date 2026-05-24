#!/usr/bin/env python3
"""
process_pdf.py — PDF 한 편을 받아 메타데이터 추출, 요약 생성, 스텁 생성까지 처리.

Usage:
    python scripts/process_pdf.py <pdf_path>
"""

import sys
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path

import fitz  # pymupdf
import anthropic

ROOT = Path(__file__).parent.parent
WIKI_PAPERS = ROOT / "wiki" / "papers"
RAW_PAPERS = ROOT / "raw" / "papers"
OUTPUT = ROOT / "output"
LOGS = ROOT / "logs"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS / "pipeline.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def extract_metadata(pdf_path: Path) -> dict:
    doc = fitz.open(str(pdf_path))
    meta = doc.metadata or {}

    # 첫 2페이지에서 텍스트 추출
    text = ""
    for i in range(min(2, len(doc))):
        text += doc[i].get_text()
    doc.close()

    title = meta.get("title") or _extract_title(text)
    authors = _extract_authors(meta.get("author") or "", text)
    abstract = _extract_abstract(text)
    arxiv_id = _extract_arxiv_id(text, pdf_path.name)
    year = _extract_year(text, meta)

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "arxiv_id": arxiv_id,
        "year": year,
        "raw_text_sample": text[:3000],
    }


def _extract_title(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines[0] if lines else "Unknown Title"


def _extract_authors(meta_author: str, text: str) -> list[str]:
    if meta_author:
        return [a.strip() for a in re.split(r"[;,]", meta_author) if a.strip()][:6]
    return []


def _extract_abstract(text: str) -> str:
    m = re.search(r"[Aa]bstract[.\s]*\n(.*?)(?:\n\n|\n[A-Z])", text, re.DOTALL)
    if m:
        return m.group(1).replace("\n", " ").strip()[:1500]
    return ""


def _extract_arxiv_id(text: str, filename: str) -> str:
    # 텍스트에서 arXiv ID 추출
    m = re.search(r"arXiv[:\s]+(\d{4}\.\d{4,5})", text, re.IGNORECASE)
    if m:
        return m.group(1)
    # 파일명에서 추출
    m = re.search(r"(\d{4}\.\d{4,5})", filename)
    if m:
        return m.group(1)
    return ""


def _extract_year(text: str, meta: dict) -> int:
    if meta.get("creationDate"):
        m = re.search(r"(\d{4})", meta["creationDate"])
        if m:
            return int(m.group(1))
    m = re.search(r"\b(202\d|201\d)\b", text[:500])
    if m:
        return int(m.group(1))
    return datetime.now().year


def generate_summary(meta: dict) -> str:
    client = anthropic.Anthropic()
    prompt = f"""다음 논문의 메타데이터와 초록을 바탕으로 한국어로 요약해줘.

제목: {meta['title']}
저자: {', '.join(meta['authors'][:3])}
연도: {meta['year']}
초록: {meta['abstract'] or '(초록 없음)'}

아래 형식으로 작성해:

## 한 줄 요약
(핵심 기여를 한 문장으로)

## 핵심 기여
- (기여 1)
- (기여 2)
- (기여 3)

## 방법론
(핵심 방법론 2-3문단)

## 실험 결과
(주요 결과 요약)

## 한계 및 후속 연구
(한계점과 열린 질문들)

## 추천 태그
(쉼표로 구분된 영어 태그 5개 이내, 예: transformer, attention, efficient-inference)
"""
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def extract_tags_from_summary(summary: str) -> list[str]:
    m = re.search(r"## 추천 태그\n(.*)", summary)
    if m:
        return [t.strip() for t in m.group(1).split(",") if t.strip()]
    return []


def create_stub(meta: dict, summary: str, pdf_path: Path) -> Path:
    arxiv_id = meta["arxiv_id"]
    filename = arxiv_id if arxiv_id else re.sub(r"[^\w-]", "_", meta["title"])[:40]
    stub_path = WIKI_PAPERS / f"{filename}.md"
    tags = extract_tags_from_summary(summary)

    # 요약에서 태그 섹션 제거
    summary_clean = re.sub(r"\n## 추천 태그\n.*", "", summary, flags=re.DOTALL).strip()

    content = f"""---
title: "{meta['title']}"
authors: {json.dumps(meta['authors'], ensure_ascii=False)}
year: {meta['year']}
venue: ""
arxiv_id: "{arxiv_id}"
doi: ""
tags: {json.dumps(tags, ensure_ascii=False)}
status: stub
added: {datetime.now().strftime('%Y-%m-%d')}
---

{summary_clean}

## 관련 문서
"""
    stub_path.write_text(content, encoding="utf-8")
    return stub_path


def save_output(meta: dict, summary: str) -> Path:
    filename = meta["arxiv_id"] or re.sub(r"[^\w-]", "_", meta["title"])[:40]
    out_path = OUTPUT / f"{filename}_summary.md"
    out_path.write_text(
        f"# {meta['title']}\n\n**arXiv**: {meta['arxiv_id']}  \n**년도**: {meta['year']}\n\n{summary}",
        encoding="utf-8",
    )
    return out_path


def move_to_raw(pdf_path: Path, arxiv_id: str, title: str) -> Path:
    filename = arxiv_id if arxiv_id else re.sub(r"[^\w-]", "_", title)[:40]
    dest = RAW_PAPERS / f"{filename}.pdf"
    shutil.move(str(pdf_path), str(dest))
    return dest


def write_log(entry: dict):
    log_path = LOGS / "pipeline.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def process(pdf_path: Path):
    log.info(f"처리 시작: {pdf_path.name}")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(pdf_path),
        "status": "error",
        "error": None,
    }

    try:
        meta = extract_metadata(pdf_path)
        log.info(f"메타데이터: {meta['title']} (arXiv: {meta['arxiv_id'] or 'N/A'})")

        summary = generate_summary(meta)
        log.info("요약 생성 완료")

        stub_path = create_stub(meta, summary, pdf_path)
        log.info(f"스텁 생성: {stub_path}")

        out_path = save_output(meta, summary)
        log.info(f"결과 저장: {out_path}")

        raw_path = move_to_raw(pdf_path, meta["arxiv_id"], meta["title"])
        log.info(f"원본 이동: {raw_path}")

        entry.update({
            "arxiv_id": meta["arxiv_id"],
            "title": meta["title"],
            "stub_path": str(stub_path),
            "raw_path": str(raw_path),
            "output_path": str(out_path),
            "status": "ok",
        })

    except Exception as e:
        log.error(f"처리 실패: {e}", exc_info=True)
        entry["error"] = str(e)
        # 실패 시 inbox로 이동
        inbox = ROOT / "inbox" / pdf_path.name
        shutil.move(str(pdf_path), str(inbox))
        log.info(f"inbox로 이동: {inbox}")

    write_log(entry)

    # 인덱스 갱신
    if entry["status"] == "ok":
        import subprocess
        subprocess.run(
            ["python", str(ROOT / "scripts" / "update_index.py")],
            check=False,
        )

    return entry


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_pdf.py <pdf_path>")
        sys.exit(1)
    result = process(Path(sys.argv[1]))
    print(json.dumps(result, indent=2, ensure_ascii=False))
