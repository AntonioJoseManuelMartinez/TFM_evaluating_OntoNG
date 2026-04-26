# Experimento con TADKB: generación ontológica con OntoNG, RAG y QASAR

## Descripción general

Este experimento evalúa el comportamiento de **OntoNG** sobre un conjunto de datos biomédicos reales relacionado con la **organización tridimensional del genoma**, utilizando **RAG** y **QASAR** como componentes complementarios del pipeline.

La fuente de datos utilizada fue **TADKB**, un recurso centrado en los **topologically associating domains (TADs)**. Los TADs son dominios genómicos caracterizados por presentar una mayor frecuencia de contactos cromatínicos internos que con regiones vecinas, y se consideran una de las unidades mejor estudiadas de la arquitectura 3D del genoma. Se trata de estructuras relevantes para la organización cromosómica y para la delimitación de contextos regulatorios.

Para este experimento se utilizó el recurso:

- `TAD_annotations.tar.gz`
- Enlace: `http://dna.cs.miami.edu/TADKB/download/TAD_annotations.tar.gz`

Según la publicación original de TADKB, este recurso integra TADs detectados en múltiples tipos celulares humanos, junto con información complementaria sobre estructuras 3D, genes codificantes, lncRNAs y familias de TADs. Además, incluye TADs inferidos con distintos métodos de llamada, como **Directionality Index (DI)**, **GMAP** e **Insulation Score (IS)**, e incorpora variantes experimentales como **HiChIP** y **SPRITE**.

---

## Preparación de los datos

En lugar de seleccionar únicamente unos pocos ficheros, en este experimento se utilizaron **todos los archivos `.txt`** contenidos en `TAD_annotations.tar.gz`, con el fin de proporcionar a OntoNG una representación más amplia y heterogénea del dominio.

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

---

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

El objetivo fue evaluar el mayor grado posible de reutilización del contexto ontológico disponible.

---

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
- una clase intermedia de **observación o anotación de TAD**

Esto es metodológicamente relevante porque muestra que, al ampliar el conjunto de entrada a todos los ficheros del recurso, OntoNG no redujo toda la información a una única estructura genérica. En cambio, fue capaz de separar entidades propias del dominio de aquellas relacionadas con el contexto experimental.

La ontología generada presentó además una jerarquía simple y formalmente consistente. QASAR informó de:

- **Tangledness (complejidad estructural)** = `1.0`
- **Cohesión** = `5.0`
- **Consistencia** = `5.0`

Esto sugiere una ontología pequeña pero coherente, sin signos importantes de incoherencia estructural.

---

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

Este resultado es claramente mejor que el de ejecuciones previas, en las que el sistema detectaba la disponibilidad de las ontologías pero no devolvía reutilización explícita de vocabulario.

A partir de aquí puede afirmarse que existe una **reutilización parcial del conocimiento ontológico de referencia**, al menos a nivel de **clases o términos**. En particular:

- el alineamiento de `TAD` con `SO_0002304`
- y el alineamiento de `Database` con `NCIT_C15426`

ambos con puntuación máxima, indican que el sistema fue capaz de conectar conceptos relevantes de la ontología generada con términos ya presentes en las ontologías cargadas en el backend.

### Interpretación importante

Los bloques `mapped_relations` y `mapped_properties` permanecieron vacíos.

Este resultado debe interpretarse con cuidado. Tras consultar con Andrea, que validó la parte técnica del módulo RAG, se confirmó que los componentes relacionados con:

- carga de embeddings
- almacenamiento
- recuperación semántica

estaban funcionando correctamente en este caso.

Por tanto, la ausencia de reutilización explícita de propiedades y relaciones **no debe interpretarse como un fallo técnico del backend**, sino más bien como una consecuencia del comportamiento del modelo durante la generación del grafo a partir de los datos.

En otras palabras, factores como:

- la estructura del dataset
- la forma en que se representan las entidades
- el contexto efectivo que recibe el modelo

pueden condicionar que la reutilización aparezca con claridad en **clases**, pero no necesariamente en **propiedades** o **relaciones**.

Esta observación es especialmente importante para interpretar el experimento: el resultado sugiere que el efecto del RAG sobre la ontología final depende de **cómo el modelo aprovecha el contexto recuperado**. En este caso, la reutilización semántica fue clara a nivel de **términos/clases**, pero no a nivel de **propiedades** ni de **relaciones**.

---

## Evaluación con QASAR

La ontología generada fue evaluada con QASAR, obteniendo una **puntuación global de 3.0978 / 5**.

Este valor sitúa el resultado en un **rango intermedio**, lo que permite considerar la ontología como estructuralmente razonable y utilizable, aunque todavía alejada de un recurso altamente enriquecido desde el punto de vista terminológico y documental.

### Puntos fuertes

Varias subcaracterísticas estructurales mostraron valores favorables:

- **Característica estructural** = `3.43`
- **Cohesión** = `5.0`
- **Redundancia** = `5.0`
- **Formalización** = `5.0`
- **Consistencia** = `5.0`

Esto indica que la ontología no presenta incoherencias graves, ni una estructura especialmente desordenada, ni redundancia problemática.

Además:

- **Profundidad de la jerarquía de subsunción** = `2.0`
- **Tangledness / complejidad por herencia múltiple** = `1.0`

Esto sugiere una jerarquía sencilla y sin conflictos estructurales graves.

### Mantenibilidad y funcionalidad

La ontología también mostró valores razonables en mantenibilidad y adecuación funcional:

- **Característica de mantenibilidad** = `3.47`
- **Adecuación funcional** = `3.12`

