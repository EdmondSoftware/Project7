import datetime
from auth_schemas import UserSignUpSchema, UserLoginSchema
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from dbconn import DbConn

from jose import jwt, JWTError

from fastapi.security.oauth2 import OAuth2PasswordBearer
from security import hash_password, verify_password

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

auth_router = APIRouter(tags=['Auth'])

@auth_router.post("/sign_up")
def sign_app_user(data: UserSignUpSchema):
    dbconn = DbConn()

    dbconn.cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
                          (data.name, data.email, data.password))

    dbconn.conn.commit()

    return "OK"

@auth_router.post("/login_user")
def login_user(data: UserLoginSchema):
    dbconn = DbConn()

    try:
        email = data.email
        password = data.password
    except Exception as err:
        raise err

    try:
        dbconn.cursor.execute("""SELECT * FROM users
                                WHERE email=%s""",
                            (email,))
    except Exception as err:
        raise err

    try:
        user = dbconn.cursor.fetchone()
    except Exception as err:
        raise err

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' was not found!"
        )

    user = dict(user)

    if not verify_password(password, user.get('password')):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Wrong password -> '{password}'"
        )

    payload = {
        "user_id": user.get('id'),
        "email": user.get('email')
    }

    token = create_token(payload)

    return {"access_token": token}