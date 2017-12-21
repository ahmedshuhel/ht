from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///:memory:', echo=True)
Session = scoped_session(sessionmaker(bind=engine))
