from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.note import Base

engine = create_engine("sqlite:///notes.db", echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
