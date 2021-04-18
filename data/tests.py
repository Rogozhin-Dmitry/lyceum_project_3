import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'test_association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('first_tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('first_tests.id')),
    sqlalchemy.Column('first_test_page', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('first_test_page.id'))
)


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
    open = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True,
                             default=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    language = orm.relation('Category')
    user = orm.relation('User')
    __mapper_args__ = {
        'polymorphic_identity': 'tests',
        'polymorphic_on': type
    }


class FirstTest(Test):
    __tablename__ = 'first_tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'), primary_key=True)
    pages = orm.relation("FirstTestPage",
                         secondary="test_association",
                         backref="first_tests")
    __mapper_args__ = {
        'polymorphic_identity': 'first_tests',
    }


another_association_table = sqlalchemy.Table(
    'second_test_association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('second_tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('second_tests.id')),
    sqlalchemy.Column('second_test_page', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('second_test_page.id'))
)


class SecondTest(Test):
    __tablename__ = 'second_tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'), primary_key=True)
    pages = orm.relation("SecondTestPage",
                         secondary="second_test_association",
                         backref="second_tests")

    __mapper_args__ = {
        'polymorphic_identity': 'second_tests',
    }
