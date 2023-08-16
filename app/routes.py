from flask import request, render_template
import requests
from app import app
from .forms import PokemaneForm

@app.route("/")
@app.route("/home")
def home():
    return 'Hello User, Glad You Could Join Us'

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

