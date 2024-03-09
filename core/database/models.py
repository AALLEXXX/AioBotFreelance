from .db import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey


class User(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    fullname : Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    phone_number : Mapped[str] = mapped_column(nullable=True, unique=True)
    date_registration : Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    tg_username : Mapped[str] = mapped_column(nullable=False)

    purchases = relationship('Purchase', back_populates='user')
    user_support_requests =  relationship('UserSupportRequest', back_populates='user')


class Purchase(Base):
    __tablename__ = 'purchases'

    id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    user_chat_id: Mapped[str] = mapped_column(ForeignKey('users.chat_id'))
    purchase_date: Mapped[DateTime] = mapped_column(DateTime)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=True)
    cost: Mapped[int] = mapped_column(nullable=True)
    pay_token: Mapped[str] = mapped_column(unique=True, nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    promo_id: Mapped[int] = mapped_column(nullable=True)

    course = relationship('Course', back_populates='purchase')
    user = relationship('User', back_populates='purchases')


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    course_module = relationship('Course_module', back_populates='course')
    purchase = relationship('Purchase', back_populates='course')
    promo = relationship('Promocode', back_populates='course')


class Course_module(Base):
    __tablename__ = 'course_modules'

    id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(nullable=True)
    media_file_path: Mapped[str] = mapped_column(nullable=True)
    time: Mapped[int] = mapped_column(nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=True)
    module_order: Mapped[int] = mapped_column(nullable=True)

    course = relationship('Course', back_populates='course_module')



class Promocode(Base):
    __tablename__ = 'promocodes'

    id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int]= mapped_column(ForeignKey('courses.id'))
    promo: Mapped[str] = mapped_column(nullable=True, unique=True)
    is_active : Mapped[bool] = mapped_column(default=False)

    course = relationship('Course', back_populates='promo')


class UserSupportRequest(Base):
    __tablename__ = 'user_support_requests'

    id: Mapped[int]= mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.chat_id'), nullable=True)
    question: Mapped[str] = mapped_column(nullable=True)    
    date: Mapped[DateTime] = mapped_column(DateTime)

    user =  relationship('User', back_populates='user_support_requests')