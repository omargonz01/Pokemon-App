from flask import request, render_template, flash, redirect, url_for 
import requests
from app import app
from .forms import PokemaneForm, SignupForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, db
from werkzeug.security import check_password_hash

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# HTTP Methods & Rendering Template
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabs out sign up form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        
        # creates an instance of the User Model
        new_user = User(first_name, last_name, email, password)

        # adds new user to database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {new_user.first_name}! :)', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        # query the user onject from database
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello {queried_user.first_name}, thanks for coming back! :)', 'success')
            return redirect(url_for('home'))

        else:
            flash('Invalid email or password, try again playa', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    # checks if user is athenticated in order to flash his name when he clicks logout
    user_first_name = current_user.first_name if current_user.is_authenticated else "User"
    logout_user()
    flash(f"Thanks for coming, {user_first_name}! See ya next time!.", "primary")
    return redirect(url_for('home'))

@app.route("/pokemon", methods=['GET', 'POST'])
@login_required
def get_pokemanes():
    form = PokemaneForm()
    pokemon_names = []
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_names = form.pokemane.data.lower()
        print(pokemon_names)

        url = "https://pokeapi.co/api/v2/pokemon/"
    

        response = requests.get(url + pokemon_names)
        if response.ok:

            data = response.json()
            name = data["name"]
            ability_name = data["abilities"][0]["ability"]["name"]
            base_experience = data["base_experience"]
            sprite_url = data["sprites"]["front_shiny"]
            atack_base_stat = data["stats"][1]["base_stat"]
            hp_base_stat = data["stats"][0]["base_stat"]
            defense_base_stat = data["stats"][2]["base_stat"]

            pokemanes_dict = {
                "name": name,
                "ability_name": ability_name,
                "base_experience": base_experience,
                "sprite_url": sprite_url,
                "atack_base_stat": atack_base_stat,
                "hp_base_stat": hp_base_stat,
                "defense_base_stat": defense_base_stat
            }
            return render_template("pokemon.html", pokemanes_dict=pokemanes_dict, form=form)
            
        else:
            return render_template("pokemon.html", form=form)
        
    return render_template("pokemon.html", form=form)

