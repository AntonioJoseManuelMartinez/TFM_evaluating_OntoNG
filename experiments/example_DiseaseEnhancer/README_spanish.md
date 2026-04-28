# Experimento con DiseaseEnhancer: comparación con y sin RAG

## Descripción general

En este experimento se evaluó el comportamiento de **OntoNG** sobre un conjunto de datos reales procedente de **DiseaseEnhancer**, una base de datos curada manualmente de enhancers humanos asociados a enfermedad. Los **enhancers** son secuencias reguladoras no codificantes capaces de modular la transcripción de genes diana, a menudo mediante interacciones cromatínicas a distancia, por lo que su alteración puede contribuir a procesos patológicos. La publicación original de DiseaseEnhancer describe el recurso como una colección de enhancers asociados a enfermedad, genes diana, tipos de enfermedad y variantes asociadas; su versión inicial incluía **847 enhancers asociados a enfermedad en 143 enfermedades humanas**. ([academic.oup.com](https://academic.oup.com/nar/article/46/D1/D78/4559115?utm_source=chatgpt.com))

Para este experimento se utilizó el recurso:
- `enh2disease-1.0.2.txt`
- Enlace: `http://biocc.hrbmu.edu.cn/DiseaseEnhancer/RFunctions/enh2disease-1.0.2.txt`

## Preparación de los datos

A partir del fichero original se generó un CSV limpio, `enh2disease_clean.csv`, mediante un script que transformó el archivo tabulado en una tabla con seis columnas:

- `enhancer_id`
- `chromosome`
- `start_position`
- `end_position`
- `associated_gene`
- `disease_name`

El script conservó la estructura semántica esencial del dataset y normalizó el formato cromosómico. :contentReference[oaicite:2]{index=2}

## Configuración experimental

Se compararon dos condiciones:

- **con RAG + QASAR**
- **sin RAG + QASAR**

En ambos casos se utilizó `gpt-5.4` como modelo generativo. En la condición con RAG, el backend estaba cargado con las 15 ontologías de BioGateway y la consulta se ejecutó con:

- `enable_terms_lookup=True`
- `enable_properties_lookup=True`
- `enable_relations_lookup=True`
- `top_k=15` :contentReference[oaicite:3]{index=3}

La condición sin RAG mantuvo el mismo flujo general, pero sin plugin de recuperación semántica. :contentReference[oaicite:4]{index=4}

## Estructura conceptual generada

En ambas condiciones OntoNG captó correctamente el núcleo semántico del problema, organizado alrededor de tres entidades principales:

- `Enhancer`
- `Gene`
- `Disease`

La diferencia principal no está en el número de clases explícitas, sino en cómo se representan. En la ejecución **con RAG**, la serialización Turtle final contiene tres clases explícitas: `Enhancer`, `Disease` y la clase reutilizada `sio:SIO_010035`, etiquetada como `gene`. Además, genera dos propiedades de objeto diferenciadas, `associatedWithDisease` y `associatedWithGene`, lo que produce una representación algo más específica. En la ejecución **sin RAG**, también aparecen tres clases explícitas (`Enhancer`, `Gene` y `Disease`), pero el gen se modela como una clase propia (`base:Gene`) y las relaciones quedan expresadas de forma más simple, mediante propiedades como `associatedWith` y `linkedTo`. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

En conjunto, ambas ejecuciones muestran que OntoNG representa correctamente el problema, mientras que la condición con RAG introduce reutilización explícita de una clase externa y una mayor especificidad en las relaciones.

## Resultado del mapeo con RAG

El fichero de mapeos mostró una reutilización semántica explícita, aunque limitada. El único término recuperado directamente fue:

- `Gene` → `http://semanticscience.org/resource/SIO_010035`
- puntuación: `1.0`
- ontología de origen: `gene` :contentReference[oaicite:7]{index=7}

No se recuperaron mapeos en:

- `mapped_relations`
- `mapped_properties` :contentReference[oaicite:8]{index=8}

Esto indica que el backend RAG estaba funcionando, pero que en este experimento la reutilización efectiva del contexto externo volvió a concentrarse en el nivel de **clases**, no en propiedades ni en relaciones.

## Evaluación con QASAR

### Con RAG

La ontología generada con RAG obtuvo una **puntuación global de 3.1716 / 5**. Entre los valores más relevantes destacan:

- **Característica estructural** = `3.0`
- **Mantenibilidad** = `4.0460`
- **Adecuación funcional** = `2.7349`
- **Cohesión** = `5.0`
- **Formalización** = `5.0`
- **Consistencia** = `5.0` :contentReference[oaicite:9]{index=9}

### Sin RAG

La ontología generada sin RAG obtuvo una **puntuación global de 3.2114 / 5**, ligeramente superior a la de la condición con RAG. Entre los valores principales destacan:

- **Característica estructural** = `3.1429`
- **Operabilidad** = `2.2380`
- **Adecuación funcional** = `2.8688`
- **Cohesión** = `5.0`
- **Formalización** = `5.0`
- **Consistencia** = `5.0` :contentReference[oaicite:10]{index=10}

En conjunto, la condición **sin RAG** aparece ligeramente mejor valorada por QASAR, probablemente porque genera una estructura algo más simple y contenida.

## Limitaciones principales

En ambas condiciones, la principal debilidad fue la falta de enriquecimiento léxico y documental:

- sinónimos por clase = `0.0`
- sinónimos por propiedad = `0.0`
- sinónimos por propiedad de objeto = `0.0`
- sinónimos por propiedad de datos = `0.0` 

Por tanto, aunque el RAG permitió reutilizar explícitamente la clase `Gene`, no produjo una mejora global de calidad según QASAR ni resolvió las carencias de documentación léxica.

## Interpretación global

Este experimento muestra un patrón distinto al de casos más complejos: aquí el problema conceptual es más directo y el modelo, incluso sin RAG, es capaz de generar una estructura pequeña, coherente y bien puntuada. La comparación entre ambas condiciones indica que el uso de RAG tuvo un efecto **real pero limitado**: permitió reutilizar explícitamente la clase `Gene`, pero esa mejora semántica localizada no se tradujo en una mejora global de calidad. 

En consecuencia, este caso apoya la idea de que el valor del RAG no debe medirse solo en términos de puntuación global, sino también en función de **qué componentes concretos consigue alinear o reutilizar**. En este experimento, el beneficio principal del RAG fue semántico y localizado, no estructural ni documental.

## Estructura de archivos del experimento

- `README_spanish.md`
- `enh2disease-1.0.2.txt`
- `enh2disease_clean.zip`
- `prepare_enh2disease_csv.py`
- `with_RAG/`
  - resultados de la ejecución con RAG
- `no_RAG/`
  - resultados de la ejecución sin RAG
