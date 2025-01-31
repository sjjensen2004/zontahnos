FROM python:3.10

WORKDIR /app
COPY ./app/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app/app ./app
WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker"]