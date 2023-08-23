from . import main
from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
import requests 
from ..auth.forms import PokemaneForm
from app.models import Pokemon, teams, db


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/pokemon", methods=['GET', 'POST'])
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

@main.route("/catch_pokemon/<pokemon_name>", methods=['GET', 'POST'])
@login_required
def catch_pokemon():
    form = PokemaneForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our PokemaneForm data
        name = form.name.data 
        ability_name = form.ability_name.data
        sprite_url = form.sprite_url.data
        attack_base_stat = form.attack_base_stat.data
        hp_base_stat = form.hp_base_stat.data
        defense_base_stat = form.defense_base_stat.data
        
        user_id = current_user.id
        
        # Creating an instance of the Post Model
        new_pokemon = Pokemon(name, sprite_url, attack_base_stat, hp_base_stat, defense_base_stat, ability_name, user_id)

        # Adding new post to our database
        db.session.add(new_pokemon)
        db.session.commit()

        flash(f"You caught {new_pokemon}!", "success")
        return redirect(url_for('main.home'))
    else:
        return render_template('create_post.html', form=form)         