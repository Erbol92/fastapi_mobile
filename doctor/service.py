from doctor.models import *
from fastapi import  HTTPException, Depends, Query
from sqlalchemy.future import select
from sqlalchemy import update
from pydantic import BaseModel
from fastapi import APIRouter
from auth.db import User
from auth.user import current_active_user

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    await init_models()  # Инициализация моделей при старте приложения

# Модель для валидации данных при вставке


class DoctorCreate(BaseModel):
    first_name: str
    second_name: str
    last_name: str
    position_id: int


class SpecialityCreate(BaseModel):
    title: str


@router.get("/doctors/")
async def read_doctor(
    doctor_id: int = Query(None),  # Параметр запроса
    first_name: str = Query(None),
    second_name: str = Query(None),
    last_name: str = Query(None),
    session: AsyncSession = Depends(get_session)
):
    query = select(Doctor)

    # Добавляем условия поиска в зависимости от переданных параметров
    if doctor_id is not None:
        query = query.where(Doctor.id == doctor_id)
    if first_name is not None:
        query = query.where(Doctor.first_name == first_name)
    if second_name is not None:
        query = query.where(Doctor.second_name == second_name)
    if last_name is not None:
        query = query.where(Doctor.last_name == last_name)

    result = await session.execute(query)
    doctors = result.scalars().all()

    if not doctors:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctors


@router.put("/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, first_name: str, second_name: str, last_name: str, position_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(current_active_user)):
    stmt = update(Doctor).where(Doctor.id == doctor_id).values(
        first_name=first_name,
        second_name=second_name,
        last_name=last_name,
        position_id=position_id
    )
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {"message": "Doctor updated successfully"}


@router.post("/doctors/", response_model=DoctorCreate)
async def create_doctor(doctor: DoctorCreate, session: AsyncSession = Depends(get_session), user: User = Depends(current_active_user)):
    new_doctor = Doctor(
        first_name=doctor.first_name,
        second_name=doctor.second_name,
        last_name=doctor.last_name,
        position_id=doctor.position_id
    )
    session.add(new_doctor)
    await session.commit()
    # Обновляем объект, чтобы получить его ID
    await session.refresh(new_doctor)
    return new_doctor


@router.put("/speciality/{speciality_id}")
async def update_speciality(speciality_id: int, title: str, session: AsyncSession = Depends(get_session), user: User = Depends(current_active_user)):
    stmt = update(Speciality).where(Speciality.id == speciality_id).values(
        title=title
    )
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Speciality not found")

    return {"message": "Speciality updated successfully"}




@router.post("/speciality/", response_model=SpecialityCreate)
async def create_speciality(speciality: SpecialityCreate, session: AsyncSession = Depends(get_session), user: User = Depends(current_active_user)):
    new_speciality = Speciality(
        title=speciality.title
    )
    session.add(new_speciality)
    await session.commit()
    # Обновляем объект, чтобы получить его ID
    await session.refresh(new_speciality)
    return new_speciality


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}