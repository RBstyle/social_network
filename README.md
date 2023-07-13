### Starting:
### 1. Create virtual environment and install dependencies from `requirements.txt`
```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### 2. Create database
```shell
$ sudo -u postgres psql -c 'CREATE DATABASE social_network;'
```

### 3. Create relation with the database
```shell
$ alembic init alembic
```

### 4. Setup URI to the database in `alembic.ini`
for example:
```
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/social_network
```
### 5. Set metadata in `alembic/env.py`
```python
from app.db.database import Base
from app.db.models import Profile, Post, Like

target_metadata = Base.metadata
```
### 6. Make migrations:
```shell
$ alembic revision --autogenerate
$ alembic upgrade head
```

### 7. Rename file `.env.simple` to `.env` and fill variables with values.

### 8. Start with uvicorn
```shell
$ uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Signup form: `http://127.0.0.1:8000/auth/signup`

Login form: `http://127.0.0.1:8000/auth/login`

Swagger UI : `http://127.0.0.1:8000/docs`

Swagger specification is in `docs/`