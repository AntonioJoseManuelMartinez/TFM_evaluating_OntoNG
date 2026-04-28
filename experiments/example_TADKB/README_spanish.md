# Experimento con TADKB: generación ontológica con OntoNG, RAG y QASAR

## Descripción general

Este experimento evaluó el comportamiento de **OntoNG** sobre un conjunto de datos biomédicos reales relacionado con la **organización tridimensional del genoma**, utilizando **RAG** y **QASAR** como componentes complementarios del pipeline.

La fuente de datos utilizada fue **TADKB**, un recurso centrado en los **topologically associating domains (TADs)**. Los TADs son dominios genómicos caracterizados por presentar una mayor frecuencia de contactos cromatínicos internos que con regiones vecinas y se consideran una de las unidades estructurales y funcionales mejor estudiadas del genoma. El recurso TADKB integra TADs detectados en múltiples tipos celulares, junto con información adicional sobre estructuras 3D, genes codificantes, lncRNAs y familias de TADs. ([bmcgenomics.biomedcentral.com](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-5551-2?utm_source=chatgpt.com))

Para este experimento se utilizó el recurso:

- `TAD_annotations.tar.gz`
- Enlace: `http://dna.cs.miami.edu/TADKB/download/TAD_annotations.tar.gz`

## Preparación de los datos

En lugar de seleccionar solo unos pocos ficheros, en este experimento se utilizaron **todos los archivos `.txt`** contenidos en `TAD_annotations.tar.gz`, con el fin de proporcionar a OntoNG una representación más amplia y heterogénea del dominio.

A partir de ellos se construyó un único dataset tabular, `tad_all_files.csv`, generado mediante la extracción y combinación de todos los `.txt` del recurso. Cada fila del CSV representa una observación de TAD e incluye:

- `chromosome`
- `start_position`
- `end_position`
- `source_method`
- `cell_type`
- `calling_method`
- `resolution`
- `source_file`
- `database_name`

Esta transformación permitió adaptar un conjunto de datos originalmente distribuido en múltiples ficheros planos a un formato tabular adecuado para su procesamiento por OntoNG.

## Configuración del pipeline

Se ejecutó un pipeline completo basado en **OntoNG + RAG + QASAR**.

### Configuración principal

- **Modelo generativo:** `gpt-5.4`
- **Backend RAG:** ontologías de BioGateway embebidas en **Neo4j**
- **Número de ontologías cargadas en RAG:** 15
- **Configuración de la consulta RAG:**
  - `enable_terms_lookup=True`
  - `enable_properties_lookup=True`
  - `enable_relations_lookup=True`
  - `top_k=15`

El objetivo fue evaluar el mayor grado posible de reutilización del contexto semántico disponible.

## Estructura conceptual generada por OntoNG

El resultado obtenido a partir del dataset completo no fue una representación plana, sino una ontología con una **estructura conceptual relativamente articulada**.

QASAR identificó:

- **8 clases**
- una densidad de propiedades y relaciones suficiente para considerar que la ontología no es meramente descriptiva

Entre las clases inferidas aparecieron entidades relacionadas tanto con el dominio biológico como con el contexto experimental y de procedencia, como:

- `TAD`
- `CellType`
- `CallingMethod`
- `Resolution`
- `SourceMethod`
- `SourceFile`
- `Database`
- una clase intermedia de observación o anotación de TAD

Esto indica que, al ampliar el conjunto de entrada a todos los ficheros del recurso, OntoNG no redujo toda la información a una única estructura genérica, sino que fue capaz de separar entidades propias del dominio de aquellas relacionadas con el contexto experimental.

La ontología generada presentó además una jerarquía simple y formalmente consistente. QASAR informó de:

- **Cohesión** = `5.0`
- **Consistencia** = `5.0`
- **Formalización** = `5.0`

lo que sugiere una ontología pequeña pero coherente y sin conflictos estructurales graves.

## Resultado del mapeo con RAG

En esta ejecución, el backend RAG dejó de devolver una salida vacía. El fichero de mapeos mostró que el sistema reconoció correctamente las ontologías cargadas y recuperó **tres términos mapeados explícitamente**:

- **TAD** → `http://purl.obolibrary.org/obo/SO_0002304`  
  Puntuación: `1.0`  
  Ontología de origen: `tad`

