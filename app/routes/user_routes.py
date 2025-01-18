from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.forms.user_forms import LoginForm, RegistrationForm
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user_service.create_user(form.username.data, form.password.data)
    flash('Успешная регистрация! Теперь вы можете войти.', 'success')
    return redirect(url_for('user.login'))
  return render_template('pages/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = user_service.authenticate_user(username, password)
    if user:
      login_user(user)
      return redirect(url_for('dialogue.all'))
    else:
      flash('Неверное имя пользователя или пароль', 'danger')
  return render_template('pages/login.html', form=form)

@user_bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('user.login'))
