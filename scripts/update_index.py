#!/usr/bin/env python3
"""
update_index.py — wiki/papers/INDEX.md를 스텁 파일들로부터 재생성.

Usage:
    python scripts/update_index.py
    python scripts/update_index.py --rebuild   # 전체 재생성
"""

import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
WIKI_PAPERS = ROOT / "wiki" / "papers"
INDEX_PATH = WIKI_PAPERS / "INDEX.md"


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ": " in line:
            k, v = line.split(": ", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def build_index():
    entries = []
    for md_path in sorted(WIKI_PAPERS.glob("*.md")):
        if md_path.name in ("INDEX.md", "_template.md"):
            continue
        fm = parse_frontmatter(md_path)
        if not fm:
            continue
        entries.append({
            "added": fm.get("added", "0000-00-00"),
            "arxiv_id": fm.get("arxiv_id", ""),
            "title": fm.get("title", md_path.stem),
            "venue": fm.get("venue", ""),
            "status": fm.get("status", "stub"),
            "file": md_path.name,
        })

    entries.sort(key=lambda x: x["added"], reverse=True)

    lines = [
        "# Papers Index",
        "",
        f"_마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"_총 {len(entries)}편_",
        "",
        "| 날짜 | ID | 제목 | venue | status |",
        "|------|----|------|-------|--------|",
    ]

    for e in entries:
        title_link = f"[{e['title'][:50]}]({e['file']})"
        lines.append(
            f"| {e['added']} | {e['arxiv_id'] or '-'} | {title_link} | {e['venue'] or '-'} | {e['status']} |"
        )

    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"INDEX.md 갱신 완료 — {len(entries)}편")
    return len(entries)


if __name__ == "__main__":
    build_index()
