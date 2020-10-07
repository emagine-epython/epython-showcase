# FROM python:3.8-alpine
FROM mcr.microsoft.com/playwright

RUN apt-get update \
  && apt install software-properties-common -y \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt install -y python3-pip python3-dev -y \
  && apt install python3.8 -y \
  && python3.8 -m pip install --upgrade pip \
  && python3.8 -m pip install \
  playwright \
  boto3 \
  && python3.8 -m playwright install

COPY snap_yahoo_eq.py .
    
CMD ["python3.8", "snap_yahoo_eq.py"]