###############################################################################
#  BUILD IMAGE                                                                #
###############################################################################
FROM python:3.10-slim AS build

RUN apt-get -y update \
    && apt-get install -y \
    libpq-dev \
    gcc \
    && pip install poetry

COPY poetry.lock pyproject.toml /usr/src/

WORKDIR /usr/src

RUN virtualenv -p python3.10 venv \
    && PATH="/usr/src/venv/bin:$PATH" \
    VIRTUAL_ENV="/usr/src/venv" \
    poetry install --only main


###############################################################################
#  RUNTIME IMAGE                                                              #
###############################################################################
FROM python:3.10-slim

ENV PATH="/usr/src/venv/bin:$PATH"

EXPOSE 8000

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/src/venv /usr/src/venv

COPY ./app /usr/src/app

WORKDIR /usr/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
