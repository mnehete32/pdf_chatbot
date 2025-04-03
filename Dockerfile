FROM nvcr.io/nvidia/pytorch:23.09-py3

WORKDIR /qa_bot

COPY . /qa_bot

RUN pip install -r requirements.txt

RUN CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install --force-reinstall llama-cpp-python==0.3.8 --no-cache-dir
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.2/compat/lib.real/

# Had to install numpy becasue llama-cpp-python install 2.2.4 version of numpy
# which is not compatible with gradio
RUN pip install numpy==1.24.4
ENTRYPOINT [ "python", "app.py" ]
EXPOSE 7860
