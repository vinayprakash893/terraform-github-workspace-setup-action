FROM python:3.10

WORKDIR /app


COPY poetry.lock pyproject.toml ./
RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install

COPY . ./
RUN chmod +x /app/entrypoint.py
ENTRYPOINT ["/app/entrypoint.py"]