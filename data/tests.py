import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy.dialects import mysql

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title_picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    made_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    language_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("categories.id"))
    language = orm.relation('Category')
    user = orm.relation('User')
    __mapper_args__ = {
        'polymorphic_identity': 'tests',
        'polymorphic_on': type
    }


class FirstTest(Test):
    __tablename__ = 'first_tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'first_tests',
    }


class SecondTest(Test):
    __tablename__ = 'second_tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'), primary_key=True)
    # добавим контента

    __mapper_args__ = {
        'polymorphic_identity': 'second_tests',
    }
