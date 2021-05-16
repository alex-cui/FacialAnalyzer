FROM python:3.7
  
RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python3", "main.py"]