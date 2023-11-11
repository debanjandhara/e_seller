from dotenv import load_dotenv
import os
import openai

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


def create_vector(content, vector_name):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text=content)
    
    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    
    # os.makedirs(os.path.dirname(f"{vector_name}.pkl"), exist_ok=True)
    
    with open(f"{vector_name}.pkl", "wb") as f:
        print("Dumping in ",f"{vector_name}.pkl")
        pickle.dump(VectorStore, f)

    return vector_name




def query_from_vector(query, vector_name):

    if os.path.exists(f"{vector_name}.pkl"):
        with open(f"{vector_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)

    # query = "what colour is the sky"

    docs = VectorStore.similarity_search(query=query, k=3)

    llm = OpenAI()
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        print(cb)
    # print("\n\nResponse : ",response)
    return response


# folder = "data/uuid1234/"

# folder2 = "data/uuid1234/vectors/"



# # filename = "data/uuid1234/apple.com.filtered.json"

# # vector_name = create_vector(filename)

# # print(vector_name)

# vector_name = "data/uuid1234/apple.com.filtered.json"

# query_from_vector("What is the price of iphone ?", vector_name)

# # print(read_file_to_string(filename))