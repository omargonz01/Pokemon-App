from flask import request, render_template
import requests
from app import app
from .forms import PokemaneForm, SignupForm, LoginForm

@app.route("/")
@app.route("/home")
def home():
    return 'Hello User, Glad You Could Join Us'

# temp database to test
TEST_USERS = {
    'sk8andthra5h@gmail.com': {
        'name': 'OG',
        'password': 'killawhale1'
    }
}

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = f'{form.first_name.data} {form.last_name.data}'
        email = form.email.data
        password = form.password.data
        TEST_USERS[email] = {
            'name': name,
            'password': password
        }
        return f'Thanks for testing {name}, we see you!'
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in TEST_USERS and password == TEST_USERS[email]['password']:
            return f'Hello, {TEST_USERS[email]["name"]}, thanks for coming back!'
        else:
            return 'Invalid email or password, try again playa'
    else:
        print('not valid, try again')
        return render_template('login.html', form=form)

@app.route("/pokemon", methods=['GET', 'POST'])
def get_pokemanes():
    form = PokemaneForm()
    pokemon_names = []
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_names = form.pokemane.data
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

