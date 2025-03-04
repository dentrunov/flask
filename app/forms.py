from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Логин', validators=[DataRequired()])
  password = PasswordField('Пароль', validators=[DataRequired()])
  remember_me = BooleanField('Запомнить меня')
  submit = SubmitField('Авторизация')

class RegistrationForm(FlaskForm):
  username = StringField('Логин', validators=[DataRequired()])
  email = StringField('Электронная почта', validators=[DataRequired(), Email()])
  password = PasswordField('Пароль', validators=[DataRequired()])
  password2 = PasswordField(
    'Повторите пароль ', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Регистрация')

  def validate_username(self, username):
    user = db.session.scalar(sa.select(User).where(
      User.username == username.data))
    if user is not None:
      raise ValidationError('используйте другое имя пользователя')

  def validate_email(self, email):
    user = db.session.scalar(sa.select(User).where(
      User.email == email.data))
    if user is not None:
      raise ValidationError('используйте другую электронную почту')

class AddStudentsForm(FlaskForm):
  name = StringField('Имя', validators=[DataRequired()])
  surname = StringField('Фамилия', validators=[DataRequired()])
  par = SelectField('Параллель', choices=list(range(5, 12)))
  class_ = SelectField('Класс', choices=['А', 'Б', 'В', 'Г', 'Д'])
  submit = SubmitField('Регистрация')

class EditInformationForm(FlaskForm):
  name = StringField('Имя', validators=[DataRequired()])
  surname = StringField('Фамилия', validators=[DataRequired()])
  email = StringField('Электронная почта', validators=[DataRequired(), Email()])
  phone = StringField('Номер телефона')
  submit = SubmitField('Отредактировать')
