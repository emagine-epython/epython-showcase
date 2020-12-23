FROM tensorflow/tensorflow 

RUN pip install --upgrade pip \
    && pip install \
    https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp36-cp36m-linux_x86_64.whl \
    kydb \
    fastapi \
    uvicorn

EXPOSE 8080

COPY main.py /root/main.py

CMD ["uvicorn", "root.main:app", "--host", "0.0.0.0", "--port", "8080"]
