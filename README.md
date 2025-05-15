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
2. Ensure your module defines a `router` object (instance of FastAPI's `APIRouter`)
3. That's it! Your router will be automatically registered with the application

Example:
```python
# app/api/endpoints/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
async def get_users():
    return {"users": []}
```

No need to manually include your router in `api.py` - it will be discovered and registered automatically.

### How it works

The template implements an auto-discovery system:
1. `app/api/endpoints/__init__.py` scans all Python files in the endpoints directory
2. It collects any module that defines a `router` object
3. `app/api/api.py` registers all discovered routers with the application

This makes it easy to add new API functionality without modifying existing code. 