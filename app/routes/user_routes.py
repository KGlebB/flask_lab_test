from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if user_service.create_user(username, password):
      flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
      return redirect(url_for('user.login'))
    else:
      flash('Ошибка регистрации. Попробуйте снова.', 'danger')
  return render_template('pages/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = user_service.authenticate_user(username, password)
    if user:
      login_user(user)
      return redirect(url_for('dialogue.all'))
    else:
      flash('Неверное имя пользователя или пароль', 'danger')
  return render_template('pages/login.html')

@user_bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('user.login'))
