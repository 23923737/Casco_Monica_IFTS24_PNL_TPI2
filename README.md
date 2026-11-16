Autor: Casco Monica
Fecha: 12/11/2026
Actualización: 16/11/2026

# Buscador de información sobre celiaquía y alimentación sin TACC

## 1. Descripción del proyecto

Este proyecto desarrolla una aplicación para consultar información sobre celiaquía, alimentación sin TACC y recomendaciones relacionadas con la seguridad alimentaria. La solución combina recuperación documental con un modelo de lenguaje para responder preguntas basadas en evidencia, mostrando además las fuentes consultadas para cada respuesta.

La aplicación trabaja con documentos PDF, los divide en fragmentos, los transforma en embeddings, los almacena en una base vectorial y recupera los textos más relevantes para la consulta del usuario. Luego utiliza un modelo generativo para construir una respuesta apoyada en el contexto recuperado.

## 2. Objetivo general

Diseñar y evaluar un sistema de búsqueda semántica para responder preguntas sobre alimentos sin TACC, con especial atención a la trazabilidad de la evidencia y a la prevención de respuestas inventadas o interpretaciones incorrectas.

## 3. Objetivos específicos

- Buscar información relevante sobre celiaquía y alimentación sin TACC.
- Recuperar fragmentos útiles de documentos oficiales.
- Generar respuestas apoyadas en evidencia documental.
- Mostrar las fuentes utilizadas para cada respuesta.
- Evitar afirmaciones no respaldadas por el corpus.
- Promover una lectura crítica de las respuestas del sistema.

## 4. Tecnologías utilizadas

- Python 3.12
- Gradio
- LangChain
- ChromaDB
- Ollama
- PyPDF
- bge-m3
- granite4:latest
- Visual Studio Code

## 5. Método de trabajo

El sistema sigue un flujo de trabajo basado en RAG (Retrieval-Augmented Generation):

1. Se cargan los documentos PDF desde la carpeta `datos/documentos`.
2. El texto se extrae página por página.
3. Los documentos se dividen en fragmentos.
4. Se generan embeddings con el modelo `bge-m3`.
5. Los fragmentos y vectores se almacenan en Chroma.
6. El usuario realiza una pregunta.
7. El sistema recupera los fragmentos más relevantes.
8. El modelo genera una respuesta con base en ese contexto.
9. Se muestran los fragmentos usados como evidencia.

## 6. Estructura del proyecto

```text
Buscador_salud_sin_tacc/
├── .venv/
├── datos/
│   ├── documentos/
│   └── vectores/
│       └── chroma_db_sin_tacc/
├── rag.py
├── rag 1.py
├── requirements.txt
├── README.md
├── .gitignore
└── .gradio/
```

## 7. Instalación

Clonar el repositorio e ingresar al directorio del proyecto:

```bash
git clone <URL-del-repositorio>
cd Buscador_salud_sin_tacc
```

Crear y activar el entorno virtual:

```powershell
uv venv --python 3.12
```

Instalar las dependencias:

```powershell
uv pip install -r requirements.txt
```

Alternativa con `pip`:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 8. Ejecución

Para levantar la interfaz de consulta:

```powershell
python rag.py
```

La aplicación levantará una interfaz web local con una URL similar a:

```text
http://127.0.0.1:7860/
```

## 9. Uso de la aplicación

1. Abrir la URL mostrada por Gradio.
2. Escribir una pregunta relacionada con celiaquía o alimentación sin TACC.
3. El sistema recupera fragmentos relevantes del índice vectorial.
4. El modelo responde utilizando ese contexto.
5. La interfaz muestra la respuesta y las fuentes documentales empleadas.

Ejemplos de consultas:

- ¿Qué recomendaciones existen para evitar la contaminación cruzada?
- ¿Qué alimentos se mencionan para personas con celiaquía?
- ¿Qué información hay sobre alimentación sin TACC?

## 10. Consideraciones importantes

- La información se basa únicamente en los documentos cargados en el sistema.
- La presencia de una referencia a opciones sin TACC no garantiza que un local sea apto para personas con celiaquía.
- El sistema no reemplaza el criterio profesional ni la verificación directa con establecimientos.
- Las respuestas deben interpretarse como síntesis documental, no como diagnóstico ni validación.

## 11. Criterio de evaluación

El proyecto busca analizar la calidad de un sistema RAG en un caso real de salud alimentaria, evaluando:

- calidad de la recuperación semántica;
- precisión y trazabilidad de las respuestas;
- capacidad de abstenerse cuando no hay evidencia suficiente;
- prevención de alucinaciones o interpretaciones excesivas;
- claridad de las referencias utilizadas.

## 12. Limitaciones

- Es necesario validar la respuesta del modelo frente al contenido original del documento.
- Consultas muy amplias o ambiguas pueden devolver fragmentos incompletos.
- La interpretación del lenguaje puede requerir control y validación manual.
- Para una versión más robusta, el corpus debería ampliarse con más documentos oficiales y verificables.

## 13. Referencias documentales

El proyecto se apoya en información documental que debe ser verificada y citada con cuidado. Se recomienda trabajar con fuentes oficiales y confiables, por ejemplo:

- ANMAT
- Guías nacionales sobre celiaquía
- Documentación pública sanitaria y alimentaria
- Normativas y recomendaciones del ámbito argentino

## 14. Glosario

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

## 15. Resumen ejecutivo

Este proyecto implementa un buscador textual basado en RAG para responder preguntas sobre celiaquía y alimentos sin TACC. El sistema recupera fragmentos relevantes desde documentos PDF, los representa con embeddings y genera respuestas apoyadas en contexto. La clave del trabajo es la trazabilidad: cada respuesta debe estar vinculada a la evidencia documental y evitar inferencias no respaldadas.

## 16. Licencia

Este proyecto se entrega como trabajo práctico académico. Se recomienda revisar la licencia del repositorio y de los documentos fuente antes de reutilizarlo en contextos profesionales o públicos.
