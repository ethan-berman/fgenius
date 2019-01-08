import functools
from flask import ( Blueprint, flash, g, redirect, render_template,request,session,url_for)

from db import get_db
import auth
from auth import login_required
bp = Blueprint('media', __name__)
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('media/index.html', posts=posts)
@bp.route('/<artist>/<album>/<track>')
def display(artist, album, track):
    #generic function for creating the html page for accessihng a given track
    db = get_db();
    post = db.execute('SELECT * FROM post p WHERE title = ? AND artist = ?', (artist,track,) ).fetchone()
    if(post is not None):
        if(post[2] == 'song'):
            return render_template('/media/song.html', post = post)
        elif(post[2] == 'movie'):
            return render_template('/media/movie.html', post = post)
        elif(post[2] == 'television'):
            return render_template('/media/tv.html', post = post)
    else:
        return "error"


@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    #user is attemting to add an item to the collection
    #check that user is logged in, gather properties
    #submit the media object to the DATABASE
    if request.method == 'POST':
        title = request.form['title']
        format = request.form['format']
        artist = request.form['artist']
        body = None
        error = None
        if format == 'song':
            body = request['lyrics']
        elif format == 'movie':
            body = request['synopsis']
        elif format == 'television':
            body = request['screenplay']
        if not title:
            error = 'title error'
        if not body:
            error = 'no body'
        if not format:
            error = 'no format'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, artist, format, body, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, artist, format, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('media.index'))

    return render_template('media/create.html')
def get_media(id, check_author=True):
    post = get_db.execute('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
