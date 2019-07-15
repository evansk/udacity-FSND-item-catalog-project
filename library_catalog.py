from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response

from database_setup import Base, Patrons, Authors, Books, Genres

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "udacityrestuarantmenuapp"

# Create session and connect to DB
engine = create_engine('sqlite:///librarycatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/library')
def showLibrary():
    return render_template('library.html')


@app.route('/login')
def showLogin():
    if not loginCheck():
        return redirect('/logout')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print request.args.get('state')
        print login_session['state']
        print 'Validating state token fail'
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        print 'FlowExchangeError'
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        print 'result get error is not none'
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        print 'User already connected'
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        return redirect(url_for('gdisconnect'))
    else:
        return render_template('logout.html')


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
    params={'token': access_token},
    headers={'content-type': 'application/x-www-form-urlencoded'})
    result=getattr(revoke, 'status_code')
    status_code=getattr(revoke, 'status_code')
    if status_code == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Disconnected.'), 200)
        redirect('/')
        flash("You have Successfully logged out")
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def loginCheck():
    if 'username' not in login_session:
        return True
    else:
        return False


@app.route('/patrons')
def showPatronList():
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    patrons = session.query(Patrons).all()
    return render_template('patron_list.html', patrons=patrons)

@app.route('/patrons/JSON')
def patronListJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    patrons = session.query(Patrons).all()
    return jsonify(Patron=[p.serialize for p in patrons])


