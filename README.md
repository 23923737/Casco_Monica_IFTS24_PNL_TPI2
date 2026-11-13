Autor: Casco Monica
Fecha: 12/11/2026


# Buscador de lugares de atención de salud y alimentación sin TACC

## 1. Descripción del proyecto

Consultas relacionadas con celiaquía.

Originalmente el objetivo fue:

Esta aplicación permite buscar una ubicación por ejemplo "centro de atención de salud", luego localizar establecimientos gastronómicos cercanos, tomando como referencia una distancia aproximada de tres cuadras (300 metros) permitiendo identificar información sobre el tipo de comida que ofrecen los establecimientos y buscar referencias a opciones de alimentación sin TACC.

Por falta de documentacion oficial pública disponible de cada establecimiento se modificó el objetivo.
## 2. Objetivos
- Consultar información relacionada con celiaquia en Argentina


## 2. Objetivos desistidos
- Buscar una ubicacion
- Identificar establecimientos gastronómicos cercanos.
- Consultar el tipo de comida ofrecida.
- Detectar referencias a opciones sin TACC.
- Mostrar las fuentes utilizadas para responder las consultas.

## 3. Tecnologías utilizadas


- Visual Studio Code
- Python 3.12
- uv 
- Gradio 
- OpenStreetMap para la búsqueda de lugares.
- LangChain 
- ChromaDB 
- Ollama 
- bge-m3
- granite4


## 4. Funcionamiento general

La aplicación tendrá dos funcionalidades principales:

**A. Búsqueda de ubicación** Desistido

1. El usuario ingresa una ubicación ejemplo "centro de atención de salud".
2. Identifica su ubicación.
3. Busca establecimientos gastronómicos en un radio aproximado de 300 metros.
4. Presenta los resultados y la información disponible sobre sus opciones gastronómicas.

**B. Consulta de información sin TACC**

1. Se cargan documentos PDF sobre celiaquía y alimentación sin TACC, la sección mas compleja determinar legitimidad de origen.
2. Los documentos se dividen en fragmentos de texto.
3. Se generan embeddings y se almacenan en ChromaDB.
4. El usuario realiza una pregunta.
5. El sistema recupera los fragmentos relacionados.
6. Un modelo de lenguaje genera una respuesta utilizando la información recuperada.
7. Se muestran las fuentes y los fragmentos utilizados.

## 5. Instalación

Clonar o descargar el proyecto y abrir la carpeta en Visual Studio Code.

Crear el entorno virtual y activarlo

```powershell
uv venv --python 3.12
```

Instalar las dependencias:

```powershell
uv pip install -r requirements.txt
```

## 6. Ejecución

La aplicación se ejecutará desde la terminal de Visual Studio Code mediante:

```powershell
python app.py
```

Aqui te escribira en la terminal

Fragmentos disponibles: 237
* Running on local URL: aqui de escribe donde puedes visualizar para escribir tu consulta para mi caso era http://127.0.0.1*******


## 7. Consideraciones

La información sobre establecimientos gastronómicos depende de los datos disponibles en las fuentes consultadas.

CRUCIAL
La presencia de referencias a opciones sin TACC no garantiza que un establecimiento sea apto para personas con celiaquía. Se recomienda verificar directamente con el local sus procedimientos y condiciones de elaboración.

Las respuestas del sistema RAG deben mostrar las fuentes documentales utilizadas y no reemplazan el asesoramiento profesional.

Corpus identificación de los archivos con alias.
Documentación Oficial respaldatoria Argentinca
https://www.anmat.gob.ar/Enfermedad_Celiaca/Guia_BPM_ALG_gastronomicos_2017.pdf?utm_source=chatgpt.com
https://www.argentina.gob.ar/sites/default/files/celiaquia_-_guia_rapida_para_consumidores.pdf?utm_source=chatgpt.com

## 8. Estructura proyecto - Preparacion de la carpeta

```text
Buscador_salud_sin_tacc/
│
├── .venv/
├── datos/
│   ├── documentos/
│   └── vectores/
│
├── app.py
├── rag.py
├── buscador.py
├── requirements.txt
└── README.md
```
** dividida en 3 app para utilizar de forma independiente**




# Resumen Qué hace


El sistema trabaja con dos documentos PDF oficiales. 
Primero extrae el texto de los PDF, luego lo divide en fragmentos y utiliza el modelo BGE-M3 para convertirlos en vectores numéricos.

Estos vectores se almacenan en Chroma (Aclaración traida de la clase Chroma se usa para buscar)

