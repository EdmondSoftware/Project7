from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
import uvicorn
from psycopg2.extras import RealDictCursor
import time
import psycopg2

from models import Base
from database import engine
from models import User
from auth import auth_router
from auth_schemas import UserSignUpSchema, UserLoginSchema
from auth import get_current_user


Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            database='test',
            password='password',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        break
    except Exception as err:
        print(err)
        time.sleep(3)

app = FastAPI()


@app.get("/")
def main():
    return

@app.get("/users")
def get_all_users():
    cursor.execute("""SELECT * from users""")
    users = cursor.fetchall()
    return users


@app.get("/photo")
def get_photo(current_user = Depends(get_current_user)):
    return FileResponse("photo.html")


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)