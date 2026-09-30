"""p1–p4 노트북이 공유하는 설정과 헬퍼.

경로는 모두 이 모듈 위치 기준의 relative path다. 노트북은 ontology_extraction/ 에서 실행한다.
"""

import json
import os
import re
import time
from pathlib import Path
from typing import TypeVar

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

MODULE_DIR = Path(__file__).parent
PROJECT_ROOT = MODULE_DIR.parent
OUTPUT_ROOT = MODULE_DIR / "outputs"

DATASETS_DIR = Path("/Users/soo/code/datasets/")
INPUT_PATH = DATASETS_DIR / "bpi" / "documents" / "bpi2019-purchase-process.txt"

load_dotenv(PROJECT_ROOT / ".env")
GEMINI_MODEL = os.environ["GEMINI_MODEL"]
EMBEDDING_MODEL = os.environ.get("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def stage_dir(stage: str) -> Path:
    d = OUTPUT_ROOT / stage
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- 문서

SECTION_RE = re.compile(r"^(\d+)\. [A-Z].*$", re.MULTILINE)


def load_chunks(path: Path = INPUT_PATH) -> tuple[str, str, list[dict]]:
    """p1과 같은 규칙(섹션 = 청크)으로 문서를 나눈다. (doc_id, doc_text, chunks)"""
    doc_text = path.read_text(encoding="utf-8")
    doc_id = path.stem
    starts = [0] + [m.start() for m in SECTION_RE.finditer(doc_text)]
    chunks = []
    for i, (s, e) in enumerate(zip(starts, starts[1:] + [len(doc_text)])):
        text = doc_text[s:e]
        chunks.append({"chunk_id": f"{doc_id}#c{i:02d}", "start": s, "end": e, "title": text.strip().splitlines()[0], "text": text})
    return doc_id, doc_text, chunks


# ---------------------------------------------------------------- Gemini

T = TypeVar("T", bound=BaseModel)


def generate_json(
    prompt: str,
    schema: type[T],
    system: str,
    temperature: float = 0.0,
    seed: int = 0,
    retries: int = 3,
) -> tuple[T | None, str | None]:
    """구조화 출력 호출. (결과, 에러). 스키마 위반은 에러 문자열로 돌려준다 (게이트의 형식 검사)."""
    config = types.GenerateContentConfig(
        system_instruction=system,
        response_mime_type="application/json",
        response_schema=schema,
        temperature=temperature,
        seed=seed,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    last_err = None
    for attempt in range(retries):
        try:
            resp = get_client().models.generate_content(model=GEMINI_MODEL, contents=prompt, config=config)
        except Exception as e:  # 네트워크·쿼터 오류는 재시도
            last_err = f"api: {e}"
            time.sleep(2**attempt)
            continue
        try:
            return schema.model_validate_json(resp.text), None
        except (ValidationError, TypeError) as e:
            return None, f"schema: {e}"
    return None, last_err


def embed(texts: list[str], task_type: str = "SEMANTIC_SIMILARITY", batch_size: int = 100) -> np.ndarray:
    """L2 정규화된 임베딩 행렬 (len(texts), dim)."""
    vecs = []
    for i in range(0, len(texts), batch_size):
        resp = get_client().models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts[i : i + batch_size],
            config=types.EmbedContentConfig(task_type=task_type),
        )
        vecs.extend(e.values for e in resp.embeddings)
    m = np.array(vecs, dtype=np.float32)
    return m / np.linalg.norm(m, axis=1, keepdims=True)


# ---------------------------------------------------------------- 게이트 기록


def gate_record(item_id: str, stage: str, reason: str, route_to: str | None, **detail) -> dict:
    """게이트 비통과 한 건. route_to는 되돌릴 단계(p1–p4) 또는 'human'."""
    return {"item_id": item_id, "stage": stage, "reason": reason, "route_to": route_to, **detail}
