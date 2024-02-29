# Backend app

A backend base on fastAPI framework.

## Getting Started

1. ```python -m venv .venv``` (if it does not exist or is incompatible)
2. ```./.venv/Scripts/activate```
3. ```pip install -r .\requirements.txt```
4. *Up your database*
5. *Configure the .env file*
6. ```alembic upgrade head```
7. ```cd .\src\```
8. ```uvicorn main:app --reload``` OR ```py .\main.py```


### Up database in docker 
```bash
docker run --rm --name db-vuc -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:14.5
```


### Other

Url admin panel: /admin
Docs url: /api/openapi
