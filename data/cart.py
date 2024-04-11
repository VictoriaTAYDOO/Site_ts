import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer,
                             nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
