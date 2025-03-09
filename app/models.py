from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from datetime import datetime, timezone
from uuid import uuid4

from app import db, login


class User(UserMixin, db.Model):
    class Status(Enum):

        admin = 1
        tutor = 2
        teacher = 3
        user = 4

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    status: so.Mapped[Status] = so.mapped_column(sa.INTEGER)
    phone: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<Пользователь {}>'.format(self.username)
  
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))


class Classes(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    class_parral: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)


    def __repr__(self):
        return '<Класс {}>'.format(self.class_name)

class Student(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    surname: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    class_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Classes.id, ondelete="CASCADE"), index=True, nullable=True)
    tutor_id: so.Mapped[int] = so.mapped_column(sa.Integer(), index=True, nullable=True)
    paral: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    uuid: so.Mapped[str] = so.mapped_column(sa.Uuid(), index=True, default=uuid4())
    at_school: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id, ondelete="CASCADE"), nullable=True)


    def __repr__(self):
        return '<User {}>'.format(self.name)

# class User(db.model):

    # class Status(Enum):

    #     admin = 1
    #     tutor = 2
    #     teacher = 3

#     user_id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     class_id: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     class_parral: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     surname: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     uuid: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     login: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     password: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
#     password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
#     status: so.Mapped[Status]


#     def __repr__(self):
#         return '<User {}>'.format(self.username)

class Enter_exit(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Student.id, ondelete="CASCADE"), index=True)
    enter_time: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now())
    exit_time: so.Mapped[datetime] = so.mapped_column(
        index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)