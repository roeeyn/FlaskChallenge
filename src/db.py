from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

is_prod = getenv("ENV", "local") == "prod"

engine = create_engine(
    f"sqlite:///github_users{'' if is_prod else '_test'}.db",
    connect_args={"check_same_thread": False},
)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
