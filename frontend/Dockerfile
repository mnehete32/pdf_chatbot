FROM python:3.10.12

WORKDIR /qa_bot/frontend

COPY ./frontend/ /qa_bot/frontend/

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "gradio_app.py" ]
EXPOSE 7860
