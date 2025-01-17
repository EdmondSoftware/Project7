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


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        current_user = verify_token(token)
        return current_user
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="In UserApp/services/auth.py function get_current_user()\n"
                                   "Error occurred while trying to get current user\n"
                                   f"ERR: {err}")


def create_token(user_data: dict):
    token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "exp": token_exp,
        "user": user_data
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={
            "WWW-Authenticated": 'Bearer'
        }
    )

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except JWTError:
        raise exception

    user_data = payload.get('user')

    return user_data


auth_router = APIRouter(tags=['Auth'])

@auth_router.post("/sign_up")
def sign_app_user(data: UserSignUpSchema):
    hashed_password = hash_password(data.password)
    dbconn = DbConn()

    dbconn.cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
                          (data.name, data.email, hashed_password))

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