import os
import json
from OntoNG import OntoNG, LLMConfig, EnginePlugins, QASARConfig, QualityQASAR

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QASAR_API_KEY = os.getenv("QASAR_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definida")

if not QASAR_API_KEY:
    raise ValueError("QASAR_API_KEY no está definida")

DATASET_PATH = "enh2disease_clean.csv"


def pipeline_enh2disease_no_rag_qasar():
    qa_plugin = QualityQASAR(api_key=QASAR_API_KEY)
    qa_config = QASARConfig(
        persistent=False,
        ontology_name="DiseaseEnhancer enh2disease Ontology - no RAG + QASAR"
    )

    engine = OntoNG(
        llm_config=LLMConfig(
            provider="openai",
            api_key=OPENAI_API_KEY,
            max_tokens=None,
            model="gpt-5.4",
            temperature=0
        ),
        plugins=EnginePlugins(
            rag_plugin=None,
            quality_analyzer=qa_plugin
        )
    )

    parts = engine.partition_data(source=DATASET_PATH, min_columns=5, max_columns=10)

    diagrams = []
    json_data_last = None

    for part in parts:
        json_data, json_data_llm, column_mapping, llm_column_mapping = engine.perform_preprocessing(
            source=part,
            llm_columns=False,
            is_raw_text=True
        )
        json_data_last = json_data

        print("=== PREPROCESSING ===")
        print(json_data)

        diagram = engine.generate_puml_diagram(preprocessing_data=json_data)
        if not diagram:
            raise RuntimeError("No se pudo generar el diagrama para una partición")

        diagrams.append(diagram)

    if not diagrams:
        raise RuntimeError("No se generó ningún diagrama")

    if len(diagrams) > 1:
        complete_diagram = engine.merge_puml_diagram(diagrams)
    else:
        complete_diagram = diagrams[0]

    with open("enh2disease_no_rag_qasar.puml", "w", encoding="utf-8") as file:
        file.write(complete_diagram)

    print("=== DIAGRAM GENERATED ===")
    print(complete_diagram)

    ontology = engine.generate_ontology(
        preprocessing_data=json_data_last,
        diagram=complete_diagram,
        model="gpt-5.4"
    )

    if not ontology:
        raise RuntimeError("No se pudo generar la ontología sin RAG")

    with open("enh2disease_no_rag_qasar.ttl", "w", encoding="utf-8") as file:
        file.write(ontology)

    print("=== ONTOLOGY GENERATED ===")
    print(ontology[:3000])

    report = qa_plugin.analyze(ontology=ontology, config=qa_config)

    with open("enh2disease_no_rag_qasar_report.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(vars(report), indent=2, ensure_ascii=False))

    print("=== QASAR REPORT GENERATED ===")
    print(json.dumps(vars(report), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    pipeline_enh2disease_no_rag_qasar()
