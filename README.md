# FastAPI Template API

A minimal and extensible FastAPI template designed for easy extension and automation.

## Structure

```
template-api/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── health.py
│   │   ├── __init__.py
│   │   └── api.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── services/
│   │   └── __init__.py
│   ├── workflows/
│   │   └── .gitkeep
│   └── __init__.py
├── tests/
├── .env
├── Dockerfile
├── docker-compose.yml
├── main.py
└── requirements.txt
```

## Getting Started

### Running Locally

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

### Using Docker

1. Build and start the container:
   ```
   docker-compose up -d
   ```

2. Stop the container:
   ```
   docker-compose down
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Extension Guide

To add new endpoints:

1. Create new modules in `app/api/endpoints/`
2. Include router in `app/api/api.py`

Example:
```python
# app/api/endpoints/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
async def get_users():
    return {"users": []}
```

Then include in api.py:
```python
from app.api.endpoints import users
app.include_router(users.router, prefix=settings.API_V1_STR)
``` 