from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from . import functions_ai
from .schema_ai import AiResponse, AiRequest
from auth.oauth2 import get_current_user
from user.schema_user import UserBase


router = APIRouter(
    prefix='/ai',
    tags=['AI'],
)

@router.post('', response_model=AiResponse)
async def submit_answer(payload: AiRequest, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return await functions_ai.getDeepSeekResponse(payload.tradition, payload.input_text ,current_user=current_user, db=db) 

# @router.post('', response_model=AiResponse)
# async def submit_answer(payload: AiRequest, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     return await functions_ai.getDeepSeekResponse(payload.card, payload.input_text ,current_user=current_user, db=db) 

# @router.post('/daily', response_model=AiResponse)
# async def submit_daily_answer(payload: AiRequest, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
#     return await functions_ai.getDailyDeepSeekResponse(payload.card, payload.input_text ,current_user=current_user, db=db) 