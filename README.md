# Evaluating OntoNG for Biomedical Ontology Generation

This repository contains the working material for a Master’s Thesis focused on evaluating ontology generation from real biomedical tabular datasets using large language models (LLMs), comparing **non-RAG** and **RAG-based** settings.

## Project overview

The thesis explores whether an ontology generation pipeline based on LLMs can produce meaningful biomedical ontologies from structured datasets, and whether the incorporation of **Retrieval-Augmented Generation (RAG)** with ontology-based context improves the resulting output.

The work is centered on three main questions:

1. Can OntoNG infer a plausible conceptual structure from real biomedical tabular data?
2. Does ontology-based context improve semantic alignment with existing biomedical vocabularies?
3. How do the generated ontologies behave in terms of structural quality and evaluation metrics?

## Experimental framework

The experimental pipeline combines the following components:

- **OntoNG** as the ontology generation engine
- **RAGannotationAPI** as the retrieval backend
- **Neo4j** for storing ontology embeddings
- **OpenAI GPT models** for schema and ontology generation
- **QASAR** for ontology quality evaluation

The comparison is performed under two main conditions:

- **without RAG**, using OntoNG alone
- **with RAG**, using OntoNG together with ontology context loaded into the retrieval backend

In this setup, the RAG component provides additional context to the LLM by retrieving relevant ontology fragments using vector similarity search over embeddings stored in Neo4j, a common approach in RAG pipelines :contentReference[oaicite:0]{index=0}.

## Ontology context used in RAG

The RAG backend was populated with a set of **15 BioGateway-related ontologies** converted to a format compatible with the embedding pipeline. These ontologies cover several biomedical subdomains related to genes, proteins, regulatory regions and chromosomal domains:

- `tad`
- `crm`
- `crm2gene`
- `crm2phen`
- `crm2tfac`
- `gene`
- `gene2phen`
- `prot`
- `prot2bp`
- `prot2cc`
- `prot2mf`
- `prot2prot`
- `reg2targ`
- `ortho`
- `tfac2gene`

Their role in the project is to provide structured semantic context that may be reused during ontology generation, especially at the level of classes, properties and relations.

## Datasets analyzed

The repository documents experiments on real biomedical resources related to gene regulation and genome organization, including:

- **TADKB**
- **DiseaseEnhancer**
- **ENdb**

These resources were transformed into tabular CSV datasets before being processed by OntoNG. In several cases, the original data were distributed across multiple raw files and required custom preprocessing scripts to build a unified structured dataset.

## Evaluation strategy

The experiments are designed to assess:

- the conceptual structure inferred from each dataset
- the degree of semantic reuse obtained through RAG
- the alignment between generated ontologies and the ontology context loaded in the backend
- and the structural and quality characteristics of the resulting ontologies

Ontology quality is evaluated using **QASAR**, which provides quantitative metrics and issue reports covering:

- structural consistency
- maintainability
- functional adequacy
- annotation richness
- lexical enrichment

## Current status

At the current stage of the thesis, the repository includes:

- ontology generation experiments **without RAG**
- ontology generation experiments **with RAG**
- ontology quality assessment using **QASAR**
- comparative analyses across multiple biomedical datasets
- processed datasets and generated outputs for each experimental condition

The results obtained so far indicate that RAG can improve semantic reuse in some cases, but that its effect is **selective and dependent on the dataset and its alignment with the ontology context**.

## Repository structure

The repository is organized into two main directories:

- `data/`  
  Contains transformed datasets, source-derived files and ontology context files used in RAG.

- `experiments/`  
  Contains scripts, outputs and documentation for each experiment, including:
  - conceptual diagrams (`.puml`)
  - generated ontologies (`.ttl`)
  - mapping files (`.json`)
  - QASAR evaluation results
  - experiment-specific notes

## Reproducibility

This repository serves as the experimental workspace of the thesis and documents the preprocessing, execution and evaluation steps followed in each case study.

Since the original biomedical resources were heterogeneous in format, preprocessing was required before ontology generation. Each experiment is associated with its corresponding dataset transformation and execution pipeline.

The repository is expected to evolve as additional experiments, refinements and comparisons are incorporated during the final stages of the thesis.
