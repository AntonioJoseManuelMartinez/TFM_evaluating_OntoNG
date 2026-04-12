# Evaluating OntoNG

This repository supports a Master’s Thesis focused on evaluating ontology generation from biomedical datasets using large language models (LLMs), comparing **non-RAG** and **RAG-based** settings.

## Objective

The aim of this project is to evaluate the ability of an LLM-based system to:

1. infer an ontological schema from biomedical tabular data,
2. generate an ontology in RDF/OWL/Turtle format,
3. compare the automatically generated output with manually created reference schemas or ontologies,
4. assess whether the use of **RAG** with context ontologies improves the results compared with a non-RAG setup.

## Working environment

The project is based on the following components:

- **OntoNG** as the main ontology generation engine,
- **RAGannotationAPI** as the RAG backend,
- **Neo4j** for storing ontology embeddings,
- OpenAI GPT models for the ontology generation stages,
- context ontologies derived from BioGateway, including:
  - `crm`
  - `crm2gene`
  - `crm2phen`

## Initial dataset used

The first real experiment was conducted using a 25-row sample from `enh2disease-1.0.2.txt`, obtained from **DiseaseEnhancer**, a database of enhancer–disease associations.

## Repository structure

- `experiments/`: descriptions of the experiments carried out
- `data/samples/`: data samples used in the tests
- `scripts/`: Python scripts used to run OntoNG with and without RAG
- `results/`: generated outputs (`.puml`, `.ttl`, `.json`)
- `notes/`: observations, issues, and methodological decisions
