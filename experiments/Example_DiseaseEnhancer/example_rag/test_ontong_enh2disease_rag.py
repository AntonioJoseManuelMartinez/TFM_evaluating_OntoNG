import os
import json
from OntoNG import OntoNG, LLMConfig, RAGTecnomod, EnginePlugins

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definida")

def pipeline_with_rag():
    plugin = RAGTecnomod()

    engine = OntoNG(
        llm_config=LLMConfig(
            provider="openai",
            api_key=OPENAI_API_KEY,
            max_tokens=None,
            model="gpt-4o",
            temperature=0
        ),
        plugins=EnginePlugins(
            rag_plugin=plugin,
            quality_analyzer=None
        )
    )

    json_data, json_data_llm, column_mapping, llm_column_mapping = engine.perform_preprocessing(
        source="enh2disease_breast_cancer_25.csv",
        llm_columns=False
    )

    print("=== PREPROCESSING ===")
    print(json_data)

    diagram = engine.generate_puml_diagram(preprocessing_data=json_data)
    if not diagram:
        raise RuntimeError("No se pudo generar el diagrama")

    with open("enh2disease_breast_cancer_25_rag.puml", "w", encoding="utf-8") as f:
        f.write(diagram)

    print("=== DIAGRAM GENERATED ===")
    print(diagram)

    mappings = engine.query_rag(
        text=diagram,
        blacklist=[],
        enable_terms_lookup=True,
        enable_properties_lookup=True,
        enable_relations_lookup=True,
        top_k=3
    )

    with open("enh2disease_breast_cancer_25_rag_mappings.json", "w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)

    print("=== RAG MAPPINGS ===")
    print(json.dumps(mappings, indent=2, ensure_ascii=False))

    rag_ontology = engine.generate_ontology(
        preprocessing_data=json_data,
        diagram=diagram,
        rag_enabled=True,
        mapped_entities=mappings,
        model="gpt-4.1",
        replace=True
    )

    if not rag_ontology:
        raise RuntimeError("No se pudo generar la ontología con RAG")

    with open("enh2disease_breast_cancer_25_rag.ttl", "w", encoding="utf-8") as f:
        f.write(rag_ontology)

    print("=== ONTOLOGY WITH RAG GENERATED ===")
    print(rag_ontology[:3000])

if __name__ == "__main__":
    pipeline_with_rag()
