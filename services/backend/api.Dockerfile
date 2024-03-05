# syntax=docker/dockerfile:1.2

FROM python:3.11

WORKDIR /code

ENV KMP_DUPLICATE_LIB_OK=TRUE

COPY requirements.txt /code/requirements.txt
COPY .dockerignore /code/.dockerignore
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src /code/src
COPY data /code/data
COPY pyproject.toml /code/pyproject.toml

RUN pip install /code/

CMD ["uvicorn", "src.ppl.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
