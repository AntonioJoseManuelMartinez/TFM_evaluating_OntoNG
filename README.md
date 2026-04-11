# Evaluating_OntoNG

Repositorio de trabajo del Trabajo Fin de Máster sobre evaluación de generación de ontologías a partir de datasets biomédicos mediante LLMs, comparando condiciones **sin RAG** y **con RAG**.

## Objetivo

El objetivo de este trabajo es evaluar la capacidad de un sistema basado en modelos de lenguaje para:

1. inferir un esquema ontológico a partir de datos tabulares biomédicos,
2. generar una ontología en formato RDF/OWL/Turtle,
3. comparar el resultado generado automáticamente con esquemas/ontologías manuales de referencia,
4. analizar si el uso de **RAG** con ontologías de contexto mejora el resultado respecto a una ejecución sin RAG.

## Entorno de trabajo

- **OntoNG** como motor principal de generación ontológica.
- **RAGannotationAPI** como backend RAG.
- **Neo4j** para almacenamiento de embeddings ontológicos.
- Modelos GPT de OpenAI para las fases de generación.
- Ontologías de contexto derivadas de BioGateway, entre ellas:
  - `crm`
  - `crm2gene`
  - `crm2phen`

## Dataset inicial utilizado

El primer experimento real se ha realizado con una muestra de 25 filas de `enh2disease-1.0.2.txt`, procedente de **DiseaseEnhancer**, una base de datos de asociaciones entre enhancers y enfermedades.

## Estructura del repositorio

- `experiments/`: descripción de los experimentos realizados.
- `data/samples/`: muestras de datos utilizadas en las pruebas.
- `scripts/`: scripts Python empleados para ejecutar OntoNG con y sin RAG.
- `results/`: resultados generados (`.puml`, `.ttl`, `.json`).
- `notes/`: observaciones, incidencias y decisiones metodológicas.
