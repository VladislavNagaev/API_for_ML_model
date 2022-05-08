from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from app.modules import  ModelProcessing, TokenVerification
from app.forms import PredictionData, AnswerData
from typing import Union, Dict
from loguru import logger
import os


logger.add(
    'debug.json', 
    format='{time} {level} {message}', 
    level='INFO', 
    rotation="10 MB",
    compression='zip',
    serialize=True
)


POSTGRES_USER = os.environ.get(key='POSTGRES_USER', default='')
POSTGRES_PASSWORD = os.environ.get(key='POSTGRES_PASSWORD', default='')
POSTGRES_HOST = os.environ.get(key='POSTGRES_HOST', default='')
POSTGRES_PORT = os.environ.get(key='POSTGRES_PORT', default='')
POSTGRES_DB = os.environ.get(key='POSTGRES_DB', default='')
MLFLOW_URI = os.environ.get(key='MLFLOW_URI', default='')
MODEL_NAME = os.environ.get(key='MODEL_NAME', default='')



router = APIRouter()

@logger.catch
@router.get('/', tags=["root"])
def index() -> dict:
    return {'status': 'OK' }

@logger.catch
@router.post(
    '/model', 
    response_model=AnswerData, 
    description='Return predictions'
)
def predict(
    *, 
    token: str, 
    data: PredictionData, 
) -> Dict:

    logger.info(f'token: {token} data: {data}')

    authorized = TokenVerification(
        postgres_user=POSTGRES_USER, 
        postgres_password=POSTGRES_PASSWORD, 
        postgres_host=POSTGRES_HOST, 
        postgres_port=POSTGRES_PORT, 
        postgres_db=POSTGRES_DB, 
    ).verify_token(token)

    if authorized:
    
        dict_data = data.dict(by_alias=True)

        model_processing = ModelProcessing(
            mlflow_uri=MLFLOW_URI,
            model_name=MODEL_NAME,
        )
        model_processing.load()
        answer_dict = model_processing.predict(
            data=dict_data, 
            inverse_target=True
        )

        return answer_dict
    
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
