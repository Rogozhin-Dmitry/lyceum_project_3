import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class TemporaryThirdTest(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'temporary_third_test'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    selected_page = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    test_id = sqlalchemy.Column(sqlalchemy.Integer)
    data = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='{}')
    result_data = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='{}')
    test_type = sqlalchemy.Column(sqlalchemy.Integer)

