# ------------

from dotenv import load_dotenv
import os
import openai

# -------------

import magic
import docx
import json
import PyPDF2

# -------------

# import os
import os.path as osp
# import pickle
import pandas as pd

# -------------

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import openai

def read_file_to_string(file_path):
    try:
        # Initialize an empty string to store the file contents
        file_contents = ""

        # Open the file and read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        return file_contents
    except FileNotFoundError:
        return "File not found."


def create_vector(content, vector_folder_name):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text=content)
    
    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    
    # os.makedirs(os.path.dirname(f"{vector_name}.pkl"), exist_ok=True)
    
    # directory = os.path.dirname(vector_name)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
        
    VectorStore.save_local(vector_folder_name)
    
    # with open(f"{vector_name}.pkl", "wb") as f:
    #     print("Dumping in ",f"{vector_name}.pkl")
    #     pickle.dump(VectorStore, f)

    return vector_folder_name




def query_from_vector(query, vector_folder_name):

    # if os.path.exists(f"{vector_name}.pkl"):
    #     with open(f"{vector_name}.pkl", "rb") as f:
    #         VectorStore = pickle.load(f)
    
    embeddings = OpenAIEmbeddings()    
    VectorStore = FAISS.load_local(vector_folder_name, embeddings=embeddings)


    # query = "what colour is the sky"

    docs = VectorStore.similarity_search(query=query, k=3)

    llm = OpenAI()
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        print(cb)
    print("\n\nResponse : ",response)
    return response


def read_document(file_path):
    # Use magic to determine the file type
    mime = magic.Magic()
    file_type = mime.from_file(file_path)
    
    content = ''

    # Read content based on the file type
    if file_type.startswith('Microsoft Word'):
        # # For .docx files
        # doc = docx.Document(file_path)
        # content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        if file_path.endswith('.docx'):
            # For .docx files
            doc = docx.Document(file_path)
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_type.startswith('JSON'):
        # For .json files
        with open(file_path, 'r') as json_file:
            content = json.load(json_file)
    elif file_type.startswith('ASCII'):
        # For plain text (.txt) files
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
    elif file_type.startswith('PDF'):
        pdfFileObj = open(file_path, 'rb')
 
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
 
        # printing number of pages in pdf file
        # print(len(pdfReader.pages))

        # creating a page object
        pageObj = pdfReader.pages[0]

        # extracting text from page
        content = pageObj.extract_text()

        # closing the pdf file object
        pdfFileObj.close()

    return content

def merge_db(vector_base_folder, final_folder):

# Example usage:
# directory_path = r'data/uuid2502/uploads'
# output_file = r'data/uuid2502/merged.pkl'
# combine_pickle_files(directory_path, output_file)

# print(query_from_vector("give me a summary about networking", r"data/uuid2502/merged"))

vector_base_folder = "data/uuid2502/vectors"

filename = "test"

vector_folder_name = f"{vector_base_folder}/{filename}"

# print(create_vector(read_document(r"data/uuid2502/uploads/sample.txt"), vector_folder_name))
# print(query_from_vector("give me summary about operating system", vector_folder_name))