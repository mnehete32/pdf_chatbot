from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.llms import LlamaCpp
from huggingface_hub import hf_hub_download
from sentence_transformers import SentenceTransformer
from langchain.chains.question_answering import load_qa_chain

# Load Embeddings Model
embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2', device="cuda")

# Load Best Llama Model
model_name_or_path = "TheBloke/Llama-2-7B-Chat-GGUF"
model_basename = "llama-2-7b-chat.Q4_0.gguf"
model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

llm = LlamaCpp(
    model_path=model_path,
    max_tokens=256,
    n_gpu_layers=-1,
    n_batch=256,
    n_ctx=1024,
    verbose=False
)

def process_pdf(pdf_path, namespace, pinecone_index):
    loader = PyPDFLoader(pdf_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)
    
    vectors = [
        (str(i), embeddings_model.encode(t.page_content).tolist(), {"text": t.page_content})
        for i, t in enumerate(docs)
    ]
    
    pinecone_index.upsert(vectors, namespace=namespace)

def ask_question(query, session_id, pinecone_index):
    namespace = f"user_{session_id}"
    query_embedding = embeddings_model.encode(query).tolist()
    results = pinecone_index.query(vector=query_embedding, top_k=5, include_metadata=True, namespace=namespace)
    retrieved_docs = [match["metadata"]["text"] for match in results["matches"]]
    retrieved_docs = [Document(page_content=text) for text in retrieved_docs]
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=retrieved_docs, question=query)
    return response
