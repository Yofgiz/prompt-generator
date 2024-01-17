from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil
from PyPDF2 import PdfReader

DATA_PATH = "./data"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)


def load_documents():
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_PATH, filename)
            with open(filepath, "rb") as file:
                pdf_reader = PdfReader(file)
                num_pages = len(PdfReader.pages)
                document = ""
                for page_number in range(num_pages):
                    page = pdf_reader.getPage(page_number)
                    text = page.extractText()
                    document += text
                documents.append(document)
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks

if __name__ == "__main__":
    main()