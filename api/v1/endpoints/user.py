from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.user_model import UserModel
from core.deps import get_session

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim Bypass

router = APIRouter()

# POST USER
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def post_user(user: UserModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).order_by(UserModel.id.desc())
        result = await session.execute(query)
        usr = result.scalars().first()
        if usr:
            next_id = usr.id + 1
        else:
            next_id = 1
    new_user = UserModel(
        id = next_id,
        first_name = user.first_name,
        last_name = user.last_name,
        full_name = user.full_name,
        job_type = user.job_type,
        phone = user.phone,
        email = user.email,
        image = user.image,
        country = user.country,
        city = user.city,
        onboarding_completion = user .onboarding_completion
    )
    db.add(new_user)
    await db.commit()
    return new_user

# GET USERS
@router.get('/', response_model=List[UserModel])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()
    return users

# GET USER
@router.get('/{user_id}', response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()
        if user:
            return user
        else:
            raise HTTPException(detail='User não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

# PUT USER
@router.put('/{user_id}', response_model=UserModel, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up = result.scalar_one_or_none()
        if user_up:
            user_up.first_name = user.first_name
            user_up.last_name = user.last_name
            user_up.full_name = user.full_name
            user_up.job_type = user.job_type
            user_up.phone = user.phone
            user_up.email = user.email
            user_up.image = user.image
            user_up.country = user.country
            user_up.city = user.city
            user_up.onboarding_completion = user.onboarding_completion
            await session.commit()
            return user_up
        else:
            raise HTTPException(detail='User não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

# DELETE User
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del = result.scalar_one_or_none()
        if user_del:
            await session.delete(user_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='User não encontrado.', status_code=status.HTTP_404_NOT_FOUND)