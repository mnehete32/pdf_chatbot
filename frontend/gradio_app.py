import gradio as gr
import requests
import uuid
import os
# Backend URL
BACKEND_URL = os.environ.get("BACKEND_BASE_URL")

def ensure_session_id(session_id):
    """Generates a session ID if it's not present in gr.State()."""
    return session_id if session_id else str(uuid.uuid4())

def upload_pdf(pdf, session_id):
    """Uploads a PDF and sets the session ID."""
    session_id = ensure_session_id(session_id)  # Ensure session_id is set

    # files = {'file_location': pdf.name}'
    print(pdf)
    response = requests.post(f"{BACKEND_URL}/upload/", headers = {"Content-Type": "application/json"},json={ "file_path": pdf, "session_id": session_id})

    if response.status_code == 200:
        return f"PDF uploaded successfully! Session ID: {session_id}", session_id
    else:
        return "Failed to upload PDF.", session_id

def query_pdf(query, session_id):
    """Sends a query to the backend using the stored session ID."""
    session_id = ensure_session_id(session_id)  # Ensure session_id is set

    if session_id is None:
        return "Please upload a PDF first."

    data = {"session_id": session_id, "query": query}
    response = requests.post(f"{BACKEND_URL}/query/", data=data)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Failed to process query."

# Define Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# 📄 Multi-User PDF Chatbot with FastAPI Backend")
    
    session_id_state = gr.State()  # Store session_id per user

    with gr.Row():
        upload_button = gr.File(label="Upload PDF",)
        upload_status = gr.Textbox(label="Upload Status", interactive=False)
    
    query_input = gr.Textbox(label="Enter your query")
    query_button = gr.Button("Ask Question")
    response_output = gr.Textbox(label="Response", interactive=False)

    # Link actions to functions
    upload_button.change(upload_pdf, inputs=[upload_button, session_id_state], outputs=[upload_status, session_id_state])
    query_button.click(query_pdf, inputs=[query_input, session_id_state], outputs=response_output)

# Run Gradio app
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0")
