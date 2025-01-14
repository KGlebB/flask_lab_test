import random
import string
from app import db
from app.models import Dialogue, Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime

class DialogueService:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(DialogueService, cls).__new__(cls)
    return cls._instance

  def __init__(self):
    self.faq = {
      "Как вас зовут?": "Я чат-бот, созданный для помощи вам.",
      "Какой сегодня день?": "Сегодня {day}.",
      "Что вы можете делать?": "Я могу отвечать на ваши вопросы и помогать с информацией.",
      "Какой ваш любимый цвет?": "Я не имею предпочтений, но многие любят синий!",
      "Где вы находитесь?": "Я существую в облаке и доступен везде, где есть интернет."
    }
    self.vectorizer = TfidfVectorizer()
    self.vectors = self.vectorizer.fit_transform(self.faq.keys()).toarray()

  def get_user_dialogues(self, user_id):
    return Dialogue.query.filter_by(user_id=user_id).all()

  def get_dialogue(self, dialogue_id):
    return Dialogue.query.get_or_404(dialogue_id)

  def get_messages(self, dialogue_id):
    return Message.query.filter_by(dialogue_id=dialogue_id).order_by(Message.timestamp).all()

  def create_dialogue(self, user_id):
    title = 'Диалог ' + ''.join(random.choice(string.ascii_letters) for _ in range(3))
    new_dialogue = Dialogue(user_id=user_id, title=title)
    db.session.add(new_dialogue)
    db.session.commit()
    return new_dialogue

  def process_message(self, message, dialogue):
    user_vector = self.vectorizer.transform([message]).toarray()
    cosine_similarities = cosine_similarity(user_vector, self.vectors).flatten()
    best_match_index = np.argmax(cosine_similarities)
    best_match_question = list(self.faq.keys())[best_match_index]
    response = self.faq[best_match_question]

    if "{day}" in response.lower():
      now = datetime.now()
      response = response.format(day=now.strftime("%A, %d %B %Y"))

    if cosine_similarities[best_match_index] < 0.1:
      response = "Извините, я не знаю ответа на этот вопрос."

    new_message = Message(dialogue_id=dialogue.id, content=message, response=response)
    db.session.add(new_message)
    db.session.commit()
