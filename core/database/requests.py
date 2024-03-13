from typing import Tuple
from core.database.basedao import BaseDAO
from core.database.models import Purchase, User, Course, Course_module, UserSupportRequest, Promocode
from sqlalchemy import ResultProxy, and_, bindparam, delete, func, insert, or_, select, text, update
from core.database.db import async_session_maker

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session: 
            query = select(cls.model.__table__.columns).filter(cls.model.chat_id == model_id)
            result: ResultProxy = await session.execute(query)
            return result.mappings().one_or_none()
    @classmethod
    async def find_reg_user_by_id(cls, model_id: int):
        async with async_session_maker() as session: 
            query = select(cls.model.__table__.columns).filter(and_(cls.model.chat_id == model_id, cls.model.phone_number != None))
            result: ResultProxy = await session.execute(query)
            return result.mappings().one_or_none()
        
    @classmethod
    async def get_names_unpurchased_courses(cls, user_id) -> list: 
        async with async_session_maker() as session: 
            stmt = (
        select(Course)
        .where(
            ~Course.id.in_(
                select(Purchase.course_id)
                .where(Purchase.user_chat_id == user_id)
                    )
                )
            )

            result = await session.execute(stmt)
            courses_not_purchased = result.scalars().all() #TODO
            courses = list()
            for course in courses_not_purchased:
                courses.append(course.name)
            return courses

    @classmethod
    async def get_chat_id_all_admin(cls) -> list[Tuple[str]]:
        async with async_session_maker() as session:
            stmt = (select(User.chat_id).where(User.role == 'admin'))
            result = await session.execute(stmt)

            return result.fetchall()

    @classmethod
    async def update_by_id(cls, model_id, **data):
        async with async_session_maker() as session:
            condition = cls.model.__table__.c.chat_id == model_id
            query = update(cls.model.__table__).where(condition).values(**data)
            await session.execute(query)
            await session.commit()




class CourseDAO(BaseDAO): 
    model = Course

    @classmethod
    async def find_by_course_name(cls, course_name: str) -> Tuple:
        async with async_session_maker() as session: 
            stmt = select(cls.model.id, cls.model.name, cls.model.description, cls.model.cost).where(cls.model.name.like(bindparam('pattern', f'%{course_name}%')))
            result: ResultProxy = await session.execute(stmt)
            return result.fetchone()




class PurchaseDAO(BaseDAO):
    model = Purchase
    @classmethod
    async def find_pay_token_by_id(cls, model_id: int):
        async with async_session_maker() as session: 
            query = select(cls.model.pay_token).filter(cls.model.user_chat_id == model_id)
            result: ResultProxy = await session.execute(query)
            return result.fetchone()
        

    @classmethod
    async def delete_by_pay_token(cls, pay_token: str):
        async with async_session_maker() as session:
            await session.execute(Purchase.__table__.delete().where(Purchase.pay_token == pay_token))
            await session.commit()
    

    @classmethod
    async def update_by_pay_token(cls, pay_token, **data):
        async with async_session_maker() as session:
            condition = cls.model.__table__.c.pay_token == pay_token
            query = update(cls.model.__table__).where(condition).values(**data)
            await session.execute(query)
            await session.commit()


class Course_modulesDAO(): 
    model = Course_module

    @classmethod
    async def get_all_modules(cls, course_id) -> Tuple:
        """
        select description, time, module_order 
        from course_modules 
        where course_id = 1
        order by module_order;
        """
        async with async_session_maker() as session: 
            stmt = select(Course_module.description,
                          Course_module.time,
                          Course_module.module_order
                          ).select_from(Course_module).filter(Course_module.course_id == course_id).order_by(Course_module.module_order)
            result = await session.execute(stmt)
            return result.fetchall()



class UserSupportRequestDAO(BaseDAO):
    model = UserSupportRequest

    
class PromocodeDAO(BaseDAO):
    model = Promocode

    