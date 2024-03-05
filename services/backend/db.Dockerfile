# syntax=docker/dockerfile:1.2

FROM python:3.11

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY .dockerignore /code/.dockerignore
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src /code/src
COPY pyproject.toml /code/pyproject.toml

RUN pip install /code/

CMD ["python", "-m", "ppl.utils.pubmed"]
