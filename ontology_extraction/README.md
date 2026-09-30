# ontology_extraction

문서 → 온톨로지 구축 파이프라인 실험. 각 단계는 교체 가능한 슬롯이고, 단계 뒤의 게이트가 산출물을 **건 단위**로 통과 / 반려 / 보류한다.

| 노트북 | 단계 | 입력 → 출력 | 게이트 |
|---|---|---|---|
| `p1_term_extraction.ipynb` | term 추출 | 원문 → `outputs/p1/terms.json` | 원문 span 일치, JSON 스키마, self-consistency, 문서 단위 병합 |
| `p2_normalization.ipynb` | 정규화 | term → `outputs/p2/normed_terms.json` | 결정론 규칙 → 임베딩 후보 → LLM 고정 액션(MERGE/DISTINCT/UNSURE), PK 충돌·모호 병합은 사람 큐, 병합 로그 |
| `p3_concept_extraction.ipynb` | concept(=Object Type) | normed_term → `outputs/p3/concepts.json` | instance 승격, 닫힌 어휘 재사용·중복, 계층 순환, 근거 언급 수 |
| `p4_relation_inference.ipynb` | relation 추론 | concept + 원문 → `outputs/p4/relations.json` | domain/range 닫힌 어휘, 근거 문장 원문 일치·표기 포함, 다중성 충돌, judge 방향 검사, 낮은 confidence 보류 |

실행 순서: p1 → p2 → p3 → p4. 노트북은 이 폴더에서 실행한다 (공통 설정은 `common.py`).

## 게이트 기록

단계마다 `rejected.json`과 `human_queue.json`을 남긴다. 한 건은 `{item_id, stage, reason, route_to, ...}` 형식이고, `route_to`는 실패 원인 단계(`p1`–`p4`) 또는 `human`이다. 루프 오케스트레이션(반려 건을 원인 단계로 다시 보내는 부분)은 아직 없다. 이 기록이 그 입력이다.

## 선택 입력

- `catalog/object_types.json`: 기존 Object Type 카탈로그 `[{"name", "description"}]`. 있으면 p3가 재사용을 먼저 시도한다(닫힌 어휘).
- `.env`의 `GEMINI_EMBEDDING_MODEL`: p2 임베딩 모델 (기본 `gemini-embedding-001`).
