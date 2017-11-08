from flask import render_template
from app.main import main
from app import db
from app.models import Component

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')