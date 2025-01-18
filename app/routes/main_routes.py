from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.dialogue_service import DialogueService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
  return render_template('pages/index.html')

@main_bp.route('/about')
def about():
  return render_template('pages/about.html')
