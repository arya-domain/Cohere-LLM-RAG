import os
import pinecone
import gradio as gr
import time
import logging
from langchain.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    UnstructuredExcelLoader,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain.vectorstores import Pinecone
from langchain_core.messages import HumanMessage, SystemMessage


def setup_logger(log_file: str, level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)
        console_handler.setLevel(level)
        file_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger("app.log")


class TextAnalysisPipeline:
    def __init__(self):
        try:
            self.cohere_api_key = "2VWYeENqn45Ktw3o8V5lFX7eBqOy6CkB3Lgo6nmf"
            self.pinecone_api_key = "3ccb7171-c728-4334-aeae-c4bdc25c171a"
            self.pinecone_environment = "gcp-starter"
            self.index_name = "cohere"

            os.environ["COHERE_API_KEY"] = self.cohere_api_key
            pinecone.init(
                api_key=self.pinecone_api_key, environment=self.pinecone_environment
            )

            self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
            self.llm = ChatCohere()

            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.index_name, metric="cosine", dimension=1024
                )

            self.vectorstore = None
            self.current_file = None

            self.initial_prompt = """You are an AI assistant specialized in analyzing and answering questions based on the content of various text-based files, including PDFs, CSVs, Excel sheets, and plain text documents. Your task is to provide accurate, concise, and relevant answers to user queries using the information from the retrieved document sections. Follow these guidelines:

1. Base your answers solely on the information provided in the retrieved documents.
2. If the answer is not directly found in the documents, say so clearly.
3. Provide concise answers, but include relevant details when necessary.
4. If asked about topics not covered in the documents, politely explain that you can only answer questions related to the uploaded file.
5. Use a professional and helpful tone in your responses.
6. For data files (CSV, Excel), be prepared to provide basic statistical insights if asked.

Remember, your goal is to assist users in understanding the content of the file they've uploaded."""

            logger.info("TextAnalysisPipeline initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing TextAnalysisPipeline: {str(e)}")
            raise

    def reset_pipeline(self):
        try:
            index = pinecone.Index(self.index_name)
            index.delete(delete_all=True)
            self.vectorstore = None
            self.current_file = None
            logger.info(
                "Pipeline reset: Deleted all vectors from Pinecone and reset current file"
            )
        except Exception as e:
            logger.error(f"Error resetting pipeline: {str(e)}")
            raise

    def process_file(self, file_path):
        try:
            if file_path != self.current_file:
                logger.info(f"New file detected. Resetting pipeline.")
                self.reset_pipeline()
                self.current_file = file_path
            else:
                return

            logger.info(f"Processing file: {file_path}")

            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".csv":
                loader = CSVLoader(file_path)
            elif file_extension in [".xlsx", ".xls"]:
                loader = UnstructuredExcelLoader(file_path)
            elif file_extension in [".txt", ".md", ".json"]:
                loader = TextLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")

            documents = loader.load()

            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(documents)

            batch_size = 100
            for i in range(0, len(docs), batch_size):
                batch = docs[i : i + batch_size]
                if self.vectorstore is None:
                    self.vectorstore = Pinecone.from_documents(
                        batch, self.embeddings, index_name=self.index_name
                    )
                else:
                    time.sleep(60)
                    self.vectorstore.add_documents(batch)
                logger.info(
                    f"Processed batch {i//batch_size + 1} of {len(docs)//batch_size + 1}"
                )

            logger.info("File processed and vectors stored in Pinecone")
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise

    def query(self, query):
        try:
            if not self.vectorstore:
                logger.warning("Query attempted without processed file")
                return "Please upload a file first.", ""

            logger.info(f"Querying: {query}")
            retriever = self.vectorstore.as_retriever()
            retrieved_documents = retriever.invoke(query)

            messages = [
                SystemMessage(content=self.initial_prompt),
                HumanMessage(content=query),
            ]
            response = self.llm.invoke(messages, documents=retrieved_documents)

            retrieved_text = (
                retrieved_documents[0].page_content
                if retrieved_documents
                else "No relevant documents found."
            )

            logger.info("Query processed successfully")
            return response.content, retrieved_text
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise


# Initialize the pipeline
try:
    pipeline = TextAnalysisPipeline()
except Exception as e:
    logger.error(f"Failed to initialize pipeline: {str(e)}")
    raise


def save_uploaded_file(file):
    try:
        if file is None:
            logger.warning("No file uploaded")
            return None
        file_path = f"{file.name}"
        if hasattr(file, "read"):
            with open(file_path, "wb") as f:
                f.write(file.read())
        else:
            logger.info(f"File appears to be already saved at: {file}")
            return file
        logger.info(f"File saved successfully: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error handling uploaded file: {str(e)}")
        raise


def process_and_query(file, query):
    try:
        if file is None:
            logger.warning("Query attempted without file upload")
            return "Please upload a file first.", ""

        file_path = save_uploaded_file(file)
        if file_path is None:
            logger.error("Failed to handle uploaded file")
            return "Error handling the uploaded file.", ""

        pipeline.process_file(file_path)
        return pipeline.query(query)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        return error_message, ""


iface = gr.Interface(
    fn=process_and_query,
    inputs=[
        gr.File(
            label="Upload File",
            file_types=[".pdf", ".csv", ".xlsx", ".xls", ".txt", ".md", ".json"],
        ),
        gr.Textbox(label="Enter your question"),
    ],
    outputs=[
        gr.Textbox(label="LLM Response"),
        gr.Textbox(label="Retrieved Document Text"),
    ],
    title="Text Analysis System",
    description="Upload a file (PDF, CSV, Excel, TXT, MD, or JSON) and ask questions about its content. The system will automatically reset when a new file is uploaded.",
)

iface.launch(max_file_size="10mb", debug=True)
