# Examples

## PDF 한 편 처리 예시

```bash
$ python scripts/process_pdf.py input/pdfs/attention_is_all_you_need.pdf

[INFO] 파일 감지: attention_is_all_you_need.pdf
[INFO] 메타데이터 추출 완료: "Attention Is All You Need" (Vaswani et al., 2017)
[INFO] arXiv ID: 1706.03762
[INFO] Claude API 요약 생성 중...
[INFO] 스텁 생성: wiki/papers/1706.03762.md
[INFO] 결과 저장: output/1706.03762_summary.md
[INFO] 원본 이동: raw/papers/1706.03762.pdf
[INFO] 처리 완료 (12.3초)
```

## 생성된 스텁 예시 (wiki/papers/1706.03762.md)

```markdown
---
title: "Attention Is All You Need"
authors: ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"]
year: 2017
venue: "NeurIPS"
arxiv_id: "1706.03762"
doi: ""
tags: ["transformer", "attention", "sequence-to-sequence"]
status: stub
added: 2024-01-15
---

## 한 줄 요약
RNN 없이 어텐션 메커니즘만으로 구성된 Transformer 아키텍처를 제안.

## 핵심 기여
- Self-attention 기반 인코더-디코더 구조
- Multi-head attention으로 다양한 표현 공간에서 병렬 어텐션
- Positional encoding으로 순서 정보 주입

## 방법론
_미작성 (stub)_

## 실험 결과
_미작성 (stub)_

## 한계 및 후속 연구
_미작성 (stub)_

## 관련 문서
- [concepts/attention.md](../concepts/attention.md)
- [techniques/transformer.md](../techniques/transformer.md)
```

## INDEX.md 예시 (자동 갱신)

```markdown
# Papers Index

| 날짜 | ID | 제목 | venue | status |
|------|----|------|-------|--------|
| 2024-01-15 | 1706.03762 | Attention Is All You Need | NeurIPS | stub |
```
