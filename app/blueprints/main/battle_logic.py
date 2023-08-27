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

def execute_battle_step(user_team, enemy_team, current_step, max_moves=10):
    # Check if the battle has reached the maximum number of moves
    if current_step >= max_moves:
        # Determine the winner based on the state of the battle after max_moves
        user_hp = sum(pokemon.hp for pokemon in user_team)
        enemy_hp = sum(pokemon.hp for pokemon in enemy_team)

        if user_hp > enemy_hp:
            return "user", []
        elif enemy_hp > user_hp:
            return "enemy", []
        else:
            return "draw", []

    # Simulate one step of the battle
    messages = []
    user_team_defeated = all(pokemon.hp <= 0 for pokemon in user_team)
    enemy_team_defeated = all(pokemon.hp <= 0 for pokemon in enemy_team)

    if user_team_defeated and enemy_team_defeated:
        return "draw", messages
    elif user_team_defeated:
        return "enemy", messages
    elif enemy_team_defeated:
        return "user", messages

    for user_pokemon, enemy_pokemon in zip(user_team, enemy_team):
        user_damage = calculate_damage(user_pokemon, enemy_pokemon)
        enemy_damage = calculate_damage(enemy_pokemon, user_pokemon)

        if user_damage > 0:
            enemy_pokemon.hp -= user_damage
            if enemy_pokemon.hp <= 0:
                enemy_pokemon.hp = 0
            messages.append(f"{user_pokemon.name} dealt {user_damage} damage to {enemy_pokemon.name}")

        if enemy_damage > 0:
            user_pokemon.hp -= enemy_damage
            if user_pokemon.hp <= 0:
                user_pokemon.hp = 0
            messages.append(f"{enemy_pokemon.name} dealt {enemy_damage} damage to {user_pokemon.name}")

    return None, messages