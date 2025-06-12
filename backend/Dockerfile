FROM python:3.12

WORKDIR /app

COPY . /app
RUN pip install poetry \
    && poetry install

EXPOSE 8000
CMD ["poetry", "run", "python", "app/main.py"]
