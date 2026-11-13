
from pathlib import Path
import sys

import gradio as gr

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. Configuración

CARPETA_DOCUMENTOS = Path("datos/documentos")
CARPETA_INDICE = Path("datos/vectores/chroma_db_sin_tacc")

DOCUMENTOS = [
    "DOC001.pdf",
    "DOC002.pdf",
    "DOC003.pdf"
]

MODELO_EMBEDDINGS = "bge-m3"
MODELO_GENERADOR = "granite4:latest"

NOMBRE_COLECCION = "documentos_sin_tacc_bge_m3"

K = 3


# 2. Cargar directamente los documentos PDF

def cargar_documentos():
    """Lee los PDF y conserva la identificación y página."""

    documentos = []

    for nombre_archivo in DOCUMENTOS:

        ruta_pdf = CARPETA_DOCUMENTOS / nombre_archivo

        if not ruta_pdf.exists():
            raise FileNotFoundError(
                f"No se encontró el documento: {ruta_pdf}"
            )

        cargador = PyPDFLoader(str(ruta_pdf))
        paginas = cargador.load()

        documento_id = ruta_pdf.stem

        for pagina in paginas:
            pagina.metadata["id"] = documento_id
            pagina.metadata["archivo"] = nombre_archivo

        documentos.extend(paginas)

        print(f"Documento cargado: {documento_id}")
        print(f"Páginas: {len(paginas)}")

    return documentos


# 3. Dividir los documentos

def dividir_documentos(documentos):
    """Divide los textos en fragmentos de 500 caracteres."""

    divisor = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    fragmentos = divisor.split_documents(documentos)

    return fragmentos


# 4. Construir el índice persistente

def construir_indice():
    """Reconstruye Chroma utilizando los tres documentos PDF."""

    documentos = cargar_documentos()

    fragmentos = dividir_documentos(documentos)

    embeddings = OllamaEmbeddings(
        model=MODELO_EMBEDDINGS
    )

    CARPETA_INDICE.mkdir(
        parents=True,
        exist_ok=True
    )

    indice_rag = Chroma(
        collection_name=NOMBRE_COLECCION,
        embedding_function=embeddings,
        persist_directory=str(CARPETA_INDICE)
    )

    # Eliminar la colección anterior para evitar duplicados
    if indice_rag.get(limit=1)["ids"]:

        indice_rag.delete_collection()

        indice_rag = Chroma(
            collection_name=NOMBRE_COLECCION,
            embedding_function=embeddings,
            persist_directory=str(CARPETA_INDICE)
        )

    identificadores = [
        f"fragmento_{numero}"
        for numero in range(len(fragmentos))
    ]

    indice_rag.add_documents(
        documents=fragmentos,
        ids=identificadores
    )

    print("\nÍNDICE RECONSTRUIDO CORRECTAMENTE")
    print("--------------------------------")
    print("Total de páginas:", len(documentos))
    print("Total de fragmentos:", len(fragmentos))
    print("Fragmentos indexados:", len(indice_rag.get()["ids"]))


# 5. Cargar el índice existente

def cargar_indice():
    """Abre la colección Chroma guardada en el disco."""

    embeddings = OllamaEmbeddings(
        model=MODELO_EMBEDDINGS
    )

    indice_rag = Chroma(
        collection_name=NOMBRE_COLECCION,
        embedding_function=embeddings,
        persist_directory=str(CARPETA_INDICE)
    )

    print("\nÍndice cargado correctamente.")
    print("Fragmentos disponibles:", len(indice_rag.get()["ids"]))

    return indice_rag


# 6. Crear cadena RAG

def crear_cadena_rag():
    """Conecta la plantilla, Granite 4 y el parser."""

    plantilla = ChatPromptTemplate.from_messages([
        (
            "system",
            "Respondé en español utilizando solamente la información "
            "del contexto. Citá [1], [2] o [3] junto a cada afirmación. "

            "No inventes datos ni completes frases que estén cortadas "
            "en los fragmentos recuperados. "

            "No conviertas una posibilidad en certeza, una recomendación "
            "en obligación ni una práctica preventiva en garantía de seguridad. "

            "No utilices las expresiones garantizar o asegurar la seguridad "
            "si el contexto no las respalda expresamente. "

            "Cuando existan recomendaciones relacionadas con la pregunta, "
            "presentalas en una lista clara. "

            "Si la pregunta se refiere a un restaurante específico, "
            "aclará que los documentos contienen recomendaciones generales "
            "pero no permiten verificar ese establecimiento. "

            "Si no existe información pertinente para responder, "
            "respondé exactamente: "
            "No encuentro esa información en los documentos."
        ),
        (
            "human",
            "Contexto:\n{contexto}\n\nPregunta: {pregunta}"
        )
    ])

    modelo = ChatOllama(
        model=MODELO_GENERADOR,
        temperature=0
    )

    cadena_rag = plantilla | modelo | StrOutputParser()

    return cadena_rag


# 7. Recuperar evidencia y generar respuestas

def consultar(pregunta_usuario: str) -> tuple[str, str]:
    """Devuelve la respuesta y los fragmentos utilizados como evidencia."""

    if not pregunta_usuario.strip():
        return (
            "Escribí una pregunta.",
            "Todavía no se consultaron fuentes."
        )

    hallazgos = indice_rag.similarity_search_with_score(
        query=pregunta_usuario,
        k=K
    )

    contexto = ""
    fuentes = ""

    for numero, hallazgo in enumerate(hallazgos, start=1):

        documento, distancia = hallazgo

        archivo = documento.metadata["archivo"]
        pagina = documento.metadata["page"] + 1

        referencia = f"{archivo}, página {pagina}"

        contexto += (
            f"[{numero}] {referencia}\n"
            f"{documento.page_content}\n\n"
        )

        fuentes += (
            f"**[{numero}] {referencia}** "
            f"(distancia {distancia:.3f})\n\n"
        )

        fuentes += (
            f"```text\n"
            f"{documento.page_content}\n"
            f"```\n\n"
        )

    respuesta = cadena_rag.invoke({
        "contexto": contexto,
        "pregunta": pregunta_usuario
    })

    return respuesta, fuentes


# 8. Ejecutar la aplicación

if __name__ == "__main__":

    # Reconstruir únicamente cuando se solicita expresamente
    if "--rebuild" in sys.argv:
        construir_indice()

    indice_rag = cargar_indice()

    cadena_rag = crear_cadena_rag()

    interfaz = gr.Interface(
        fn=consultar,

        inputs=gr.Textbox(
            label="Escribí tu consulta sobre cuidados celiaquía",
            placeholder="Ejemplo: ¿Cómo evitar la contaminación cruzada?",
            lines=2
        ),

        outputs=[
            gr.Textbox(
                label="Respuesta del asistente",
                lines=8
            ),

            gr.Markdown(
                label="Fragmentos recuperados y enviados al modelo"
            )
        ],

        title="Buscador de información LG Libre Gluten",

        description=(
            "Consultá los documentos sobre celiaquía y "
            "recomendaciones para elaborar menús libres de gluten. "
            "Las respuestas muestran las fuentes utilizadas. "
            "La información no certifica restaurantes ni "
            "garantiza la ausencia de contaminación cruzada."
        )
    )

    interfaz.launch()
