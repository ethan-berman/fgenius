from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from auth import login_required
from db import get_db

bp = Blueprint('song', __name__, url_prefix='/song')

@bp.route('/')
def index():
    db = get_db()
    #index of the songs blueprint, display top songs here maybe
    return "top songs"
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
