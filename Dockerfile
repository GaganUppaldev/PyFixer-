FROM python:3.14

WORKDIR /app

RUN pip install --no-cache-dir pytest

COPY codebase/ /app/

CMD ["pytest", "-v"]

