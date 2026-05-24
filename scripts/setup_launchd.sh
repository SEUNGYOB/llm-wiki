#!/bin/bash
# setup_launchd.sh — launchd plist를 실제 API key로 치환 후 등록.
# 최초 1회 실행.

set -e

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "오류: ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다."
    echo "  export ANTHROPIC_API_KEY=sk-ant-..."
    exit 1
fi

PLIST_SRC="$(dirname "$0")/../launchd/com.moltbot.llm-wiki-watcher.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.moltbot.llm-wiki-watcher.plist"

# API key 치환하여 LaunchAgents에 설치
sed "s/YOUR_API_KEY_HERE/$ANTHROPIC_API_KEY/" "$PLIST_SRC" > "$PLIST_DEST"

# 기존 등록 해제 (재등록 시)
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# 등록
launchctl load "$PLIST_DEST"
echo "등록 완료: com.moltbot.llm-wiki-watcher"
echo "상태 확인: launchctl list | grep llm-wiki"
echo "로그 확인: tail -f $(dirname "$0")/../logs/watcher.log"
