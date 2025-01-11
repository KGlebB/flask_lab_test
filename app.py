from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Модель для хранения диалогов
class Dialogue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)  # Заголовок диалога
    messages = db.relationship('Message', backref='dialogue', lazy=True)  # Связь с сообщениями

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dialogue_id = db.Column(db.Integer, db.ForeignKey('dialogue.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Заготовленные вопросы и ответы
faq = {
    "Как вас зовут?": "Я чат-бот, созданный для помощи вам.",
    "Какой сегодня день?": "Сегодня {day}.",
    "Что вы можете делать?": "Я могу отвечать на ваши вопросы и помогать с информацией.",
    "Какой ваш любимый цвет?": "Я не имею предпочтений, но многие любят синий!",
    "Где вы находитесь?": "Я существую в облаке и доступен везде, где есть интернет."
}

# Векторизация вопросов
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(faq.keys()).toarray()

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))  # Redirect to registration if not logged in
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dialogues')
@login_required
def dialogues():
    user_dialogues = Dialogue.query.filter_by(user_id=current_user.id).all()
    return render_template('dialogues.html', dialogues=user_dialogues)

@app.route('/dialogue/<int:dialogue_id>', methods=['GET', 'POST'])
@login_required
def continue_dialogue(dialogue_id):
    dialogue = Dialogue.query.get_or_404(dialogue_id)
    if request.method == 'POST':
        user_input = request.form['message']
        
        # Векторизация пользовательского ввода
        user_vector = vectorizer.transform([user_input]).toarray()
        
        # Вычисление косинусного сходства
        cosine_similarities = cosine_similarity(user_vector, vectors).flatten()
        
        # Находим индекс наиболее похожего вопроса
        best_match_index = np.argmax(cosine_similarities)
        
        # Получаем ответ на основе наиболее похожего вопроса
        best_match_question = list(faq.keys())[best_match_index]
        response = faq[best_match_question]
        
        # Если вопрос о дне, добавляем текущую дату
        if "сегодня" in user_input.lower():
            now = datetime.now()
            response = response.format(day=now.strftime("%A, %d %B %Y"))
        
        if cosine_similarities[best_match_index] < 0.1:  # Порог для определения "неизвестного"
            response = "Извините, я не знаю ответа на этот вопрос."
        
        new_message = Message(dialogue_id=dialogue.id, content=user_input, response=response)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('continue_dialogue', dialogue_id=dialogue.id))
    
    messages = Message.query.filter_by(dialogue_id=dialogue.id).all()
    return render_template('continue_dialogue.html', dialogue=dialogue, messages=messages)

@app.route('/new_dialogue', methods=['GET', 'POST'])
@login_required
def new_dialogue():
    if request.method == 'POST':
        title = request.form['title']
        new_dialogue = Dialogue(user_id=current_user.id, title=title)
        db.session.add(new_dialogue)
        db.session.commit()
        return redirect(url_for('dialogues'))
    return render_template('new_dialogue.html')

if __name__ == '__main__':
    with app.app_context():  # Создаем контекст приложения
        db.create_all()  # Создаем таблицы в базе данных
    app.run(debug=True)
