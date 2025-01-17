from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"]=os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

from langchain.document_loaders import PyPDFLoader, JSONLoader
import json
from pathlib import Path
from pprint import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter,RecursiveJsonSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Load the PDF file
# pdf_path = "rag/documents/ELBANI_CV_LAST.pdf"  
json_path = "rag/documents/cv_wail.json"  

# loading the jsondata
json_data = json.loads(Path(json_path).read_text())

# recursive splitter
splitter = RecursiveJsonSplitter(max_chunk_size=1)

# chunks
docs = splitter.create_documents(texts=[json_data])


# Add to vectorDB
vectorstore = Chroma.from_documents(
    documents=docs,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever(

)



################################# testing scripts ######################################

# Example usage: Retrieve documents related to a query
# docs = retriever.invoke("list the project in which wail worked on ?")

# for i, chunk in enumerate(docs):
#     print(f"docs {i+1}:\n{chunk.page_content}\n{'-'*50}\n")

