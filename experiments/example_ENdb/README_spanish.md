# Experimento con ENdb: comparación con y sin RAG

## Descripción general

En este experimento se evaluó el comportamiento de **OntoNG** sobre un dataset biomédico complejo procedente de **ENdb**, una base de datos curada manualmente de enhancers soportados experimentalmente en humano y ratón. 
Los enhancers son elementos reguladores cis capaces de modular la transcripción génica mediante interacciones a distancia y están estrechamente relacionados con procesos biológicos y enfermedades. 
ENdb integra información sobre enhancers, genes diana, factores de transcripción y enfermedades, proporcionando un recurso rico para el estudio de redes regulatorias. ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/31665430/))

Para este experimento se utilizaron los siguientes ficheros del recurso:

- `enhancer_main.txt`
- `enhancer_gene.txt`
- `enhancer_TF.txt`

Enlace: `http://www.licpathway.net/ENdb/Download.php`

## Preparación de los datos

A partir de los tres ficheros originales se generó un único dataset estructurado, `endb_human_clean.csv`, mediante un script que:

- concatenó los tres recursos,
- filtró los registros humanos,
- eliminó duplicados,
- y conservó las variables más relevantes.

El dataset final contiene **3904 filas** y las siguientes columnas:

- `enhancer_id`
- `chromosome`
- `start_position`
- `end_position`
- `enhancer_type`
- `tissue_context`
- `disease_name`
- `target_gene`
- `transcription_factor`

Este proceso permitió adaptar un recurso distribuido y heterogéneo a un formato tabular adecuado para OntoNG.

## Configuración experimental

Se compararon dos condiciones:

- **con RAG + QASAR**
- **sin RAG + QASAR**

En la condición con RAG:

- ontologías de BioGateway cargadas en el backend
- `enable_terms_lookup=True`
- `enable_properties_lookup=True`
- `enable_relations_lookup=True`
- `top_k=15`

En ambas condiciones se utilizó `gpt-5.4` como modelo generativo.

## Estructura conceptual generada

En ambas ejecuciones, OntoNG captó correctamente el núcleo semántico del dataset y generó una ontología más rica que en experimentos anteriores.

QASAR identificó:

- **6 clases** en ambas condiciones

Las entidades principales incluyen:

- `Enhancer`
- `Gene`
- `Disease`
- `Tissue`
- `TranscriptionFactor`
- `RegulatoryAssociation`

La diferencia principal radica en el grado de alineamiento:

- **Con RAG:** reutilización explícita de clases externas y modelado más claro de las relaciones regulatorias
- **Sin RAG:** estructura similar pero completamente autocontenida

Desde el punto de vista estructural, ambas ontologías presentan:

- cohesión = `5.0`
- redundancia = `5.0`
- formalización = `5.0`
- consistencia = `5.0`
- profundidad jerárquica = `2.0`
- tangledness = `0.0`

## Resultado del mapeo con RAG

El fichero de mapeos mostró una reutilización semántica más rica que en experimentos previos.

**Mapped terms:**

- `Gene` → `http://semanticscience.org/resource/SIO_010035` (score = 1.0)
- `TranscriptionFactor` → `http://purl.obolibrary.org/obo/NCIT_C17207` (score = 1.0)
- `RegulatoryAssociation` → `http://purl.obolibrary.org/obo/SO_0000727` (score = 0.5563)

No se detectaron mapeos en:

- `mapped_properties`
- `mapped_relations`

Esto confirma que la reutilización semántica se concentra en **clases**, no en propiedades ni relaciones.

## Evaluación con QASAR

### Con RAG

- **Puntuación global** = `3.1732 / 5`
- **Característica estructural** = `3.2857`
- **Mantenibilidad** = `3.7246`
- **Adecuación funcional** = `3.1025`
- **Compatibilidad** = `3.75`

### Sin RAG

- **Puntuación global** = `3.1335 / 5`
- **Característica estructural** = `3.2857`
- **Mantenibilidad** = `3.5786`
- **Adecuación funcional** = `3.0766`
- **Compatibilidad** = `3.5`

En este caso, la condición **con RAG** muestra una ligera mejora global, especialmente en alineamiento semántico y mantenibilidad.

## Limitaciones principales

Ambas ontologías presentan limitaciones similares:

- sinónimos por clase = `0.0`
- sinónimos por propiedad = `0.0`
- sinónimos por propiedad de objeto = `0.0`
- sinónimos por propiedad de datos = `0.0`

Principales incidencias:

- propiedades de anotación sin descripción
- propiedades sin nombre o sin sinónimos
- clases sin enriquecimiento léxico

Además:

- operabilidad ≈ `2.25`
- calidad en uso ≈ `1.88`

Esto indica que las ontologías son estructuralmente válidas, pero todavía poco maduras desde el punto de vista documental.

## Interpretación global

Este experimento representa el caso más favorable para el uso de RAG dentro del trabajo. A diferencia de otros datasets, ENdb presenta una estructura semántica más alineada con las ontologías de BioGateway, lo que permite una reutilización más rica de conceptos como `Gene`, `TranscriptionFactor` y `RegulatoryAssociation`.

Sin embargo, el efecto del RAG sigue siendo **parcial**:

- mejora la reutilización semántica a nivel de clases,
- pero no se extiende a propiedades ni relaciones,
- y el impacto en la calidad global sigue siendo moderado.

Esto refuerza la idea de que la utilidad del RAG depende en gran medida del grado de correspondencia entre el dataset y el contexto ontológico disponible.

## Estructura de archivos del experimento

- `README_spanish.md`
- `endb_human_clean.csv`
- `prepare_endb_csv.py`
- `with_RAG/`
  - resultados de la ejecución con RAG
- `no_RAG/`
  - resultados de la ejecución sin RAG
