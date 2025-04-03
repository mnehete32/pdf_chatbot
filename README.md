# PDF Chatbot

A chatbot that allows users to interact with PDF documents using natural language queries. It leverages **LangChain**, **Llama**, and **Pinecone** for document retrieval and response generation. **Gradio** is used for the frontend interface, and **FastAPI** is used for the backend with **Llama** as the language model.

## Features
- Upload PDF files and interact with them using natural language.
- Utilizes **LangChain** for efficient document parsing and query processing.
- Uses **Llama** as the language model for generating responses.
- Stores and retrieves document embeddings using **Pinecone**.
- Provides a web-based interface powered by **Gradio**.
- Backend built using **FastAPI** to serve requests efficiently.
- Deployed using Kubernetes for scalability.

## Technologies Used

### Frontend
- **Gradio** - Provides a user-friendly web-based interface.

### Backend
- **FastAPI** - Handles API requests and serves the chatbot.
- **Llama** - Generates responses for user queries.
- **LangChain** - Facilitates document parsing and query processing.
- **Pinecone** - Manages and retrieves document embeddings.
- **Kubernetes** - Orchestrates deployment and scaling.

## Prerequisites
Ensure you have the required API keys and credentials before running the chatbot. Add your secrets in the file [kube/secrets-env.yaml](kube/secrets-env.yaml) with the following format:

```yaml
PINECONE_API_KEY= <your pinecone api key>
PINECONE_API_ENV= <region of pinecone>
INDEX_NAME= <name of index in pinecone>
HUGGINGFACEHUB_API_TOKEN= <hugging face api key>
```

## Installation & Deployment
To set up and deploy the chatbot, follow these steps:

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd pdf_chatbot
   ```

2. Run the setup script to create docker images:
   ```sh
   sh bash.sh
   ```

3. Deploy the application using Kubernetes:
   ```sh
   kubectl apply -k kube/
   ```

## Persistent Storage
The chatbot uses a **Persistent Volume** to store uploaded PDF files, ensuring accessibility across different pods. The configurations are defined in:
- [Persistent Volume](kube/peresistent-volume.yaml)
- [Persistent Volume Claim](kube/pvc.yaml)

## Accessing the Frontend
The frontend service is exposed using **NodePort**, making it accessible at:
```
http://0.0.0.0:<service-node-port>/
```
Replace `<service-node-port>` with the actual NodePort value assigned in the Kubernetes service configuration.