from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas, utils, oauth2
from ..database import get_db
from ..utils import log

router = APIRouter(
    prefix="/create_digital_access_code",
    tags=['create']
)


@router.post('/', response_model=schemas.location_data_out)
def code_generator(location_data_payload: schemas.location_data_in, db: Session = Depends(get_db)):
    def generate_digital_access_code():
        while True:
            code = utils.generate_number()
            search_dac_query = db.query(models.Digital_access_code_location).filter(
                models.Digital_access_code_location.digital_access_code == code)
            if not search_dac_query.first():
                return code
    longitude_search = db.query(models.Digital_access_code_location).filter(
        models.Digital_access_code_location.longitude == location_data_payload.longitude)
    latitude_search = db.query(models.Digital_access_code_location).filter(
        models.Digital_access_code_location.latitude == location_data_payload.latitude)
    data_assigned_out = db.query(models.Digital_access_code_location).filter(
        models.Digital_access_code_location.longitude == location_data_payload.longitude).first()

    if longitude_search.first() and latitude_search.first():
        return data_assigned_out

    data_insert = models.Digital_access_code_location(
        **location_data_payload.dict(), digital_access_code=generate_digital_access_code())
    try:
        db.add(data_insert)
        db.commit()
        db.refresh(data_insert)
    except Exception as ex:
        log.error(
            f'Database error : {type(ex).__name__} : create_digital_acess_code')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{type(ex)},Error')
    return data_insert
