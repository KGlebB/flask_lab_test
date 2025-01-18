from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.dialogue_service import DialogueService

dialogue_bp = Blueprint('dialogue', __name__)
dialogue_service = DialogueService()

@dialogue_bp.route('/chat')
def all():
  dialogue_id = request.args.get('dialogueId')
  dialogues = []
  messages = []
  if current_user.is_authenticated:
    dialogues = dialogue_service.get_user_dialogues(current_user.id)
    if dialogue_id:
      dialogue = dialogue_service.get_dialogue(dialogue_id)
      if dialogue.user_id == current_user.id:
        messages = dialogue_service.get_messages(dialogue_id)
      else:
        return abort(403, description="Запрещено просматривать чужие диалоги.")
  return render_template('pages/chat.html', dialogues=dialogues, messages=messages)

@dialogue_bp.route('/send', methods=['POST'])
@login_required
def send():
  dialogue_id = request.args.get('dialogueId')
  message = request.form['message']
  if dialogue_id is not None:
    dialogue = dialogue_service.get_dialogue(dialogue_id)
  else:
    dialogue = dialogue_service.create_dialogue(current_user.id)
  dialogue_service.process_message(message, dialogue)
  return redirect(url_for('dialogue.all', dialogueId=dialogue.id))
