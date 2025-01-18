import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=25)])
  password = PasswordField('Пароль', validators=[DataRequired()])
  submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
  username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=25)])
  password = PasswordField('Пароль', validators=[DataRequired()])
  confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать.')])
  submit = SubmitField('Зарегистрироваться')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Имя пользователя уже занято. Пожалуйста, выберите другое.')

  def validate_password(self, password):
    password_data = password.data
    if len(password_data) < 8:
      raise ValidationError('Пароль должен содержать не менее 8 символов.')
    if not re.search(r"[A-Z]", password_data):
      raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
    if not re.search(r"[a-z]", password_data):
      raise ValidationError('Пароль должен содержать хотя бы одну строчную букву.')
    if not re.search(r"[0-9]", password_data):
      raise ValidationError('Пароль должен содержать хотя бы одну цифру.')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password_data):
      raise ValidationError('Пароль должен содержать хотя бы один специальный символ.')
