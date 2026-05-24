# SCHEMA

llm-wiki 전체에서 사용하는 데이터 구조 정의.

## 논문 스텁 (wiki/papers/*.md)

```markdown
---
title: "논문 제목"
authors: ["저자1", "저자2"]
year: 2024
venue: "NeurIPS / arXiv / ICML ..."
arxiv_id: "2401.00001"
doi: ""
tags: ["attention", "efficient-inference"]
status: stub | reviewed | complete
added: 2024-01-01
---

## 한 줄 요약

## 핵심 기여

## 방법론

## 실험 결과

## 한계 및 후속 연구

## 관련 문서
```

**status 값:**
- `stub` — 자동 생성, 미검토
- `reviewed` — 사람이 확인 완료
- `complete` — 내용 충분히 채워짐

## 모델 페이지 (wiki/models/*.md)

```markdown
---
title: "모델명"
org: "Anthropic / OpenAI / Meta ..."
released: 2024-01-01
params: "70B"
context: "128k"
tags: ["open-source", "instruction-tuned"]
status: stub | complete
---

## 개요

## 아키텍처 특징

## 성능 벤치마크

## 관련 논문
```

## 개념 페이지 (wiki/concepts/*.md)

```markdown
---
title: "개념명"
tags: ["attention", "transformer"]
---

## 정의

## 핵심 아이디어

## 관련 기법

## 주요 논문
```

## 로그 레코드 (logs/pipeline.jsonl)

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "source_file": "input/pdfs/paper.pdf",
  "arxiv_id": "2401.00001",
  "title": "논문 제목",
  "stub_path": "wiki/papers/2401.00001.md",
  "raw_path": "raw/papers/2401.00001.pdf",
  "status": "ok | error",
  "error": null
}
```

## 인덱스 (wiki/papers/INDEX.md)

논문 스텁 목록을 최신순으로 유지. `update_index.py`가 자동 갱신.

```markdown
| 날짜 | ID | 제목 | venue | status |
|------|----|------|-------|--------|
| 2024-01-01 | 2401.00001 | 제목 | arXiv | stub |
```
