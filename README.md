### Starting:
1. Install dependencies from `requirements.txt`
```shell
pip install -r requirements.txt
```
2. Create relation with the database
```shell
alembic init alembic
```
Next you need setup URI to the database in `alembic.ini`
```
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/social_network
```
 and set metadata in `alembic/env.py`
```
from app.db.database import Base
from app.db.models import Profile, Post, Like

target_metadata = Base.metadata
```
Next make migrations:
```shell
alembic revision --autogenerate
```
And do a migrations:
```shell
alembic upgrade head
```
3. Setting up enviroment,
rename file `.env.simple` to `.env` and fill variables with values.
4. Start with uvicorn
```shell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Swagger UI : ```http://127.0.0.1:8000/docs```

Swagger specification is in `docs/`