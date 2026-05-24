# Commands

## 파이프라인

```bash
# PDF 단일 처리
python scripts/process_pdf.py <pdf경로>

# inbox/ 일괄 처리
python scripts/process_inbox.py

# 인덱스 재생성
python scripts/update_index.py --rebuild

# 와처 수동 실행 (foreground)
python scripts/watch_input_pdfs.py
```

## launchd 관리

```bash
# 와처 등록 (최초 1회)
cp launchd/com.moltbot.llm-wiki-watcher.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.moltbot.llm-wiki-watcher.plist

# 상태 확인
launchctl list | grep llm-wiki

# 재시작
launchctl unload ~/Library/LaunchAgents/com.moltbot.llm-wiki-watcher.plist
launchctl load ~/Library/LaunchAgents/com.moltbot.llm-wiki-watcher.plist

# 로그 확인
tail -f logs/watcher.log
tail -f logs/pipeline.log
```

## 상태 확인

```bash
# 처리 대기 중인 PDF
ls input/pdfs/

# 최근 파이프라인 로그
tail -20 logs/pipeline.jsonl | python -m json.tool

# wiki 논문 수
ls wiki/papers/*.md | wc -l

# stub 상태인 논문
grep -l "status: stub" wiki/papers/*.md | wc -l
```

## git

```bash
# 코드/문서만 커밋 (.gitignore가 PDF/output/logs 차단)
git add -A
git status   # 확인 후
git commit -m "메시지"
git push
```
