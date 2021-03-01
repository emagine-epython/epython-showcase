FROM python:3

RUN pip install --upgrade pip \
    && pip install \
    kydb \
    s3fs \
    fsspec \
    dash \
    pandas \
    gunicorn

EXPOSE 8080

ADD tsdb /tsdb
ADD dash_demo /dash_demo
COPY app.py /

CMD ["gunicorn", "--workers", "2", "app:server"]
