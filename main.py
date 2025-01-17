import datetime

from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
import uvicorn
from psycopg2.extras import RealDictCursor
import time
import psycopg2
import qrcode

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


@app.get("/photo/{user_id}")
def create_qrcode(user_id: int = 1):
    dt = datetime.datetime.now()

    data = f"http://54.235.26.36/photo/{user_id}/{datetime}"

    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Thickness of the border (minimum is 4)
)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save("qrcode.png")

    return FileResponse("qrcode.png")


@app.put("http://54.235.26.36/photo/{user_id}/{datetime}")
def update_QR_use_to_True():
    pass


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)