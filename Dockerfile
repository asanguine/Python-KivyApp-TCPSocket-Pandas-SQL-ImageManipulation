FROM python:3.10.12

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
        python3-dev \
        libffi-dev \
        libssl-dev \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libportmidi-dev \
        libswscale-dev \
        libavformat-dev \
        libavcodec-dev \
        zlib1g-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python3", "main.py"]
