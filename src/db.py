from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

local_env = getenv("ENV", "local")

# As we're using the same seeded DB for local and prod we can use this
is_prod = local_env == "prod" or local_env == "local"

engine = create_engine(
    f"sqlite:///github_users{'' if is_prod else '_test'}.db",
    connect_args={"check_same_thread": False},
)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
