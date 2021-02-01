from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.db import engine
from pydantic import BaseModel

Base = declarative_base()


class GitHubUserOrm(Base):
    __tablename__ = "github_users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    img_url = Column(String)
    profile_url = Column(String)
    user_type = Column("type", String)

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.img_url}, {self.profile_url}, {self.user_type}"


Base.metadata.create_all(engine)


class GitHubUser(BaseModel):
    id: int
    username: str
    img_url: str
    profile_url: str
    user_type: str

    class Config:
        orm_mode = True
