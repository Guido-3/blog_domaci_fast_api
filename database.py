from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=True)
# `engine`` manages connections to the db
# we can specify the pool size, max_overflow, isolation_level, query logging etc


Session = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


db = Annotated[Session, Depends(get_db)]
