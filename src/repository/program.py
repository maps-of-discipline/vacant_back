from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.db import sessionmaker


class ProgramRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    
