# Workflows

## 1. PDF 자동 처리 흐름

```
[다른 기기] → Syncthing → input/pdfs/새논문.pdf
                                ↓
                    watch_input_pdfs.py (상시 실행)
                    파일 쓰기 완료(on_closed) 감지
                                ↓
                    process_pdf.py 호출
                    ├── 1. PDF 메타데이터 추출 (pymupdf)
                    │       title, authors, abstract
                    ├── 2. arXiv ID / DOI 추출 시도
                    ├── 3. Claude API → 한국어 요약 생성
                    ├── 4. wiki/papers/{id}.md 스텁 생성
                    ├── 5. output/{id}_summary.md 저장
                    ├── 6. raw/papers/{id}.pdf 로 이동
                    └── 7. logs/pipeline.jsonl 에 로그
                                ↓
                    update_index.py 호출
                    └── wiki/papers/INDEX.md 갱신
```

## 2. 수동 처리 흐름

PDF를 직접 넣거나, 자동 처리에 실패한 경우:

```bash
# 단일 PDF 수동 처리
python scripts/process_pdf.py input/pdfs/paper.pdf

# inbox/ 항목 일괄 처리
python scripts/process_inbox.py

# 인덱스만 강제 재생성
python scripts/update_index.py --rebuild
```

## 3. 스텁 → 완성 페이지 흐름

1. `wiki/papers/INDEX.md` 에서 `status: stub` 항목 확인
2. `output/{id}_summary.md` 요약 참고
3. 스텁 파일 열어서 섹션 채우기
4. `status: reviewed` 또는 `complete` 로 변경
5. `STATUS.md` 카운터 업데이트

## 4. 새 개념/모델 페이지 생성

```bash
# 개념 페이지
cp wiki/concepts/_template.md wiki/concepts/새개념.md

# 모델 페이지
cp wiki/models/_template.md wiki/models/새모델.md
```

SCHEMA.md의 포맷 따라 작성 후 관련 논문 페이지에서 링크 추가.
