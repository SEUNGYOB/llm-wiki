# Errors

## PDF 처리 오류

### `pymupdf` 설치 실패
```
pip install pymupdf
# 안 되면:
pip install PyMuPDF
```

### PDF가 스캔 이미지라 텍스트 추출 불가
- 증상: `abstract`가 빈 문자열
- 해결: `ocrmypdf`로 OCR 처리 후 재투입
```bash
ocrmypdf input.pdf input_ocr.pdf
```

### arXiv ID 추출 실패
- 증상: `arxiv_id: null`, 파일명을 ID로 사용
- 해결: 스텁 파일에서 수동으로 `arxiv_id` 입력

## 자동화 오류

### launchd가 실행 안 됨
```bash
# 로그 확인
cat logs/watcher.log
# plist 문법 오류 확인
plutil -lint launchd/com.moltbot.llm-wiki-watcher.plist
```

### watchdog이 on_closed를 안 잡음
- 증상: PDF 수신 직후 처리 시도 → 파일 불완전
- 해결: `watch_input_pdfs.py`에서 파일 크기 안정화 대기 로직 작동 중인지 확인

### Claude API 오류 (429 Rate limit)
- 로그: `logs/pipeline.jsonl` 에서 `"status": "error"` 확인
- 해결: `inbox/`로 이동된 파일을 `process_inbox.py`로 재처리

## Syncthing 오류

### 파일이 안 들어옴
1. Syncthing Web UI (http://localhost:8384) 에서 연결 상태 확인
2. `input/pdfs/` 경로가 plist의 경로와 일치하는지 확인
3. Mac mini가 절전 모드에 빠졌는지 확인 (에너지 설정 → 잠자기 해제)
