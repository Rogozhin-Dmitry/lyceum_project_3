from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin


class FirstTestPage(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'first_test_page'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    image_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    right_image_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)