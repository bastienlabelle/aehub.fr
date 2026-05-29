FROM python:3.14-slim AS base

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