from fastapi import FastAPI
from database import engine
from models import Base
import psycopg2
from fastapi.responses import FileResponse

"Daniel mihatel register gri"
conn = psycopg2.connect(
    user = "postgres",
    host = "localhost",
    password = "password",
    database = "test"
    )

cursor = conn.cursor()

Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def main():
    return "Ok"

@app.get("/users")
def get_all_users():
    cursor.execute("""SELECT * from users""")
    users = cursor.fetchall()
    return users

@app.get("/photo")
def get_photo():
    return FileResponse("photo.html")
