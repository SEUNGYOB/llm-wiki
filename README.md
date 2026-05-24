# llm-wiki

LLM 논문·모델·기법을 자동으로 수집·처리·정리하는 지식 베이스.

## 원칙

| 원칙 | 설명 |
|------|------|
| GitHub | 코드와 문서만 버전 관리 |
| Syncthing | PDF와 중간 산출물만 동기화 |
| `raw/` | 원본 보관 전용 — 수집 후 수정 금지 |
| `wiki/` | 최종 지식 페이지 |
| `output/` | 처리 결과를 사람이 확인하는 곳 |

## 디렉토리 구조

```
llm-wiki/
├── input/pdfs/          ← Syncthing 수신 폴더 (PDF 투입구)
├── raw/
│   ├── papers/          ← 처리 완료된 원본 PDF 보관
│   ├── clips/           ← 웹 클리핑 원본
│   └── releases/        ← 모델 릴리즈 노트 원본
├── wiki/
│   ├── concepts/        ← 개념 지식 페이지
│   ├── models/          ← 모델별 지식 페이지
│   ├── papers/          ← 논문별 지식 페이지
│   └── techniques/      ← 기법별 지식 페이지
├── output/              ← 처리 결과 (요약, 스텁 초안 등)
├── inbox/               ← 수동 처리 대기 항목
├── logs/                ← 자동화 로그
├── scripts/             ← 파이프라인 스크립트
└── launchd/             ← Mac launchd plist
```

## 자동화 흐름

```
input/pdfs/ (Syncthing 수신)
    ↓ watch_input_pdfs.py (launchd 상시 실행)
    ↓ process_pdf.py
        → 메타데이터 추출 (제목, 저자, DOI, arXiv ID)
        → Claude API로 요약 생성
        → wiki/papers/ 스텁 생성
        → output/ 에 처리 결과 저장
        → raw/papers/ 로 원본 이동
        → logs/ 에 로그 기록
    ↓ update_index.py
        → wiki/papers/INDEX.md 갱신
```

## 빠른 시작

```bash
# 의존성 설치
pip install -r scripts/requirements.txt

# 와처 수동 실행 (테스트용)
python scripts/watch_input_pdfs.py

# launchd 등록 (상시 실행)
cp launchd/com.moltbot.llm-wiki-watcher.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.moltbot.llm-wiki-watcher.plist
```

## 관련 문서

- [SCHEMA.md](SCHEMA.md) — 데이터 스키마
- [workflows.md](workflows.md) — 상세 워크플로
- [commands.md](commands.md) — 사용 가능한 커맨드
- [syncthing.md](syncthing.md) — Syncthing 설정 가이드
- [errors.md](errors.md) — 알려진 오류와 해결법
- [STATUS.md](STATUS.md) — 현재 상태
