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

    images: Mapped[List['Images']] = db.relationship('Images', back_populates = 'user')
    leaderboard_images: Mapped[List['Leaderboard']] = db.relationship('Leaderboard', back_populates='user')
    comments: Mapped[List['LeaderboardComment']] = db.relationship('LeaderboardComment',  back_populates = 'user')
    likes: Mapped[List ['LeaderboardLike']] = db.relationship('LeaderboardLike', back_populates='user')


class Images(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key= True)
    # image: Mapped[blob] = mapped_column(db.LargeBinary)
    image = db.Column(db.LargeBinary, nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))

    # leaderboard_images: Mapped[List['Leaderboard]] = db.relationship('Leaderbaord', back_populates='orignal_image')

    user: Mapped['Users'] = db.relationship('Users', back_populates = 'images')
    leaderboard: Mapped[List['Leaderboard']] = db.relationship('Leaderboard', back_populates = 'original_image')

class Leaderboard(Base):
    __tablename__ = 'leaderboard'
    id: Mapped[int] = mapped_column(primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    original_image_id: Mapped[int] = mapped_column(db.ForeignKey('images.id'))

    user: Mapped['Users'] = db.relationship('Users', back_populates = 'leaderboard_images')
    original_image: Mapped['Images'] = db.relationship('Images', back_populates= 'leaderboard')
    comments: Mapped[List['LeaderboardComment']] = db.relationship('LeaderboardComment', back_populates = 'leaderboard_image')
    likes: Mapped[List['LeaderboardLike']] = db.relationship('LeaderboardLike', back_populates = 'leaderboard_image')


    def like_count(self):
        return len(self.likes)
    
    def comment_count(self): 
        return len(self.comments)
    

class LeaderboardComment(Base):
    __tablename__ = 'leaderboard_comments'

    id: Mapped[int] = mapped_column(primary_key =True)
    text: Mapped[str] = mapped_column(db.String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    leaderboard_image_id: Mapped[int] = mapped_column(db.ForeignKey('leaderboard.id'))

    user: Mapped['Users'] = db.relationship('Users', back_populates = 'comments')
    leaderboard_image: Mapped['Leaderboard'] = db.relationship('Leaderboard', back_populates = 'comments')



class LeaderboardLike(Base):
    __tablename__ = 'leaderboard_likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    leaderboard_image_id: Mapped[int] = mapped_column(db.ForeignKey('leaderboard.id'))

    user: Mapped['Users'] = db.relationship('Users', back_populates= 'likes')
    leaderboard_image: Mapped['Leaderboard'] = db.relationship('Leaderboard', back_populates ='likes')