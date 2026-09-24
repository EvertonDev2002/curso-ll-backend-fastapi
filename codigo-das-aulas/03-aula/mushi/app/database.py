from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)
