# ontology_extraction

문서 → 온톨로지 구축 파이프라인 실험. 각 단계는 교체 가능한 슬롯이고, 단계 뒤의 게이트가 산출물을 **건 단위**로 통과 / 반려 / 보류한다.

| 노트북 | 단계 | 입력 → 출력 | 게이트 |
|---|---|---|---|
| `p1_term_extraction.ipynb` | term 추출 | 원문 → `outputs/p1/terms.json` | 원문 span 일치, JSON 스키마, self-consistency, 문서 단위 병합 |
| `p2_normalization.ipynb` | 정규화 | term → `outputs/p2/normed_terms.json` | 결정론 규칙 → 임베딩 후보 → LLM 고정 액션(MERGE/DISTINCT/UNSURE), PK 충돌·모호 병합은 사람 큐, 병합 로그 |
| `p3_concept_extraction.ipynb` | concept(=Object Type) | normed_term → `outputs/p3/concepts.json` | instance 승격, 닫힌 어휘 재사용·중복, 계층 순환, 근거 언급 수 |
| `p4_relation_inference.ipynb` | relation 추론 | concept + 원문 → `outputs/p4/relations.json` | domain/range 닫힌 어휘, 근거 문장 원문 일치·표기 포함(spaCy 표제어 비교), 다중성 충돌, judge 방향 검사, 낮은 confidence 보류 |

실행 순서: p1 → p2 → p3 → p4. 노트북은 이 폴더에서 실행한다 (공통 설정은 `common.py`).

## 그래프로 보기

`uv run python build_graph_view.py` → `outputs/ontology_graph.html`. p2–p4 결과를 읽어 concept(노드)과 relation(엣지)을 인터랙티브 그래프로 보여준다. 노드·엣지를 누르면 원문 근거와 게이트 판정이 나오고, term과 반려·보류 건은 토글로 켠다. 노트북을 다시 돌린 뒤 이 스크립트도 다시 실행한다.

## 게이트 기록

단계마다 `rejected.json`과 `human_queue.json`을 남긴다. 한 건은 `{item_id, stage, reason, route_to, ...}` 형식이고, `route_to`는 실패 원인 단계(`p1`–`p4`) 또는 `human`이다. 루프 오케스트레이션(반려 건을 원인 단계로 다시 보내는 부분)은 아직 없다. 이 기록이 그 입력이다.

## 게이트만 다시 돌리기

p4의 `REUSE_CACHE = True`(기본값)면 저장된 relation 후보(`proposals.json`)와 judge 판정(`judge_cache.json`)을 재사용한다. 게이트 규칙을 바꿔도 LLM 출력은 그대로라 규칙 변경 효과만 비교할 수 있다. 후보를 새로 뽑으려면 `False`로 두거나 두 파일을 지운다.

## 선택 입력

- `catalog/object_types.json`: 기존 Object Type 카탈로그 `[{"name", "description"}]`. 있으면 p3가 재사용을 먼저 시도한다(닫힌 어휘).
- `.env`의 `GEMINI_EMBEDDING_MODEL`: p2 임베딩 모델 (기본 `gemini-embedding-001`).
