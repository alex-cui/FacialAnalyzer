FROM ubuntu:18.04
  
RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN apt-get update ##[edited]
RUN apt install python3-pip -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "main.py"]