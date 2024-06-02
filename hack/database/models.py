from config import DB_URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, func

db_url = DB_URL
DB_engine = create_async_engine(url=DB_URL)

async_session = async_sessionmaker(DB_engine)

Base = declarative_base()



class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    username = Column(String(255))
    message_text = Column(Text)


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_pool():
    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return async_session, engine
