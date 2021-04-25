import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class CreatedTest(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'created_tests'

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
    open = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True,
                             default=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    language = orm.relation('Category')
