from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_basic.database import get_session
from fast_basic.models import User
from fast_basic.schemas import Token
from fast_basic.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: Session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=404, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
