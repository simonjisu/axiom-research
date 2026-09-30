# AGENTS.md

## 규칙

- 의존성은 항상 `uv add <package>`로 설치한다. `pip install`이나 `pyproject.toml` 직접 수정은 쓰지 않는다.
- 경로는 항상 Python `pathlib.Path`를 사용한 relative path로 다룬다. 절대 경로 하드코딩은 피한다. (예외: 저장소 밖 데이터세트 루트 `DATASETS_DIR`는 설정 변수 하나로만 둔다.)

## 환경

- Python 3.12, `uv`로 관리한다 (`.python-version`, `pyproject.toml`, `uv.lock`).
- 비밀 값은 저장소 루트 `.env`에 둔다 (`GEMINI_API_KEY`, `GEMINI_MODEL`). `.env`는 커밋하지 않는다.

## 구조

- `wiki/`: Notion 자료 인덱스와 연구 질문.
- `ontology_extraction/`: 문서 → 온톨로지 구축 파이프라인(p1–p5) 실험 노트북.
