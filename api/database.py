from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./auth.db"

# Tạo engine bất đồng bộ
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Tạo session bất đồng bộ
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db():
    async with async_session() as session:
        yield session