@app.route('/patrons/<int:patron_id>')
def showPatron(patron_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    patron = session.query(Patrons).filter_by(id = patron_id).one()

    try:
        books = session.query(Books).filter_by(patron_id = patron_id)
    except:
        books = None

    return render_template('patron.html',patron=patron, books=books)

@app.route('/patrons/<int:patron_id>/JSON')
def patronJSON(patron_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    patron = session.query(Patrons).filter_by(id = patron_id).one()

    try:
        books = session.query(Books).filter_by(patron_id = patron_id)
    except:
        books = None
    return jsonify(Patron=[patron.serialize], Book=[b.serialize for b in books])



@app.route('/authors')
def showAuthorList():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    authors = session.query(Authors).all()
    return render_template('author_list.html', authors=authors)


@app.route('/authors/JSON')
def authorListJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    authors = session.query(Authors).all()
    return jsonify(Author=[a.serialize for a in authors])


@app.route('/authors/<int:author_id>')
def showAuthor(author_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    author = session.query(Authors).filter_by(id = author_id).one()
    books = session.query(Books).filter_by(author_id = author_id)
    return render_template('author.html', author=author, books=books)


@app.route('/authors/<int:author_id>/JSON')
def authorJSON(author_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    author = session.query(Authors).filter_by(id = author_id).one()
    books = session.query(Books).filter_by(author_id = author_id)
    return jsonify(Author=[author.serialize], Books=[b.serialize for b in books])


@app.route('/books')
def showBookList():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    books = session.query(Books).all()
    return render_template('book_list.html', books=books)


@app.route('/books/JSON')
def bookListJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    books = session.query(Books).all()
    return jsonify(Book=[b.serialize for b in books])


@app.route('/books/<int:book_id>')
def showBook(book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id = book_id).one()
    try:
        author = session.query(Authors).filter_by(id = book.author_id).one()
    except:
        author = None
    try:
        genre = session.query(Genres).filter_by(id = book.genre_id).one()
    except:
        genre = None
    try:
        patron = session.query(Patrons).filter_by(id = book.patron_id).one()
    except:
        patron = None
    return render_template('book.html', book=book, author=author, genre=genre, patron=patron)


@app.route('/books/<int:book_id>/JSON')
def bookJSON(book_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id = book_id).one()
    try:
        author = session.query(Authors).filter_by(id = book.author_id).one()
    except:
        author = None
    try:
        genre = session.query(Genres).filter_by(id = book.genre_id).one()
    except:
        genre = None
    try:
        patron = session.query(Patrons).filter_by(id = book.patron_id).one()
    except:
        return jsonify(Book=[book.serialize], Author=[author.serialize],Genre=[genre.serialize])
    return jsonify(Book=[book.serialize], Author=[author.serialize],Genre=[genre.serialize],Patron=[patron.serialize])


@app.route('/genres')
def showGenreList():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    genres = session.query(Genres).all()
    return render_template('genre_list.html', genres=genres)


@app.route('/genres/JSON')
def genreListJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    genres = session.query(Genres).all()
    return jsonify(Genre=[g.serialize for g in genres])


@app.route('/genres/<int:genre_id>')
def showGenre(genre_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    genre = session.query(Genres).filter_by(id = genre_id).one()
    books = session.query(Books).filter_by(genre_id = genre_id)
    return render_template('genre.html', genre=genre, books=books)


@app.route('/genres/<int:genre_id>/JSON')
def genreJSON(genre_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    genre = session.query(Genres).filter_by(id = genre_id).one()
    books = session.query(Books).filter_by(genre_id = genre_id)
    return jsonify(Genre=[genre.serialize], Book=[b.serialize for b in books])


@app.route('/patrons/add', methods=['GET', 'POST'])
def addPatron():
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        newPatron = Patrons(name=request.form['name'], email=request.form['email'])
        session.add(newPatron)
        session.commit()
        flash("New Patron Added")
        return redirect(url_for('showPatronList'))
    else:
        return render_template('add_patron.html')


@app.route('/patrons/<int:patron_id>/edit', methods=['GET', 'POST'])
def editPatron(patron_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedPatron = session.query(Patrons).filter_by(id=patron_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedPatron.name = request.form['name']
        if request.form['email']:
            editedPatron.email = request.form['email']

        session.add(editedPatron)
        session.commit()
        flash("Patron Edited")
        return redirect(url_for('showPatron', patron_id=patron_id))

    else:
        return render_template('edit_patron.html', patron=editedPatron)


@app.route('/patrons/<int:patron_id>/delete', methods=['GET', 'POST'])
def deletePatron(patron_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    patron = session.query(Patrons).filter_by(id=patron_id).one()
    books = session.query(Books).filter_by(patron_id=patron_id).all()
    if request.method == 'POST':
        if books:
            flash('Please have the patron return all books before deleting')
            return render_template('delete_patron.html', patron=patron, books=books)
        else:
            session.delete(patron)
            session.commit()
            flash("Patron deleted")
            return redirect(url_for('showPatronList'))
    else:
        return render_template('delete_patron.html', patron=patron, books=books)


@app.route('/authors/<int:author_id>/edit', methods=['GET', 'POST']) #add id see example
def editAuthor(author_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedAuthor = session.query(Authors).filter_by(id=author_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedAuthor.name = request.form['name']

        session.add(editedAuthor)
        session.commit()
        flash("Author Edited")
        return redirect(url_for('showAuthor', author_id=author_id))

    else:
        return render_template('edit_author.html', author=editedAuthor)


def authorCheck(author_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    author_id = None
    authors = session.query(Authors).all()
    for a in authors:
        print a.name
        print request.form['author']
        if a.name == request.form['author']:
            author_id = a.id
            break
    if author_id:
        return author_id
    else:
        newAuthor = Authors(name=author_name, book_count=1)
        session.add(newAuthor)
        session.flush()
        author_id = newAuthor.id
        session.commit()
        return author_id


def genreCheck(genre_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    genre_id = None
    genres = session.query(Genres).all()
    for g in genres:
        if g.name == request.form['genre']:
            genre_id = g.id
            break
    if genre_id:
        return genre_id
    else:
        newGenre = Genres(name=genre_name)
        session.add(newGenre)
        session.flush()
        genre_id = newGenre.id
        session.commit()
        return genre_id


@app.route('/books/add', methods=['GET', 'POST'])
def addBook():
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        author_id = authorCheck(request.form['author'])
        genre_id = genreCheck(request.form['genre'])

        newBook = Books(title=request.form['title'], genre_id=genre_id, summary=request.form['summary'], author_id=author_id)
        session.add(newBook)
        session.commit()
        flash("New Book Added")
        return redirect(url_for('showBookList'))
    else:
        return render_template('add_book.html')


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedBook = session.query(Books).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedBook.title = request.form['title']
        if request.form['author']:
            author_id = authorCheck(request.form['author'])
            editedBook.author_id = author_id
        if request.form['genre']:
            genre_id = genreCheck(request.form['genre'])
            editedBook.genre_id = genre_id
        if request.form['summary']:
            editedBook.summary = request.form['summary']

        session.add(editedBook)
        session.commit()
        flash("Book Edited")
        return redirect(url_for('showBook', book_id=book_id))
    else:
        return render_template('edit_book.html', book=editedBook)


@app.route('/books/<int:book_id>/delete', methods=['GET', 'POST']) #add id see example
def deleteBook(book_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id=book_id).one()
    #patron = session.query(Patrons).filter_by(id=book.patron_id).one()
    if request.method == 'POST':
        if book.patron_id:
            print "This book must first be returned to the library."
            return render_template('delete_book.html', book=book)
        else:
            author = session.query(Authors).filter_by(id=book.author_id).one()
            author.book_count = author.book_count - 1;
            session.add(author)
            session.flush()
            if author.book_count == 0:
                print
                session.delete(author)
                session.commit()

            session.delete(book)
            session.commit()
            flash("Book Deleted")
            return redirect(url_for('showBookList'))
    else:
        return render_template('delete_book.html', book=book)


@app.route('/checked_out')
def showCheckedOutBooks():
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    query = select([Books.id, Books.title, Books.patron_id, Patrons.name,]).where(Books.patron_id == Patrons.id)
    books = session.execute(query)

    return render_template('checked_out.html',books=books)
    session.commit()


def serializeInternal(self):
    return {
        'id': self.id,
        'title': self.title,
        'patron_id': self.patron_id,
        'name': self.name
    }


@app.route('/checked_out/JSON')
def checkedOutBooksJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    query = select([Books.id, Books.title, Books.patron_id, Patrons.name,]).where(Books.patron_id == Patrons.id)
    books = session.execute(query)

    return jsonify(Book=[serializeInternal(b) for b in books])
    session.commit()


@app.route('/books/<int:book_id>/checkout', methods=['GET', 'POST'])
def checkOutBook(book_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id=book_id).one()
    patrons = session.query(Patrons).all()
    if book.patron_id:
        error_message = 'Sorry this book is already checked out.'
        return render_template('error.html', error_message=error_message)
    if request.method == 'POST':
        book.patron_id = request.form['patrons_drop_down']
        session.add(book)
        session.commit()
        flash("Book Checked Out")
        return redirect(url_for('showBook', book_id=book_id))

    else:
        return render_template('check_out_book.html', book=book, patrons=patrons)


@app.route('/books/<int:book_id>/return', methods=['GET', 'POST'])
def returnBook(book_id):
    if loginCheck():
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    book = session.query(Books).filter_by(id=book_id).one()
    patron = None
    if book.patron_id == None:
        error_message = 'This book is not checked out yet and cannot be returned.'
        return render_template('error.html', error_message=error_message)
    else:
        patron = session.query(Patrons).filter_by(id=book.patron_id).one()
    if request.method == 'POST':
        book.patron_id = None
        session.add(book)
        session.commit()
        flash("Book Returned")
        return redirect(url_for('showBook', book_id=book_id))
    else:
        return render_template('return_book.html', book=book, patron=patron)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
