import os
from OntoNG import OntoNG, LLMConfig

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY no está definida")

engine = OntoNG(
    llm_config=LLMConfig(
        provider="openai",
        api_key=api_key,
        max_tokens=None,
        model="gpt-4o",
        temperature=0
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

with open("enh2disease_breast_cancer_25.puml", "w", encoding="utf-8") as f:
    f.write(diagram)

print("=== DIAGRAM GENERATED ===")
print(diagram)

ontology = engine.generate_ontology(
    preprocessing_data=json_data,
    diagram=diagram,
    model="gpt-4.1"
)

if not ontology:
    raise RuntimeError("No se pudo generar la ontología")

with open("enh2disease_breast_cancer_25.ttl", "w", encoding="utf-8") as f:
    f.write(ontology)

print("=== ONTOLOGY GENERATED ===")
print(ontology[:3000])
