import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()


class Speciality(Base):
    __tablename__ = 'speciality'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=30), unique=True)

    def __str__(self):
        return self.title


class Doctor(Base):
    __tablename__ = 'doctor'

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    second_name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    last_name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    position_id = sq.Column(sq.Integer, sq.ForeignKey(
        'speciality.id'))  # Внешний ключ на Speciality
    position = relationship(Speciality, backref='doctors')

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.last_name} '


DSN = "postgresql+asyncpg://postgres:postgres@localhost:5432/nefertiti"
engine = create_async_engine(DSN, echo=True)

# сессия
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Удаляем все таблицы
        await conn.run_sync(Base.metadata.create_all)  # Создаем таблицы заново

# Зависимость для получения сессии


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
