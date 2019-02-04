import os
import secrets
import json, pandas, random, requests
from flask import render_template, url_for, flash, redirect, request
from myapp import app, db, bcrypt
from myapp.forms import RegisterForm, LoginForm
from myapp.models import User, Movies
from flask_login import login_user, current_user, logout_user, login_required

filename ='myapp/idList/links.csv'
API_key = '1446dc92'


#metoda koja slucajnim odabirom bira id iz fajla koji sadrzi imdbID,
#api ne dopusta direktno povlacenje popisa svih id-a pa je ovo bio jedini nacin
def selectId():
    colnames=["movieId","imdbId","tmdbId"]
    data = pandas.read_csv(filename, names=colnames)
    movieid = data.imdbId.tolist()
    chosen_id = random.choice(movieid)
    chosen_id.replace(" ", "")
    return chosen_id

#glavna ili home ruta generia api request na refresh ili na search upit
@app.route('/', methods=['GET', 'POST'])
def root():
    IMDB_ID = selectId()
    input = request.form.get('tag')
    if not input:
        API_link = "https://www.omdbapi.com/?i=tt"+IMDB_ID+"&apikey="+API_key

    else:
        API_link = "https://www.omdbapi.com/?t="+input+"&apikey="+API_key

    API_link.replace(" ", "")
    resp = requests.get(API_link)
    movie = resp.json()


    return render_template('home.html',title='Home', mov = movie)



#dodaje fil iz root rute u bazu na klik botuna
@app.route('/<mov_id>',methods=['GET','POST'])
def add_mov(mov_id):
    if current_user.is_authenticated:
        movid = mov_id[2:]
        movlink = "https://www.omdbapi.com/?i=tt"+movid+"&apikey="+API_key
        mov = Movies(IMDB_link=movlink, user_id=current_user.id)

        db.session.add(mov)
        db.session.commit()
        flash('Movie added to favorites', 'sucess')
        return redirect(url_for('user'))

#ruta za registraciju korisnika koja dodaje korisnika u bazu i redirekta korisnika na login.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)


#ruta koja logira korinika iz baze
@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('root'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login',form=form)

#ruta koja odlogira korisnika i redirecta na pocetnu stranu
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root'))


#ruta koja prekazuje korisnicku stranu sa sacuvanim filmovima
@app.route('/user',methods=['GET', 'POST'])
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



#brize filmove iz baze na klik
@app.route('/user/<mov_id>',methods=['GET','POST'])
def delete_mov(mov_id):
    if current_user.is_authenticated:
        movid = mov_id[2:]
        movlink = "https://www.omdbapi.com/?i=tt"+movid+"&apikey="+API_key
        mov= Movies.query.get_or_404(movlink)
        db.session.delete(mov)
        db.session.commit()
        flash('Movie removed from favorites', 'sucess')
        return redirect(url_for('user'))
