import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tprice = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
