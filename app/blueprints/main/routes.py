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
        pokemon = Pokemon.query.filter_by(name=pokemon_names).first()

        if pokemon:
            # If the Pokémon is found in the database, extract its data and render template
            pokemanes_dict = {
                "name": pokemon.name,
                "ability_name": pokemon.ability_name,
                "base_experience": pokemon.base_experience,
                "sprite_url": pokemon.sprite_url,
                "attack_base_stat": pokemon.attack_base_stat,
                "hp_base_stat": pokemon.hp_base_stat,
                "defense_base_stat": pokemon.defense_base_stat
            }
            return render_template("pokemon.html", pokemanes_dict=pokemanes_dict, form=form)
        else:
            url = "https://pokeapi.co/api/v2/pokemon/"
            response = requests.get(url + pokemon_names)
            
            if response.ok:
                data = response.json()
                # Extract Pokémon data from the API response
                name = data["name"]
                ability_name = data["abilities"][0]["ability"]["name"]
                base_experience = data["base_experience"]
                sprite_url = data["sprites"]["front_shiny"]
                attack_base_stat = data["stats"][1]["base_stat"]
                hp_base_stat = data["stats"][0]["base_stat"]
                defense_base_stat = data["stats"][2]["base_stat"]
                
                pokemanes_dict = {
                    "name": name,
                    "ability_name": ability_name,
                    "base_experience": base_experience,
                    "sprite_url": sprite_url,
                    "attack_base_stat": attack_base_stat,
                    "hp_base_stat": hp_base_stat,
                    "defense_base_stat": defense_base_stat
                }
                
                # Creating an instance of the Pokemon Model
                new_pokemon = Pokemon(
                    name=name,
                    sprite_url=sprite_url,
                    attack_base_stat=attack_base_stat,
                    hp_base_stat=hp_base_stat,
                    defense_base_stat=defense_base_stat,
                    ability_name=ability_name,
                    base_experience = base_experience,
                    user_id=current_user.id
                )
                
                # Adding new pokemon to our database
                db.session.add(new_pokemon)
                db.session.commit()
                
                return render_template("pokemon.html", pokemanes_dict=pokemanes_dict, form=form)
            else:
                return render_template("pokemon.html", form=form)
    
    return render_template("pokemon.html", form=form)


@main.route("/catch_pokemon/<pokemon_name>", methods=['GET', 'POST'])
@login_required
def catch_pokemon(pokemon_name):
    form = PokemaneForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our PokemaneForm data
        name = form.name.data 
        ability_name = form.ability_name.data
        sprite_url = form.sprite_url.data
        attack_base_stat = form.attack_base_stat.data
        hp_base_stat = form.hp_base_stat.data
        defense_base_stat = form.defense_base_stat.data
        base_experience = form.base_experience
        
        user_id = current_user.id
        
        # Creating an instance of the Pokemon Model
        new_pokemon = Pokemon(name, sprite_url, attack_base_stat, base_experience, hp_base_stat, defense_base_stat, ability_name)

        # Adding new pokemon to our database
        db.session.add(new_pokemon)
        db.session.commit()

        flash(f"You caught {new_pokemon}!", "success")
        return redirect(url_for('main.home'))
    else:
        return render_template('pokemon.html', form=form)         