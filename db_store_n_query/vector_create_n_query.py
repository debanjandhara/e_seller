from dotenv import load_dotenv

from website_scraping.scrape_n_store import read_file_to_string

from website_scraping.sitemap_handling import filename_filtered

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

# def read_file_to_string(file_path):
#     try:
#         # Initialize an empty string to store the file contents
#         file_contents = ""

#         # Open the file and read its contents
#         with open(file_path, 'r', encoding='utf-8') as file:
#             file_contents = file.read()

#         return file_contents
#     except FileNotFoundError:
#         return "File not found."


def main():

    content = read_file_to_string(filename_filtered)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text=content)

    vector_name = filename_filtered
    
    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    with open(f"{vector_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)



def query_from_vector(query, vector_name):

    if os.path.exists(f"{vector_name}.pkl"):
        with open(f"{vector_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
        


    query = "what colour is the sky"

    docs = VectorStore.similarity_search(query=query, k=3)

    llm = OpenAI()
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        print(cb)
    print("\n\nResponse : ",response)
