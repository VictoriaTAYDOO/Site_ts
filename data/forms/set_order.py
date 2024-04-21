from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class SetOrderForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    address = StringField('Адрес доставки', validators=[DataRequired()])
    comment = StringField('Комментарий к заказу', validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')
