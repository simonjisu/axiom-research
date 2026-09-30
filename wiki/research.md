# Axiom 연구 자료 인덱스

> 확인일: 2026-09-28  
> 범위: [연구 목표 재구조화 대화](https://chatgpt.com/g/g-p-6a718b3346348191be4d2f92afde13d7-insaenggyehoeg/c/6ab3189e-7ad4-83e8-b130-de40f08b8d9d)에서 만든·참조한 개인 Notion의 Axiom 연구 자료  
> 성격: 원문을 찾기 위한 연구 인덱스. 아래 요약은 해당 Notion 페이지의 기록 시점에 묶여 있으며, 제품의 현행 동작은 코드와 실행으로 별도 검증한다.

## 먼저 읽을 문서

| 순서 | 자료 | 쓰임새 |
|---|---|---|
| 1 | [Axiom — 시작 페이지](https://app.notion.com/p/3e463f83d98981f28a0cccb006c727e4) | 제품 개발과 연구의 두 축, 온톨로지 정의 초안, 장·중·단기 목표의 입구. |
| 2 | [Axiom 연구 — 범용 온톨로지와 에이전트 유용성](https://app.notion.com/p/3e463f83d98981588467d2d57809f5b1) | 연구 프로젝트 정본. CQ에서 개념·관계 후보를 찾고 의미 질문·데이터 검증 질의·validation gate로 시험하는 계획. |
| 3 | [Axiom 용어집 — 제품 용어와 연구 용어 대응](https://app.notion.com/p/3e463f83d98981e0afb0fffed696f12a) | Object Type, Relation Type, Mapping, Glossary, Rule 등 용어의 참고 자료. Tenant·Workbench·OQL Card는 2026-09-28 기준 메모를 우선한다. |
| 4 | [Axiom 현행 시스템 구조 — FDE 교육 자료 기반](https://app.notion.com/p/3e463f83d989815d84c8edfc555a2444) | Connection → Import → Resource → Ontology/Mapping → 질의·Workflow → QA의 구조 스냅샷. 원본 FDE 교육 문서는 Draft이다. |
| 5 | [Axiom 연구 일지](https://app.notion.com/p/43e55207c6de498496701b257927fe27) | 날짜·상태·주제·핵심 질문·키워드로 연구 질문과 검증을 찾는 DB. |
| 6 | [데이터세트·자산 인덱스](./datasets.md) | 데이터세트 관리에 사용할 Notion 자산 DB와 현재 스키마의 범위를 확인한다. |

## 연구 질문별 인덱스

| 질문 | 원문 기록 | 핵심 내용 | 현재 근거 수준 |
|---|---|---|---|
| RQ1. 양 끝 Entity가 미확정인 문서 관계를 어떻게 인스턴스화하는가? | [2026-09-24 연구 일지](https://app.notion.com/p/3e563f83d98981d6ad6fd0c6df72851f) | 문장·문서 버전·원문 위치·Relation Type 후보·Entity Resolution·승인 상태를 보존하는 관계 후보를 제안한다. 확인된 후보를 관계용 Resource와 Relation Mapping으로 연결하는 최소 실험을 제시한다. | 연구 가설과 실험안. `Relation Assertion`은 현행 제품 객체로 확정되지 않았다. |
| RQ2. 문서의 표현·개념·집합·관계를 테이블 기반 스키마로 충분히 나타낼 수 있는가? | [2026-09-24 연구 일지](https://app.notion.com/p/3e563f83d98981d6ad6fd0c6df72851f) | 용어 표현, Object Type, Entity 언급, 하위 타입, 조건부 집합, 관계 주장을 구분한다. 논리 연결의 의미와 근거를 먼저 모델링하고 물리 저장 방식을 따로 비교한다. | 연구 가설. 확정 키가 없는 문서 후보를 현행 Relation Mapping에 바로 넣을 수 있다는 주장은 아니다. |
| RQ3. LLM은 온톨로지로 어떻게 조회하고 결과를 답변에 쓰는가? | [2026-09-26 연구 일지](https://app.notion.com/p/3e663f83d98981c0b4d9ef819147e749) · [분석 슬라이드](https://docs.google.com/presentation/d/1N7keK37B4HZWiVdOwutO_3OkxyRq9U9tVqOdxX0XZJ8/edit) | Workbench 범위 → 온톨로지 브리핑 → 저장된 매개변수 OQL Card 선택 또는 OQL 질의 작성 → 검증·SQL/그래프 실행 → `tool` 메시지로 결과 재입력 → 추가 조회 또는 답변을 10단계로 추적한다. | 저장소 커밋 `318e8bfef59a19a782381c2ea70de5dc2ebe82bf`의 정적 코드 분석. 실제 배포 및 질문 실행은 미검증. |

## 자료를 해석할 때의 구분

- **Relation Type**은 관계의 업무 의미와 양 끝 Object Type을 선언한다. **Relation Mapping**은 관계용 Resource의 컬럼을 양 끝 Entity 키와 관계 속성에 연결한다. 고객 원천 DB의 FK는 관계 후보를 찾는 단서이지 두 정의를 대신하지 않는다. [Relation Type 설계](https://app.notion.com/p/382d0c554e7e80faa938c49c85a47383)와 [Mapping 설계](https://app.notion.com/p/382d0c554e7e805e8638f479d2471b97)는 6월 V3 설계 자료이므로 현재 UI/API 필드는 재확인한다.
- 문서의 단어는 곧바로 Object Type이나 Entity가 아니다. 표현 → 개념 또는 Entity 후보 → 근거 확인 → 승인된 관계의 단계를 나눠야 문서의 주장과 확정된 사실을 구분할 수 있다.
- RQ3의 화면상 “추론 경로”는 실행된 질의와 결과에서 파생한 기록이며 LLM의 내부 사고 기록이 아니다. 질의 결과는 다음 모델 호출의 `tool` 메시지로 전달된다.
- [Axiom FDE 교육](https://app.notion.com/p/3ded0c554e7e8172aac4fe31efb5ebcc)은 제품 구조의 출처이지만 Draft다. [현행 시스템 구조](https://app.notion.com/p/3e463f83d989815d84c8edfc555a2444)와 [RQ3 정적 코드 분석](https://app.notion.com/p/3e663f83d98981c0b4d9ef819147e749)이 서로 다른 시점과 근거를 갖는다는 점을 유지한다.
- 용어 기준은 2026-09-20 [Axiom 라이선스 정책](https://app.notion.com/p/3e1d0c554e7e80248a5be04c9345f254)의 Tenant/Workbench 정의와 2026-09-23 [Axiom FDE 교육](https://app.notion.com/p/3ded0c554e7e8172aac4fe31efb5ebcc)의 `published`/`draft` 상태 구분을 함께 반영한다. 교육 초안의 Service/World 서술은 이전 용어로 해석한다.

## 용어 기준 (2026-09-28)

고객 경계는 **Tenant**이며, Tenant 아래 격리 단위는 게시본·초안 모두 **Workbench**다. 질의 언어는 **OQL**이고 저장된 매개변수 질의도 **OQL Card**다. 오래된 `Service`, `World`, `IR`, `SPS` 표기는 원문 인용이나 구현 식별자에서만 유지한다. `ir`, `ir_template`, `internal/ir` 같은 코드 식별자는 바꾸지 않는다. [OQA / OQL 연구 인덱스](./oqa.md)도 같은 기준을 따른다.

## 검색어

`Axiom 연구`, `Axiom 용어집`, `현행 시스템 구조`, `연구 일지`, `RQ1`, `RQ2`, `RQ3`, `Tenant`, `Workbench`, `OQL`, `OQL Card`, `Relation Mapping`, `Relation Assertion`, `Entity Resolution`, `Glossary`, `Evidence`, `Semantic Layer`, `CQ`, `validation gate`, `tool 메시지`
