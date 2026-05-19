import json
import time
from pathlib import Path
import requests


BASE_URL = "https://semantics.inf.um.es/rag-api"
OUTPUT_DIR = Path("remote_rag_results_ENdb")

TIMEOUT_SECONDS = 100000

TOP_K_ONTOLOGIES = 4
TOP_CLASS_PER_ENTITY = 1
TOP_PROPERTY_PER_RELATION = 1
TOPK_INDEX_RELATIONS = 20
SCORE_THRESHOLD = 0.5

PAUSE_SECONDS = 1

ENDB_ONTOLOGY_DESCRIPTION = (
    "enhancer regulatory region cis-regulatory module transcription factor "
    "binding target gene gene regulation disease tissue cell type"
)

ENDB_ENTITIES = [
    "enhancer",
    "gene",
    "transcriptionFactor",
    "disease",
    "tissueContext",
    "regulatoryAssociation"
]

ENDB_RELATIONS = [
    "Enhancer involves RegulatoryAssociation",
    "RegulatoryAssociation occurs in TissueContext",
    "RegulatoryAssociation associated with Disease",
    "RegulatoryAssociation has target Gene",
    "RegulatoryAssociation regulated by TranscriptionFactor"
]


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)


def safe_filename(text):
    safe_text = text.replace(" ", "_")
    safe_text = safe_text.replace("/", "_")
    safe_text = safe_text.replace("\\", "_")
    safe_text = safe_text.replace(":", "")
    safe_text = safe_text.replace(";", "")
    safe_text = safe_text.replace(",", "")
    safe_text = safe_text.replace("(", "")
    safe_text = safe_text.replace(")", "")
    return safe_text


def get_request(endpoint, params):
    url = BASE_URL + endpoint

    try:
        response = requests.get(
            url,
            params=params,
            timeout=TIMEOUT_SECONDS
        )

        status_code = response.status_code

        try:
            response_content = response.json()
        except ValueError:
            response_content = response.text

        result = {
            "ok": status_code < 400,
            "status_code": status_code,
            "url": response.url,
            "params": params,
            "response": response_content
        }

        return result

    except requests.exceptions.RequestException as error:
        result = {
            "ok": False,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "endpoint": endpoint,
            "params": params
        }

        return result


def get_available_ontologies():
    params = {}

    result = get_request("/ontologies", params)
    save_json(OUTPUT_DIR / "00_available_ontologies.json", result)

    return result


def build_class_count_index(available_ontologies_result):
    class_count_index = {}

    if not available_ontologies_result.get("ok"):
        return class_count_index

    response = available_ontologies_result.get("response", {})
    ontologies = response.get("ontologies", [])

    for ontology in ontologies:
        ontology_id = ontology.get("ontologyId")
        class_count = ontology.get("classCount")

        if ontology_id:
            class_count_index[ontology_id] = class_count

    return class_count_index


def run_similar_ontologies():
    params = {
        "top_k": TOP_K_ONTOLOGIES,
        "description_text": ENDB_ONTOLOGY_DESCRIPTION
    }

    result = get_request("/ontology/similar-ontologies", params)
    save_json(OUTPUT_DIR / "01_ENdb_similar_ontologies.json", result)

    return result


def get_ontology_ids(similar_ontologies_result):
    ontology_ids = []

    if not similar_ontologies_result.get("ok"):
        return ontology_ids

    response = similar_ontologies_result.get("response", {})
    results = response.get("results", [])

    for item in results:
        ontology_id = item.get("ontologyId")

        if ontology_id:
            ontology_ids.append(ontology_id)

    return ontology_ids


def enrich_ontology_selection(ontology_ids, class_count_index):
    enriched = []

    for ontology_id in ontology_ids:
        enriched.append(
            {
                "ontologyId": ontology_id,
                "classCount": class_count_index.get(ontology_id)
            }
        )

    return enriched


def run_similar_entity_single_ontology(entity_name, ontology_id):
    params = {
        "description_text": entity_name,
        "ontology_ids": ontology_id,
        "top_class_per_entity": TOP_CLASS_PER_ENTITY,
        "score_threshold": SCORE_THRESHOLD,
        "context": True
    }

    result = get_request("/ontology/similar-entities", params)

    entity_folder = OUTPUT_DIR / "02_entities"
    entity_folder.mkdir(parents=True, exist_ok=True)

    file_name = "entity_" + safe_filename(entity_name) + "__ontology_" + safe_filename(ontology_id) + ".json"
    save_json(entity_folder / file_name, result)

    return result


