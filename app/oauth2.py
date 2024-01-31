from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app import database
from .config import setting
from . import schemas, database, models
from statistics import mode
from jose import JWTError, jwt
from datetime import datetime, timedelta
oauth2_scheama = OAuth2PasswordBearer(tokenUrl='login')

SECRETE_KEY = setting.secrete_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRY = setting.access_token_expiry_minutes


def create_access_token(data: dict):
    to_include = data.copy()
    token_expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_include.update({'exp': token_expiry})
    jwt_token = jwt.encode(to_include, SECRETE_KEY, algorithm=ALGORITHM)
    return jwt_token


def verify_access_token(token: str, credetials_exeption):
    try:
        data = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        id: str = data.get('user_id')
        print(f'{id} inside verify access token')
        if id is None:
            raise credetials_exeption
        print('hello')
        token_data = schemas.tokenData(id=str(id))
        print('print token data',token_data)
    except:
        raise credetials_exeption
    return token_data


def get_current_user(token: str = Depends(oauth2_scheama), db: Session = Depends(database.get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate the creditainals',
                                         headers={'WWW-Authenticate': 'Bearer'})
    token = verify_access_token(token, credentials_exeption)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
