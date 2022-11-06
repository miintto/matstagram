# 맛스타그램

지도에서 나만의 맛집을 추가하고 관리하자!

[[바로가기]](http://matstagram.miintto.com)

### Environments
- OS: 
  - Mac on M1 (local)
  - Amazon Linux 2 AMI (production)
- Language:
  - Python 3.10
- Frameworks:
  - FastAPI 0.85.1
  - Uvicorn 0.19.0
- Database:
  - PostgreSQL 12.7


# 1. Quick Start

## 1.1 Set Environment Variables

```bash
$> cp .env.example .env.local
$> vim .env.local

# == Dot Env Files == #

# - FASTAPI SECRET
APP_ENV=local
...
```

## 1.2 Install Libraries

```bash
$> virtualenv -p python3.10 .venv
$> source .venv/bin/activate
(.venv) $> poetry install
```


## 1.3 Run Uvicorn Server

```bash
(.venv) $> uvicorn app.main:app
APP_ENV:  local
INFO:     Started server process [45145]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 1.4 Run Server Using Docker

```bash
(.venv) $> docker-compose --env-file .env.local up -d
```

## 1.5 Run Test
```bash
(.venv) $> docker-compose -f ./tests/docker-compose.test.yml up -d
Pulling postgres (postgres:12.7)...

(.venv) $> python ./tests/run.py
```
