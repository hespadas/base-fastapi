FROM python:3.12
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . /app
RUN pip install poetry \
    && poetry install

EXPOSE 8000
CMD poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
