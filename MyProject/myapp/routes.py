import os
import secrets
import json
import pandas
import random
import requests
from flask import render_template, url_for, flash, redirect, request
from myapp import app, db, bcrypt
from myapp.forms import RegisterForm, LoginForm
from myapp.models import User, Movies
from flask_login import login_user, current_user, logout_user, login_required

fileName = 'myapp/idList/links.csv'
API_key = '1446dc92'

tmpData = (
    {"Search": [{"Title": "Batman: The Killing Joke", "Year": "2016", "imdbID": "tt4853102", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BMTdjZTliODYtNWExMi00NjQ1LWIzN2MtN2Q5NTg5NTk3NzliL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Batman: The Dark Knight Returns, Part 2", "Year": "2013", "imdbID": "tt2166834", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BYTEzMmE0ZDYtYWNmYi00ZWM4LWJjOTUtYTE0ZmQyYWM3ZjA0XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg"}, {"Title": "Batman: Mask of the Phantasm", "Year": "1993", "imdbID": "tt0106364", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BODE0YTBiMjQtNWQyZC00YTNjLWJmYjAtMWUwNzI4NGVlZTAzL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Batman: Year One", "Year": "2011", "imdbID": "tt1672723", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BNTJjMmVkZjctNjNjMS00ZmI2LTlmYWEtOWNiYmQxYjY0YWVhXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Batman: The Movie", "Year": "1966", "imdbID": "tt0060153", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BODVjNjdlYTQtMWIwYy00MWIyLWI2ZmMtZWFhMTdjNjAzNGVlXkEyXkFqcGdeQXVyNTAyNDQ2NjI@._V1_SX300.jpg"},
                {"Title": "Batman: Assault on Arkham", "Year": "2014", "imdbID": "tt3139086", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BZDU1ZGRiY2YtYmZjMi00ZDQwLWJjMWMtNzUwNDMwYjQ4ZTVhXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Batman: Gotham Knight", "Year": "2008", "imdbID": "tt1117563", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BM2I0YTFjOTUtMWYzNC00ZTgyLTk2NWEtMmE3N2VlYjEwN2JlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Superman/Batman: Apocalypse", "Year": "2010", "imdbID": "tt1673430", "Type": "movie", "Poster": "https://m.media-amazon.com/images/M/MV5BMjk3ODhmNjgtZjllOC00ZWZjLTkwYzQtNzc1Y2ZhMjY2ODE0XkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SX300.jpg"}, {"Title": "Batman Beyond", "Year": "1999–2001", "imdbID": "tt0147746", "Type": "series", "Poster": "https://m.media-amazon.com/images/M/MV5BYTBiZjFlZDQtZjc1MS00YzllLWE5ZTQtMmM5OTkyNjZjMWI3XkEyXkFqcGdeQXVyMTA1OTEwNjE@._V1_SX300.jpg"}, {"Title": "Batman: Arkham City", "Year": "2011", "imdbID": "tt1568322", "Type": "game", "Poster": "https://images-na.ssl-images-amazon.com/images/M/MV5BOGY2NDY5NjEtNjljNy00NGU4LTljMzQtNTgxMWYxNzI5YjlhXkEyXkFqcGdeQXVyNDQwODY1NTY@._V1_SX300.jpg"}], "totalResults": "355", "Response": "True"}
)
# metoda koja slucajnim odabirom bira id iz fajla koji sadrzi imdbID,
# api ne dopusta direktno povlacenje popisa svih id-a pa je ovo bio jedini nacin
def selectId():
    colnames = ["movieId", "imdbId", "tmdbId"]
    data = pandas.read_csv(fileName, names=colnames)
    movieId = data.imdbId.tolist()
    chosen_Id = random.choice(movieId)
    chosen_Id.replace(" ", "")
    return chosen_Id

# glavna ili home ruta generia api request na refresh
@app.route('/', methods=['GET', 'POST'])
def root():
    IMDB_ID = selectId()
    API_link = "https://www.omdbapi.com/?i=tt"+IMDB_ID+"&apikey="+API_key
    API_link.replace(" ", "")
    resp = requests.get(API_link)
    movie = resp.json()
    return render_template('home.html', title='Home', mov=movie)

# ruta koja prekazuje tocno odabran film
@app.route('/<id>')
def display(id):
    movid = id[2:]
    API_link = "https://www.omdbapi.com/?i=tt"+movid+"&apikey="+API_key
    API_link.replace(" ", "")
    resp = requests.get(API_link)
    movie = resp.json()
    return render_template('home.html', title='Home', mov=movie)

# ruta koja upravlja search rezultatima
@app.route('/search', methods=['GET', 'POST'])
def search():
    br = 1
    input = request.form['tag']
    print(input)
    API_link = "https://www.omdbapi.com/?s="+input+"&page="+str(br)+"&apikey="+API_key
    API_link.replace(" ", "")
    resp = requests.get(API_link)
    movie = resp.json()
    brStr = round(int(movie.get('totalResults'))/9)
   

    return render_template('search.html', title='Search', mov=movie, br=br, input=input, brStr=brStr)

# ruta koja upravlja odabirom stranica
@app.route('/search/<input>/<br>', methods=['POST'])
def selectPage(input, br):
    if request.method == 'POST':
        next = request.form['button'] == 'Next'
        back = request.form['button'] == 'Back'
        print(next)
        print(back)
        if next:
            print(input)
            print(br)
            input = input
            br = int(br)+1
            API_link = "https://www.omdbapi.com/?s="+input+"&page="+str(br)+"&apikey="+API_key
            API_link.replace(" ", "")
            resp = requests.get(API_link)
            movie = resp.json()
            brStr = round(int(movie.get('totalResults'))/9)
            return render_template('search.html', title='Search', mov=movie, br=br, input=input, brStr=brStr)
        if back and int(br) > 1:
            print(input)
            print(br)
            input = input
            br = int(br)-1
            API_link = "https://www.omdbapi.com/?s="+input+"&page="+str(br)+"&apikey="+API_key
            API_link.replace(" ", "")
            resp = requests.get(API_link)
            movie = resp.json()
            brStr = round(int(movie.get('totalResults'))/9)

            return render_template('search.html', title='Search', mov=movie, br=br, input=input, brStr=brStr)
        else:
            input = input
            br = 1
            API_link = "https://www.omdbapi.com/?s="+input+"&page="+str(br)+"&apikey="+API_key
            API_link.replace(" ", "")
            resp = requests.get(API_link)
            movie = resp.json()
            brStr = round(int(movie.get('totalResults'))/9)
            
            return render_template('search.html', title='Search', mov=movie, br=1, input=input, brStr=brStr)

# dodaje fil iz root rute u bazu na klik botuna
@app.route('/<mov_id>', methods=['GET', 'POST'])
def add_mov(mov_id):
    if current_user.is_authenticated:
        movid = mov_id[2:]
        movlink = "https://www.omdbapi.com/?i=tt"+movid+"&apikey="+API_key
        mov = Movies(IMDB_link=movlink, user_id=current_user.id)

        db.session.add(mov)
        db.session.commit()
        flash('Movie added to favorites', 'sucess')
        return redirect(url_for('user'))

# ruta za registraciju korisnika koja dodaje korisnika u bazu i redirekta korisnika na login.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# ruta koja logira korinika iz baze
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('root'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

# ruta koja odlogira korisnika i redirecta na pocetnu stranu
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root'))


# ruta koja prekazuje korisnicku stranu sa sacuvanim filmovima
@app.route('/user', methods=['GET', 'POST'])
def user():
    if current_user.is_authenticated:
        mov = Movies.query.filter_by(user_id=current_user.id)
        saved_movies = []

        for m in mov:
            link = m.IMDB_link
            link.replace(" ", "")
            re = requests.get(link)
            m = re.json()
            saved_movies.append(m)

        print(saved_movies)
    return render_template('userPage.html', title='User', mov=saved_movies)


# brize filmove iz baze na klik
@app.route('/user/<mov_id>', methods=['GET', 'POST'])
def delete_mov(mov_id):
    if current_user.is_authenticated:
        movid = mov_id[2:]
        movlink = "https://www.omdbapi.com/?i=tt"+movid+"&apikey="+API_key
        mov = Movies.query.get_or_404(movlink)
        db.session.delete(mov)
        db.session.commit()
        flash('Movie removed from favorites', 'sucess')
        return redirect(url_for('user'))
