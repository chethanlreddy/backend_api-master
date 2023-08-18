from statistics import mode
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import oauth2
from ..utils import log
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List
from fastapi.params import Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/delete_user",
    tags=['delete user']
)

@router.delete('/{mail}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(mail : str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    search_user_data = db.query(models.User).filter(models.User.email == mail)
    if not search_user_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'users whith {mail} not found')
    get_userid = search_user_data.first()
    if get_userid.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='UnAuthorized')
    print(current_user.id)
    validate_user = db.query(models.User).filter(models.User.id == current_user.id)
    try:
        validate_user.delete(synchronize_session=False)
        db.commit()
    except Exception as ex:
        log.error(f'Database Error : {type(ex).__name__} : delete user')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = f'{type(ex)}, Error')
    return Response(status_code=status.HTTP_204_NO_CONTENT)