import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class TemporarySecondTestCreate(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'temporary_second_test_create'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    count_of_tr = sqlalchemy.Column(sqlalchemy.Integer, default=10)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("created_tests.id"))
    data = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='{}')