Posteriormente, los fragmentos recuperados se envían a Granite 4, genera una respuesta utilizando el contexto disponible.

Finalmente, mediante Gradio desarrollé una interfaz web donde permite realizar una consulta y obtener una respuesta como los documentos y páginas utilizados como evidencia.

Durante las pruebas comprobé que el sistema puede recuperar información, responder consultas y abstenerse cuando no encuentra datos suficientes. También identifiqué que un modelo de lenguaje puede interpretar incorrectamente la evidencia, por lo que es necesario validar sus respuestas.
Por esta razón de modifica el texto incluido en el código def crear_cadena_rag():. Utilizando además de los sugeridos por el cuaderno base 7 otro como ser "No conviertas una posibilidad en certeza, una recomendación " Porque las respuestas incluia por ejemplo la palabra "garantiza", la cual no está contenida en los documentos originales.

Notas
## Transferencia al Trabajo Integrador 2

Este laboratorio trabaja un único documento que no se publica como corpus del proyecto. Para el integrador vas a necesitar al menos tres documentos reales y compartibles. Conservá esta tabla como punto de partida.

| Documento propio | Pregunta respondible | Página o sección esperada | ¿Qué recuperó? | ¿Qué interpretó el modelo? | Límite observado |
|---|---|---|---|---|---|
| Que es la celiaquia | La celiaquia es una enfermedad sistémica autoinmune producida por la intolerancia permanente al gluten en individuos genéticamente predispuestos. Esta intolerancia puede presentarse en cualquier momento de la vida desde la lactancia hasta la adultez avanzada. Dado que afecta la mucosa del intestino, puede conducir a una malabsorción de nutrientes esenciales. En Argentina, se ha estimado que 1/167 personas adultas son celíacas y 1/79 individuos en otros estudios. [1][2] | La celiaquía es la inflamación del intestino provocada por intolerancia al gluten.              
Las personas afectadas deben evitar cereales con gluten y sus derivados. | Correctamente la solicitud | Completá | Completá |
| Que presupuesto tengo en casa | Organizar el dinero del hogar es dividir tus ingresos netos mensuales (lo que entra limpio a la casa)  | NA | Lo inventó | Requerir escriba no posee respuesta | Completá |
| Completá | Utilizar papel descartable y una solución de alcohol etílico para limpiar la vajilla. [1] [2] | Utilizar papel descartable y una solución de alcohol etílico para limpiar la vajilla. Garantiza evitar la contaminación cruzada | Inventó | No debe convertir una recomentadion en certeza | Completá |

## Glosario

| Término | Qué significa en este laboratorio |
|---|---|
| **Documento** | Texto y metadatos de una página cargada con LangChain. |
| **Metadato** | Dato de procedencia, como el archivo y el índice de página. |
| **Fragmento** | Parte de una página que se puede representar y recuperar por separado. |
| **Embedding** | Vector que el modelo `bge-m3` usa para comparar significados. |
| **Chroma** | Base vectorial que conserva fragmentos, vectores y metadatos. |
| **k** | Cantidad de fragmentos recuperados para armar el contexto. |
| **RAG** | Recuperación de evidencia seguida de generación con ese contexto. |
| **Abstención** | Reconocimiento de que el contexto no alcanza para responder. |
| **Trazabilidad** | Posibilidad de volver desde una respuesta hasta el fragmento y la página original. |


Chroma
La celda anterior no decide cuál fragmento es mejor: sólo comprueba que la pregunta y ambos textos se representan con el mismo modelo. Ahora construimos dos índices temporales en memoria para comparar la evidencia recuperada. La distancia menor indica mayor cercanía según esta colección; no es una probabilidad de verdad.

indice_breve = Chroma.from_documents(
    documents=fragmentos_breves,
    embedding=embeddings,
    collection_name="laboratorio_comparacion_breve",
)
indice_amplio = Chroma.from_documents(
    documents=fragmentos_amplios,
    embedding=embeddings,
    collection_name="laboratorio_comparacion_amplio",
)

hallazgo_breve = indice_breve.similarity_search_with_score(
    query=pregunta_de_comparacion,
    k=1,
)[0]
hallazgo_amplio = indice_amplio.similarity_search_with_score(
    query=pregunta_de_comparacion,
    k=1,
)[0]

for nombre, hallazgo in [("Breve", hallazgo_breve), ("Amplio", hallazgo_amplio)]:
    documento, distancia = hallazgo
    print(f"\n{nombre} — página {documento.metadata['page'] + 1}")
    print("Distancia:", round(distancia, 3))
    print(documento.page_content)
