FROM python:3.14-slim AS base

# Dépendances WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./backend /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS dev

RUN echo 'DEV'

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS prod

RUN echo 'PROD'

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]