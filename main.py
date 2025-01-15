from fastapi import FastAPI
from database import  engine
from models import Base

Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def main():
    return "Ok"
