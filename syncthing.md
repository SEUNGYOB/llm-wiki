# Syncthing 설정 가이드

`input/pdfs/`를 Syncthing 공유 폴더로 등록하는 방법.

## Mac mini 설정

1. Syncthing Web UI 열기: http://localhost:8384

2. **Folders** → **Add Folder** 클릭

3. 설정값:
   - **Folder Label**: `llm-wiki-input`
   - **Folder ID**: `llm-wiki-input` (다른 기기와 동일하게 맞출 것)
   - **Folder Path**: `/Users/moltbot/projects/llm-wiki/input/pdfs`
   - **Folder Type**: `Receive Only` (Mac mini는 수신 전용)

4. **Sharing** 탭에서 PDF를 보내는 기기(iPhone, iPad, 노트북 등) 추가

5. **Save**

## 보내는 기기 설정 (예: 노트북)

1. 같은 Folder ID(`llm-wiki-input`)로 폴더 추가
2. **Folder Type**: `Send Only`
3. Mac mini의 Device ID 추가하여 연결

## 주의사항

- Mac mini의 `input/pdfs/` 는 **Receive Only** — 로컬에서 파일을 추가해도 다른 기기로 전파되지 않음
- `raw/`, `output/`, `wiki/`는 Syncthing 범위 밖 — git으로만 관리
- PDF 파일이 완전히 수신된 후 watch_input_pdfs.py가 처리 시작함 (watchdog의 `on_closed` 이벤트 사용)

## 확인 방법

```bash
# Syncthing 상태 확인
curl -s http://localhost:8384/rest/db/status?folder=llm-wiki-input \
  -H "X-API-Key: $(cat ~/.config/syncthing/config.xml | grep apikey | head -1 | sed 's/.*>\(.*\)<.*/\1/')"

# 폴더에 파일 들어오는지 확인
ls -lh /Users/moltbot/projects/llm-wiki/input/pdfs/
```
