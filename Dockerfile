FROM python:3.10

WORKDIR /app
ARG REQUIREMENTS=requirements.txt

COPY requirements requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./zontahnos/app/app ./app
WORKDIR /app/app
ENV PYTHONPATH=/app

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker"]doc