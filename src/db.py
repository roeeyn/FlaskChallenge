from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///github_users.db", connect_args={"check_same_thread": False}
)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