def run_entities_by_small_queries(ontology_ids):
    summary = {}

    for entity_name in ENDB_ENTITIES:
        summary[entity_name] = {}

        for ontology_id in ontology_ids:
            print("Entity:", entity_name, "| Ontology:", ontology_id)

            result = run_similar_entity_single_ontology(entity_name, ontology_id)
            summary[entity_name][ontology_id] = {
                "ok": result.get("ok"),
                "status_code": result.get("status_code"),
                "error_type": result.get("error_type"),
                "error_message": result.get("error_message")
            }

            time.sleep(PAUSE_SECONDS)

    save_json(OUTPUT_DIR / "02_ENdb_similar_entities_summary.json", summary)

    return summary


def run_similar_relation_single_ontology(relation_text, ontology_id):
    params = {
        "description_text": relation_text,
        "ontology_ids": ontology_id,
        "top_property_per_relation": TOP_PROPERTY_PER_RELATION,
        "topk_index": TOPK_INDEX_RELATIONS,
        "score_threshold": SCORE_THRESHOLD
    }

    result = get_request("/ontology/similar-relations", params)

    relation_folder = OUTPUT_DIR / "03_relations"
    relation_folder.mkdir(parents=True, exist_ok=True)

    file_name = "relation_" + safe_filename(relation_text) + "__ontology_" + safe_filename(ontology_id) + ".json"
    save_json(relation_folder / file_name, result)

    return result


def run_relations_by_small_queries(ontology_ids):
    summary = {}

    for relation_text in ENDB_RELATIONS:
        summary[relation_text] = {}

        for ontology_id in ontology_ids:
            print("Relation:", relation_text, "| Ontology:", ontology_id)

            result = run_similar_relation_single_ontology(relation_text, ontology_id)
            summary[relation_text][ontology_id] = {
                "ok": result.get("ok"),
                "status_code": result.get("status_code"),
                "error_type": result.get("error_type"),
                "error_message": result.get("error_message")
            }

            time.sleep(PAUSE_SECONDS)

    save_json(OUTPUT_DIR / "03_ENdb_similar_relations_summary.json", summary)

    return summary


def save_parameters(ontology_ids, enriched_ontology_selection):
    parameters = {
        "case": "ENdb",
        "base_url": BASE_URL,
        "strategy": "Small independent requests: one entity or one relation against one ontology at a time.",
        "top_k_ontologies": TOP_K_ONTOLOGIES,
        "top_class_per_entity": TOP_CLASS_PER_ENTITY,
        "top_property_per_relation": TOP_PROPERTY_PER_RELATION,
        "topk_index_relations": TOPK_INDEX_RELATIONS,
        "score_threshold": SCORE_THRESHOLD,
        "timeout_seconds": TIMEOUT_SECONDS,
        "pause_seconds_between_requests": PAUSE_SECONDS,
        "ontology_description": ENDB_ONTOLOGY_DESCRIPTION,
        "entities": ENDB_ENTITIES,
        "relations": ENDB_RELATIONS,
        "ontology_ids_used": ontology_ids,
        "ontology_selection_with_class_counts": enriched_ontology_selection
    }

    save_json(OUTPUT_DIR / "00_ENdb_parameters.json", parameters)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Running ENdb remote RAG case with small queries")

    available_ontologies = get_available_ontologies()
    class_count_index = build_class_count_index(available_ontologies)

    similar_ontologies = run_similar_ontologies()
    ontology_ids = get_ontology_ids(similar_ontologies)

    enriched_ontology_selection = enrich_ontology_selection(
        ontology_ids,
        class_count_index
    )

    print("Ontology IDs returned by similar-ontologies:")
    print(",".join(ontology_ids))

    save_parameters(ontology_ids, enriched_ontology_selection)

    if not ontology_ids:
        print("No ontology IDs were returned. Similar entities and similar relations were not executed.")
        return

    run_entities_by_small_queries(ontology_ids)
    run_relations_by_small_queries(ontology_ids)

    print("Finished ENdb remote RAG case")
    print("Results saved in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
