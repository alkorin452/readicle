from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, BookForm, EditBookForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    # books=Book.query.all()
    books = Book.query.filter_by(on_shelf=True).all()
    books.reverse()
    return render_template('index.html', title='Home', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Registers user with information from registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Add a new Book to a specific shelf
@app.route('/addBook/<shelf>', methods=['GET', 'POST'])
@login_required
def addBook(shelf):
    form = BookForm()
    if form.validate_on_submit():
        if shelf == "wishlist":
            book = Book(title=form.title.data, author=form.author.data, genre=form.genre.data, format=form.format.data, poster_id=current_user.id, on_shelf=False)
        else:
            book = Book(title=form.title.data, author=form.author.data, genre=form.genre.data, format=form.format.data, poster_id=current_user.id,on_shelf=True)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addBook.html', title='Add Book', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


# General edit that allows logged in users to edit specific books
@app.route('/edit/<shelfType>', methods=['GET', 'POST'])
# @app.route('/edit')
@login_required
def edit(shelfType):
    if shelfType == 'wishlist':
        books = Book.query.filter_by(on_shelf=False).all()
    elif shelfType == 'index':
        books = Book.query.filter_by(on_shelf=True).all()
    books.reverse()
    return render_template('edit.html', title='Edit', books=books)


# This method is used to edit specific books
@app.route('/edit/<int:bookID>', methods=['GET', 'POST'])
@login_required
def editBook(bookID):
    form = EditBookForm()
    current_book = Book.query.get(bookID)

    # If the form is valid it changes the book data and commits
    if form.validate_on_submit():
        current_book.title = form.title.data
        current_book.author = form.author.data
        current_book.genre = form.genre.data
        current_book.format = form.format.data
        db.session.commit()
        flash('Changes have been saved')
        return redirect(url_for('index'))
    # This fills the form with the book's data
    elif request.method == 'GET':
        form.title.data = current_book.title
        form.author.data = current_book.author
        form.genre.data = current_book.genre
        form.format.data = current_book.format
    return render_template('editBook.html', title='Edit', form=form, current_book=current_book)


@app.route('/delete/<shelfType>/<int:bookID>', methods=['GET', 'POST'])
@login_required
def deleteBook(shelfType, bookID):
    current_book = Book.query.get(bookID)
    if current_user.is_authenticated:
        db.session.delete(current_book)
        db.session.commit()
    if shelfType == 'wishlist':
        books = Book.query.filter_by(on_shelf=False).all()
    else:
        books = Book.query.filter_by(on_shelf=True).all()
    books.reverse()
    return render_template('edit.html', title='Edit', books=books)


@app.route('/wishlist/<int:userID>')
@login_required
def wishlist(userID):
    print(request.script_root)
    print(current_user.id)
    books = Book.query.filter_by(on_shelf=False, poster_id=userID).all()
    books.reverse()
    return render_template('index.html', title='Home', books=books)

# Changes the Book.on_shelf to True
@app.route('/moveToShelf/<int:bookID>')
@login_required
def moveToShelf(bookID):
    current_book = Book.query.get(bookID)
    current_book.on_shelf = True
    db.session.commit()
    flash('Moved to your shelf')
    return redirect(url_for('index'))


@app.route('/shelf/<int:userID>')
@login_required
def shelf(userID):
    books = Book.query.filter_by(on_shelf=True, poster_id=userID).all()
    books.reverse()
    return render_template('index.html', title='Home', books=books)

