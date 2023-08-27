import random

class Pokemon_battle:
    def __init__(self, name, hp, attack, defense, sprite_url):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite_url = sprite_url

def calculate_damage(attacker, defender):
    damage = max(0, attacker.attack - defender.defense)
    return damage

def execute_battle(user_team, enemy_team):
    while user_team and enemy_team:
        for user_pokemon, enemy_pokemon in zip(user_team, enemy_team):
            user_damage = calculate_damage(user_pokemon, enemy_pokemon)
            enemy_damage = calculate_damage(enemy_pokemon, user_pokemon)

            if user_damage > 0:
                enemy_pokemon.hp -= user_damage
                if enemy_pokemon.hp <= 0:
                    enemy_team.remove(enemy_pokemon)

            if enemy_damage > 0:
                user_pokemon.hp -= enemy_damage
                if user_pokemon.hp <= 0:
                    user_team.remove(user_pokemon)

        if not user_team:
            return "enemy"
        elif not enemy_team:
            return "user"
    return None