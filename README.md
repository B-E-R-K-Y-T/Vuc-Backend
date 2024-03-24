# Backend app

A backend base on fastAPI framework.

## Requirements

Python 3.12

## Getting Started

1. ```python -m venv .venv``` (if it does not exist or is incompatible)
2. ```./.venv/Scripts/activate```
3. ```pip install -r .\requirements.txt```
4. *Up your database*
5. *Configure the .env file*
6. ```alembic upgrade head```
7. ```cd .\src\```
8. ```uvicorn main:app --host 127.0.0.1 --port 8080 --reload``` OR ```py .\main.py```

--- OR ---

1. *Configure the .env file*
2. ```docker-compose up```



### Up database in docker 
```bash
docker run --rm --name db-vuc -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=name_db -d postgres:15
```


### Other

* Admin panel URL: /admin
* Swagger URL: /api/openapi
* ReDoc URL: /redoc
* OpenAPI JSON URL: /api/openapi.json 
* Flower URL: host:8888/
