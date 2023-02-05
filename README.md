# 맛스타그램

지도에서 나만의 맛집을 추가하고 관리하자!

### Environments

- OS: 
  - Mac on M1 (local)
  - Amazon Linux 2 AMI (production)
- Languages:
  - Python 3.10
  - Javascript
- Libraries
  - FastAPI 0.85.1
  - Uvicorn 0.19.0
  - JQuery 3.6.1
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

# 2. Test

테스트시 local 환경에 별도 DB를 기준으로 진행하도록 하였습니다. docker 환경으로 postgreSQL을 실행합니다.

```bash
(.venv) $> docker-compose -f ./tests/docker-compose.test.yml up -d
Pulling postgres (postgres:12.7)...
```

테스트 실행

```bash
(.venv) $> pytest
```

# 3. Demo 

## 3.1 메인 진입 화면

<img width="720" alt="matstagram_main" src="https://user-images.githubusercontent.com/37063580/216816926-0cc398ad-d0ce-43ce-85e2-d48660070977.png">

## 3.2 회원 가입
<img width="720" alt="matstagram_register" src="https://user-images.githubusercontent.com/37063580/216817099-74a509ef-856e-4214-88c7-579503bfbe3e.png">

## 3.3 맛집 화면

### 3.3.1 내가 등록한 맛집 표시

<img width="720" alt="matstagram_map" src="https://user-images.githubusercontent.com/37063580/216816934-b18e5bfc-c16b-4d24-ab12-18124a7cd070.png">

### 3.3.2 특정 장소 클릭시

<img width="720" alt="matstagram_map_click" src="https://user-images.githubusercontent.com/37063580/216816945-70fa3796-f310-41c2-b75e-70c162a295cf.png">

### 3.3.3 원하는 태그로 필터링

<img width="720" alt="matstagram_filter" src="https://user-images.githubusercontent.com/37063580/216817188-5235dc73-500f-4550-aa8d-bd8cb625ed19.png">

## 3.4 내가 등록한 맛집 리스팅

<img width="720" alt="matstagram_list" src="https://user-images.githubusercontent.com/37063580/216816960-f1540f60-8fa9-4b12-ba10-0e8730737128.png">

## 3.5 내 정보

### 3.5.1 프로필 화면

<img width="720" alt="matstagram_profile" src="https://user-images.githubusercontent.com/37063580/216816965-dff8326d-5871-4567-b629-c469966336fe.png">

### 3.5.2 프로필 수정

<img width="720" alt="matstagram_profile_update" src="https://user-images.githubusercontent.com/37063580/216816970-b2701f27-ba76-49e7-ba87-6ad15df475d3.png">

## 3.6 API 문서 화면

<img width="720" alt="matstagram_documents" src="https://user-images.githubusercontent.com/37063580/216816981-1d4742c9-78f5-4435-8697-4f213655cfde.png">
