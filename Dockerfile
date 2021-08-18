FROM python:3.8
LABEL maintainer "GiowGiow"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r ./requirements.txt

COPY ./ ./

EXPOSE 80

CMD ["gunicorn", "app:server", "-b", ":80"]

