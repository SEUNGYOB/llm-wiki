# CLAUDE.md — llm-wiki

Claude가 이 레포에서 작업할 때 따라야 하는 규칙.

## 절대 원칙

- `raw/` 폴더 안 파일은 절대 수정하지 않는다. 읽기만 허용.
- PDF 파일은 git add 하지 않는다.
- `output/`, `logs/` 안 파일은 git add 하지 않는다.
- 새 파일을 만들면 반드시 인덱스를 함께 업데이트한다.

## 디렉토리 역할

| 경로 | 역할 | 수정 가능 여부 |
|------|------|--------------|
| `input/pdfs/` | Syncthing 수신 — 투입구 | 읽기 전용 |
| `raw/papers/` | 원본 PDF 보관 | 읽기 전용 |
| `raw/clips/` | 웹 클리핑 원본 | 읽기 전용 |
| `raw/releases/` | 릴리즈 노트 원본 | 읽기 전용 |
| `wiki/` | 최종 지식 페이지 | 수정 가능 |
| `output/` | 처리 결과 확인 | 수정 가능 |
| `scripts/` | 파이프라인 코드 | 수정 가능 |
| `logs/` | 자동화 로그 | 읽기 전용 |

## wiki/ 작업 규칙

- 논문 스텁 생성 시 SCHEMA.md의 논문 스텁 포맷을 따른다.
- `status: stub`으로 시작하고, 사람이 검토하면 `reviewed`로 올린다.
- 새 스텁을 만들면 `wiki/papers/INDEX.md`를 즉시 갱신한다.
- 파일명: 논문은 `arxiv_id.md` 또는 `firstauthorYYYY.md`.

## 인덱스 관리

파일을 추가하거나 상태를 바꿀 때마다:
1. `wiki/papers/INDEX.md` 갱신
2. `STATUS.md` 카운터 갱신
3. 필요시 `wiki/concepts/`, `wiki/models/` 관련 인덱스도 갱신

## 환경 변수

- `ANTHROPIC_API_KEY` — Claude API 호출에 필요
- `LLM_WIKI_ROOT` — 프로젝트 루트 경로 (기본: 이 파일이 있는 디렉토리)
