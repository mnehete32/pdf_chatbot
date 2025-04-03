import os
import gradio as gr
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Pinecone as PC
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from pinecone import Pinecone, ServerlessSpec
from langchain.llms import LlamaCpp
from huggingface_hub import hf_hub_download

# Environment Variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")
index_name = os.environ.get("INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(
        api_key= PINECONE_API_KEY, 
        index_name = index_name

    )

embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')  

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    index = pc.Index(index_name)

    vectors = [
        (str(i), embeddings_model.encode(t.page_content).tolist(), {"text": t.page_content})
        for i, t in enumerate(docs)
        ]    
    index.upsert(vectors)
    return index

# Load Best Llama Model
model_name_or_path = "TheBloke/Llama-2-7B-Chat-GGUF"
model_basename = "llama-2-7b-chat.Q2_K.gguf"
model_path = hf_hub_download(repo_id=model_name_or_path, filename= model_basename)
# Load Llama model
llm = LlamaCpp(
    model_path=model_path,
    max_tokens=256,
    n_gpu_layers=-1,  # Automatically uses all available GPU layers
    n_batch=256,  
    n_ctx=1024,  
    verbose=False  
)

def ask_question(pdf_path, query):

    docs = process_pdf(pdf_path)

    # Generate query embedding
    query_embedding = embeddings_model.encode(query).tolist()

    # Perform similarity search
    results = docs.query(vector=query_embedding, top_k=5, include_metadata=True)

    # Extract matching documents
    retrieved_docs = [match["metadata"]["text"] for match in results["matches"]]

    # Load QA chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Run QA chain with retrieved documents
    retrieved_docs = [Document(page_content=text) for text in retrieved_docs]

    response = chain.run(input_documents=retrieved_docs, question=query)
    return response

iface = gr.Interface(
    fn=ask_question,
    inputs=[gr.File(label="Upload PDF"), gr.Textbox(label="Enter your query")],
    outputs="text",
    title="Llama 2 + Pinecone QA System",
    description="Upload a PDF and ask questions about its content using Llama 3 and Pinecone."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
