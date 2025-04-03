FROM nvcr.io/nvidia/pytorch:23.09-py3

RUN CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install --force-reinstall llama-cpp-python==0.3.8 --no-cache-dir
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.2/compat/lib.real/



WORKDIR /qa_bot
COPY ./backend/ /qa_bot
RUN pip install -r requirements.txt


ENTRYPOINT [ "python", "fastapi_app.py" ]
EXPOSE 8000
