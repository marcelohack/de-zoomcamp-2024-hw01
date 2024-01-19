FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app
COPY ../src/ /app/
ENTRYPOINT ["python"]
