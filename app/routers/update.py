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
    prefix="/update_user",
    tags=['update user']
)


@router.put('/user_profile/{mail}', response_model=schemas.userCollectOut)
def update_user(mail : str, update_data_payload: dict = Body(...),
                db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    validate_phone_number = db.query(models.User_data).filter(
        models.User_data.email == mail)
    if not validate_phone_number.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user not found with mail-id {mail}')
    print_id = validate_phone_number.first()
    if print_id.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='you are not authorized')
    query_user_data = db.query(models.User_data).filter(
        models.User_data.owner_id == current_user.id)
    queru_user_auth = db.query(models.User).filter(models.User.id == current_user.id)
    if 'email' in update_data_payload.keys():
        try:
            queru_user_auth.update({'email' : update_data_payload['email']})
            db.commit()
        except Exception as ex:
            log.error(f'Database Error :{type(ex).__name__} : user mail change')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Error')
    try:
        query_user_data.update(update_data_payload, synchronize_session=False)
        db.commit()
    except Exception as ex:
        log.error(
            f'Database Error : {type(ex).__name__} : update_data_profile')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{type(ex)},error')
    return query_user_data.first()


@router.put('/password_reset/{ph_no}')
def change_password(ph_no: int, new_password: schemas.new_password_in, db: Session = Depends(get_db)):
    print(new_password)
    validate_credentials = db.query(models.User).filter(
        models.User.phone_number == ph_no)
    if not validate_credentials.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'user not found')
    if new_password.password != new_password.retype_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='passwords does not match')
    get_phone_id = validate_credentials.first()
    query_upadte_data = db.query(models.User).filter(
        models.User.id == get_phone_id.id)
    new_password = utils.hash_password(new_password.password)
    try:
        query_upadte_data.update(
            {'password': new_password}, synchronize_session=False)
        db.commit()
    except Exception as ex:
        log.error(f'Databse Error : {type(ex).__name__} : update_password')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{type(ex)},Error')
    return True


@router.put('/update_users_location/{ph_no}')
def update_location_data(ph_no: int, data_payload: dict = Body(...), db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
    validate_credentials = db.query(models.User_data).filter(
        models.User_data.phone_number == ph_no)
    if not validate_credentials.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'user not found')
    get_user_id = validate_credentials.first()
    if get_user_id.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not Authorized')
    update_query = db.query(models.User_location_data).filter(
        models.User_location_data.owner_id == current_user.id)
    try:
        update_query.update(data_payload, synchronize_session=False)
        db.commit()
    except Exception as ex:
        log.error(
            f'Database Error : {type(ex).__name__} : upadte_user_location')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{type(ex).__name__}, Error')
    return update_query.first()


@router.put('/change_phone_number', status_code=status.HTTP_200_OK)
def change_phone_number(data_payload: schemas.phone_number_in, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    search_phone_number = db.query(models.User).filter(
        models.User.phone_number == data_payload.phone_number)
    if search_phone_number.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Phone Number already exist')
    search_user_id = db.query(models.User).filter(
        models.User.id == current_user.id)
    if not search_user_id.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='UnAuthorized')
    change_in_users = db.query(models.User).filter(
        models.User.id == current_user.id)
    change_in_users_data = db.query(models.User_data).filter(
        models.User_data.owner_id == current_user.id)
    try:
        change_in_users.update(
            {'phone_number': data_payload.phone_number}, synchronize_session=False)
        change_in_users_data.update(
            {'phone_number': data_payload.phone_number}, synchronize_session=False)
        db.commit()
    except Exception as ex:
        log.error(
            f'Database Error : {type(ex).__name__} : change phone number')
    return Response(status_code=status.HTTP_200_OK)