- **Database** → `http://purl.obolibrary.org/obo/NCIT_C15426`  
  Puntuación: `1.0`  
  Ontología de origen: `crm2gene`

- **TADObservation** → `http://rdf.biogateway.eu/tad//tad_id`  
  Puntuación: `0.5561`  
  Ontología de origen: `tad`

Este resultado indica una **reutilización parcial del conocimiento de referencia**, al menos a nivel de clases o términos. En particular, el alineamiento de `TAD` con `SO_0002304` y de `Database` con `NCIT_C15426`, ambos con puntuación máxima, muestra que el sistema fue capaz de conectar conceptos relevantes de la ontología generada con términos ya presentes en las ontologías cargadas en el backend.

No obstante, los bloques `mapped_relations` y `mapped_properties` permanecieron vacíos. Esto sugiere que la reutilización semántica fue clara a nivel de **clases**, pero no a nivel de **propiedades** o **relaciones**.

## Evaluación con QASAR

La ontología generada fue evaluada con QASAR, obteniendo una **puntuación global de 3.0978 / 5**.

Este valor sitúa el resultado en un rango intermedio, lo que permite considerar la ontología como estructuralmente razonable y utilizable, aunque todavía alejada de un recurso altamente enriquecido desde el punto de vista terminológico y documental.

### Puntos fuertes

Entre las métricas más favorables destacan:

- **Característica estructural** = `3.43`
- **Cohesión** = `5.0`
- **Redundancia** = `5.0`
- **Formalización** = `5.0`
- **Consistencia** = `5.0`

Además:

- **Profundidad de la jerarquía de subsunción** = `2.0`
- **Complejidad por herencia múltiple** = `1.0`

Estos resultados sugieren una jerarquía sencilla y una estructura formalmente consistente.

También se observaron valores razonables en:

- **Mantenibilidad** = `3.47`
- **Adecuación funcional** = `3.12`

y métricas favorables como:

- **Capacidad de agrupamiento** = `5.0`
- **Capacidad de guía** = `5.0`
- **Consistencia en búsqueda y consulta** = `4.2`
- **Reconciliación de esquemas y valores** = `3.67`

### Limitaciones principales

La principal debilidad detectada por QASAR fue la falta de enriquecimiento léxico:

- **Sinónimos por clase** = `0.0`
- **Sinónimos por propiedad** = `0.0`
- **Sinónimos por propiedad de objeto** = `0.0`
- **Sinónimos por propiedad de datos** = `0.0`

En coherencia con ello, se detectaron incidencias relacionadas con:

- clases sin sinónimos
- propiedades de objeto sin sinónimos
- propiedades de datos sin sinónimos
- propiedades de anotación sin sinónimos

Esto no implica necesariamente un fallo lógico en la ontología, pero sí indica una carencia importante en términos de madurez documental y reutilización léxica.

También se observaron valores bajos en:

- **Operabilidad** = `2.26`
- **Calidad en uso** = `1.89`

lo que sugiere que, aunque la ontología es estructuralmente válida, todavía es poco amigable desde la perspectiva de reutilización humana y documentación terminológica.

## Interpretación global

Este experimento demuestra que el pipeline completo **OntoNG + RAG + QASAR** puede ejecutarse correctamente sobre un dataset biomédico real y relativamente amplio derivado de TADKB.

Además, muestra que la actualización del backend RAG y el recálculo de embeddings tuvieron un efecto positivo real. En esta ejecución se recuperaron mapeos explícitos hacia ontologías de referencia, especialmente para:

- `TAD`
- `Database`
- `TADObservation`

Esto apoya la idea de que, al menos en este experimento, el uso de RAG contribuyó a un cierto grado de **alineamiento semántico** entre la ontología generada y el vocabulario previamente cargado.

Sin embargo, la mejora fue **parcial**. Aunque se obtuvieron mapeos útiles a nivel de clases, no se recuperaron propiedades ni relaciones. Por tanto, este caso sugiere que el efecto del RAG no es uniforme: puede mejorar la reutilización de ciertos componentes del modelo sin transformar automáticamente la ontología generada en un recurso completamente alineado y maduro.

## Archivos del experimento

Los principales archivos asociados a este experimento son:

- `tad_all_files.csv`
- `tad_all_rag_qasar.puml`
- `tad_all_rag_qasar_mappings.json`
- `tad_all_rag_qasar.ttl`
- `tad_all_rag_qasar_report.json`
