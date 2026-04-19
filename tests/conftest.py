from fastapi.testclient import TestClient
from main import app
from config import settings
import models,schemas
from database import  get_db,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine=create_engine(SQLALCHEMY_DATABASE_URL)

