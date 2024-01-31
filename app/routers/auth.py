from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, database, schemas, utils, oauth2
router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)


@router.post('/', response_model=schemas.tokenOut)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # if user_data.username.isdigit():
    #     # if len(user_data.username) > 10 or len(user_data.username) < 10:
    #     #     user = db.query(models.User).filter(models.User.phone_number == user_data.username).first()
    #     # else:
    #     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid phone number')
    #     user = db.query(models.User).filter(
    #         models.User.phone_number == user_data.username).first()
    # else:
    user = db.query(models.User).filter(
            models.User.email == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    if not utils.verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    print(f'user-id :{user.id}')
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'Bearer'}