Dentro de este perfil funcional, destacaron especialmente:

- **Capacidad de agrupamiento (clustering)** = `5.0`
- **Capacidad de guía** = `5.0`
- **Consistencia en búsqueda y consulta** = `4.2`
- **Reconciliación de esquemas y valores** = `3.67`

Estos resultados sugieren que la ontología puede ser útil como estructura de organización conceptual y como recurso para consultas coherentes, aunque todavía no alcance un alto grado de madurez documental.

### Riqueza de anotación y atributos

Otras métricas favorables fueron:

- **Riqueza de anotación** = `0.8889`
- **Riqueza de atributos** = `1.8889`

Ambas alcanzaron su valor escalado máximo. Esto sugiere que la ontología presenta un nivel aceptable de anotaciones y de atributos o restricciones por clase, reforzando la idea de que el resultado no es meramente esquelético.

---

## Principales limitaciones detectadas

A pesar de los aspectos positivos anteriores, QASAR también reveló limitaciones claras.

### Falta de enriquecimiento léxico

La limitación más evidente fue la ausencia de enriquecimiento léxico:

- **Sinónimos por clase** = `0.0`
- **Sinónimos por propiedad** = `0.0`
- **Sinónimos por propiedad de objeto** = `0.0`
- **Sinónimos por propiedad de datos** = `0.0`

En coherencia con ello, la distribución de incidencias mostró:

- **Clases sin sinónimos**: `8`
- **Propiedades de objeto sin sinónimos**: `7`
- **Propiedades de datos sin sinónimos**: `10`
- **Propiedades de anotación sin sinónimos**: `10`

Estas incidencias no implican necesariamente un fallo lógico en la ontología, pero sí indican una limitación en términos de madurez ontológica. La ausencia de sinónimos reduce la interoperabilidad léxica y limita la utilidad del recurso para tareas de anotación, búsqueda semántica y procesamiento del lenguaje natural.

### Problemas relacionados con anotaciones

Otro grupo de incidencias afectó a propiedades de anotación estándar como:

- `dc:title`
- `dc:creator`
- `dcterms:description`
- `owl:versionInfo`
- `rdfs:label`
- propiedades `vann`

QASAR las marcó como carentes de nombre, descripción o sinónimos. Este patrón debe interpretarse con cautela, ya que no necesariamente refleja un defecto conceptual de la ontología generada, sino el hecho de que QASAR evalúa de forma estricta este tipo de propiedades, mientras que las ontologías generadas automáticamente no suelen estar enriquecidas en ese nivel.

### Operabilidad y calidad en uso

También se observaron valores bajos en:

- **Característica de operabilidad** = `2.26`
- **Calidad en uso** = `1.89`

Esto es coherente con la naturaleza del recurso generado: una ontología formalmente aceptable y estructuralmente consistente, pero todavía poco amigable desde la perspectiva de reutilización humana, explicación y documentación terminológica.

---

## Interpretación global

Este experimento permite extraer varias conclusiones relevantes.

### 1. Viabilidad técnica

El pipeline completo **OntoNG + RAG + QASAR** puede ejecutarse correctamente sobre un dataset biomédico real y relativamente amplio derivado de TADKB. La integración de todos los `.txt` en un único CSV y la generación de una ontología evaluable demuestran la viabilidad técnica del enfoque sobre datos reales de organización 3D del genoma.

### 2. Impacto positivo del backend RAG actualizado

El experimento muestra también que la actualización del backend RAG y el recálculo de embeddings tuvieron un efecto positivo real. En esta ejecución se recuperaron mapeos explícitos hacia ontologías de referencia, especialmente para:

- `TAD`
- `Database`
- `TADObservation`

Esto apoya la idea de que, al menos en esta versión del experimento, el uso de RAG contribuyó a un cierto grado de **alineamiento semántico** entre la ontología generada y el vocabulario ontológico previamente cargado.

### 3. La mejora es real, pero parcial

La mejora no es completa. Aunque se obtuvieron mapeos útiles a nivel de clases, no se recuperaron propiedades ni relaciones.

Dado que la infraestructura técnica del módulo RAG fue validada como funcional, este resultado no debe atribuirse a un mal funcionamiento del backend. Más bien debe interpretarse como parte de la propia pregunta de investigación: **en qué condiciones el modelo reutiliza clases, propiedades o relaciones del contexto ontológico, y en cuáles no**.

### Conclusión final

En este caso, el uso de RAG con ontologías de BioGateway no transformó automáticamente la ontología generada en un recurso completamente alineado y maduro. Sin embargo, sí aportó una **reutilización semántica concreta y medible** en componentes relevantes del modelo.

Esto hace que el experimento sea valioso no solo porque muestra que es posible reutilizar vocabulario ontológico externo, sino también porque evidencia que dicha reutilización es **selectiva** y depende de la interacción entre:

- el tipo de datos de entrada
- el grafo conceptual generado por el modelo
- y la forma en que el modelo aprovecha el contexto ontológico recuperado

---

## Archivos de este experimento

Los principales archivos asociados a este experimento son:

- `tad_all_files.csv`
- `tad_all_rag_qasar.puml`
- `tad_all_rag_qasar_mappings.json`
- `tad_all_rag_qasar.ttl`
- `tad_all_rag_qasar_report.json`

---

## Nota final

Este experimento es relevante para porque proporciona un caso realista en el que:

- el RAG contribuye a la reutilización semántica
- dicha reutilización es detectable e interpretable
- pero su efecto no es completo ni uniforme en todos los componentes de la ontología
