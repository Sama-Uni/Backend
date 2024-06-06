FROM python:3.9.19-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /apps/backend
RUN pip install Django
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY . .
EXPOSE 8000