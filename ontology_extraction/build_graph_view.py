"""p2–p4 산출물을 인터랙티브 그래프 HTML 한 장으로 만든다.

실행: ontology_extraction/ 에서 `uv run python build_graph_view.py`
출력: outputs/ontology_graph.html (브라우저로 열거나 Artifact로 게시)
"""

import json
from pathlib import Path

from common import OUTPUT_ROOT, read_json

TEMPLATE_PATH = Path(__file__).parent / "graph_view_template.html"
OUT_PATH = OUTPUT_ROOT / "ontology_graph.html"


def term_info(n: dict) -> dict:
    return {
        "id": n["normed_id"],
        "label": n["label"],
        "kind": n["kind"],
        "variants": n["surface_variants"],
        "mentions": n["n_mentions"],
        "chunks": n["chunk_ids"],
        "sentence": n["mentions"][0]["sentence"],
    }


def build() -> dict:
    p2 = read_json(OUTPUT_ROOT / "p2" / "normed_terms.json")
    p3 = read_json(OUTPUT_ROOT / "p3" / "concepts.json")
    p3_rej = read_json(OUTPUT_ROOT / "p3" / "rejected.json")
    p3_prop = read_json(OUTPUT_ROOT / "p3" / "proposals.json")
    p4 = read_json(OUTPUT_ROOT / "p4" / "relations.json")
    p4_rej = read_json(OUTPUT_ROOT / "p4" / "rejected.json")
    p4_hold = read_json(OUTPUT_ROOT / "p4" / "human_queue.json")

    normed = {n["normed_id"]: n for n in p2["normed_terms"]}

    def terms(ids):
        return [term_info(normed[i]) for i in ids if i in normed]

    concepts = [
        {
            "name": c["name"],
            "description": c["description"],
            "parent": c["parent"],
            "mentions": c["evidence_mentions"],
            "evidence": terms(c["evidence_term_ids"]),
            "instances": terms(c["instance_term_ids"]),
            "properties": terms(c["property_term_ids"]),
            "judge": c.get("judge"),
            "status": "passed",
        }
        for c in p3["concepts"]
    ]

    proposals = {p["name"]: p for p in p3_prop["proposals"]}
    for r in p3_rej["rejected"]:
        p = proposals.get(r["item_id"], {})
        concepts.append({
            "name": r["item_id"],
            "description": p.get("description", ""),
            "parent": None,
            "mentions": r.get("evidence_mentions"),
            "evidence": terms(p.get("evidence_term_ids", [])),
            "instances": terms(p.get("instance_term_ids", [])),
            "properties": terms(p.get("property_term_ids", [])),
            "judge": r.get("judge"),
            "status": "rejected",
            "reason": r["reason"],
            "route_to": r["route_to"],
        })

    def rel_out(rel, status, reason=None, route_to=None, absent=None):
        ev = rel["evidence"]
        if isinstance(ev, str):
            ev = [{"chunk_id": rel["chunk_id"], "sentence": ev}]
        return {
            "id": rel.get("relation_id") or f"{rel['domain']}.{rel['name']}.{rel['range']}@{rel['chunk_id']}",
            "name": rel["name"],
            "domain": rel["domain"],
            "range": rel["range"],
            "cardinality": rel["cardinality"],
            "confidence": rel.get("confidence", rel.get("gen_confidence")),
            "evidence": ev,
            "judge": rel.get("judge"),
            "same_pair": rel.get("same_pair_relations", []),
            "status": status,
            "reason": reason,
            "route_to": route_to,
            "absent": absent,
        }

    relations = [rel_out(r, "passed") for r in p4["relations"]]
    for r in p4_hold["human_queue"]:
        relations.append(rel_out(r["relation"], "held", r["reason"], r["route_to"]))
    for r in p4_rej["rejected"]:
        rel = r.get("relation") or r["proposal"]
        relations.append(rel_out(rel, "rejected", r["reason"], r["route_to"], r.get("absent")))

    meta = {
        "doc": p2["meta"]["doc_id"],
        "model": p4["meta"]["model"],
        "n_terms": p2["meta"]["n_terms_in"],
        "n_normed": p2["meta"]["n_normed_terms"],
        "n_concepts": p3["meta"]["n_concepts"],
        "n_relations": p4["meta"]["n_relations"],
    }
    return {"meta": meta, "concepts": concepts, "relations": relations}


if __name__ == "__main__":
    data = build()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE_PATH.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    OUT_PATH.write_text(html, encoding="utf-8")
    print(OUT_PATH, f"{len(html) / 1024:.0f} KB", {k: len(v) for k, v in data.items() if isinstance(v, list)})
