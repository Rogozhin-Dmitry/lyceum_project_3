import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class TemporaryFirstTestCreate(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'temporary_first_test_create'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("created_tests.id"))
    data = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='{}')
    load_image = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=True)
