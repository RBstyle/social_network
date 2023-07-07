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
 and set metadata in `alembic/env.py`\
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


# Simple RESTful API using FastAPI for a social networking application
---
### **Functional requirements:**
- There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
- As a user I need to be able to signup and login
- As a user I need to be able to create, edit, delete and view posts
- As a user I can like or dislike other users’ posts but not my own 
- The API needs a UI Documentation (Swagger/ReDoc)

### **Bonus section (not required):**
- Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
- Use emailhunter.co for verifying email existence on registration
- Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) 

## **Technology Requirements**
### **Tasks should be completed:**
- Using FastAPI 0.50.0+
- With any DBMS (Sqlite, PostgreSQL, MySQL)
- Uploaded to GitHub

## **Requirements**
When implementing your solution, please make sure that the code is:
- Well-structured
- Contains instructions (best to be put into readme.md) about how to deploy and test it
- Clean

The program you implement must be a complete program product, i.e. should be easy to install, provide for the handling of non-standard situations, be resistant to incorrect user actions, etc. 