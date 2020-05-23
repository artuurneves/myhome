from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')


class Product(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    current_qnt = FloatField('current_qnt')
    necessary_qnt = FloatField('necessary_qnt', validators=[DataRequired()])
    product_type_id = SelectField('product_type_id', validate_choice=False)


class ProductType(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class Item(FlaskForm):
    item_name = StringField('item_name', validators=[DataRequired()])
    item_brand = StringField('item_brand', validators=[DataRequired()])
    item_price = FloatField('item_price', validators=[DataRequired()])
    item_qnt = FloatField('item_qnt', validators=[DataRequired()])


class Shopping(FlaskForm):
    supermarket = StringField('supermarket', validators=[DataRequired()])
    date = DateField('date', format='%d-%m-%Y', validators=[DataRequired()])
