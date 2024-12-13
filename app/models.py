from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column  
from typing import List
from datetime import date
from PIL import Image
from authlib.integrations.flask_client import OAuth



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str]= mapped_column(db.String(20))
    dob: Mapped[date] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(db.String(500), nullable=False)

    images: Mapped[List['Images']] = db.relationship(back_populates = 'user')


class Images(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key= True)
    # image: Mapped[blob] = mapped_column(db.LargeBinary)
    image = db.Column(db.LargeBinary, nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))


    user: Mapped['Users'] = db.relationship(back_populates = 'images')