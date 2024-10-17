import streamlit as st
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from langchain_community.llms import OpenAI 
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # Nueva importación
from langchain_community.vectorstores import Chroma
import os
# Configura la API Key de OpenAI directamente en el código
OPENAI_API_KEY = ""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Título de la aplicación
st.title("Asistente de PDF con LLM")

# Entrada de texto para pegar el enlace del PDF
pdf_url = st.text_input("Pega el enlace del PDF aquí:")

# Botón para procesar el PDF y mostrar el contenido
if st.button("Procesar PDF"):
    if pdf_url:
        try:
            # Descargar el PDF desde la URL
            response = requests.get(pdf_url)
            response.raise_for_status()  # Verificar si hay errores en la solicitud
            
            # Leer el contenido del PDF
            pdf_content = BytesIO(response.content)
            reader = PdfReader(pdf_content)
            
            # Extraer texto de todas las páginas
            text_content = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            
            # Verificar si se extrajo texto
            if text_content.strip():
                st.success("El contenido del PDF ha sido procesado correctamente. Ahora puedes hacer preguntas.")
                
                # División del texto para el procesamiento por LangChain
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text_content)
                
                # Crear un index vectorial para preguntas-respuestas
                embeddings = OpenAIEmbeddings()
                docsearch = Chroma.from_texts(chunks, embeddings)
                
                # Cadena de preguntas y respuestas
                qa_chain = load_qa_chain(OpenAI(), chain_type="stuff")

                # Interfaz para realizar preguntas
                st.subheader("Pregúntale algo sobre el PDF")
                user_question = st.text_input("Escribe tu pregunta aquí:")

                if user_question and st.button("Responder"):
                    try:
                        # Buscar la respuesta en los datos del PDF
                        relevant_chunks = docsearch.similarity_search(user_question)
                        answer = qa_chain.run(input_documents=relevant_chunks, question=user_question)
                        st.write(f"Respuesta: {answer}")
                    except Exception as e:
                        st.error(f"Error al generar la respuesta: {e}")
            else:
                st.warning("No se pudo extraer texto del PDF. Puede que el PDF no contenga texto reconocible o esté protegido.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error al descargar el PDF: {e}")
        except Exception as e:
            st.error(f"Error al leer el PDF: {e}")
    else:
        st.warning("Por favor, pega un enlace de un PDF válido.")
