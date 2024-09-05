import random as RND  # I import the random module to generate random numbers for damage in fight
import status.status as status
import command_parser.command_parser as parser

# Global variables
monster_health = 0
monster_attack_power = 0
current_monster = ""

# Dictionary to track which monsters have been defeated
# key = monster name, value = defeated (True/False)
monster_defeated_status = {
    "Goomba": False,
    "Castle Guard": False,
    "Bowser": False,
}


# health and attack power for Goomba in the blacksmith basement, Castle Guard in the castle, and Bowser in the final boss room
# The first number is the health, and the second number is the attack power
# I check which monster is being initiated for a fight
# Then i set the monster attributes for this fight
# Finally, i return the command_available_fight function so the player can have the option to attack during the fight
def initiate_fight(monster_name):
    global current_monster
    if monster_name == "Goomba":
        set_monster_stat(15, 3, monster_name)
    elif monster_name == "Castle Guard":
        set_monster_stat(70, 5, monster_name)
    elif monster_name == "Bowser":
        set_monster_stat(100, 8, monster_name)
    return command_available_fight()


# Available commands to the player during a fight
# (currently only the attack option)
# I also return the monster's current health and attack power for display
def command_available_fight():
    monster_health = get_monster_health()
    monster_attack_power = get_monster_attack_power()
    return f"Monster Health: {monster_health}\nMonster Attack: {monster_attack_power}\n\nCombat Action: Attack"


# This value is updated during the fight as the player attacks
def get_monster_health():
    return monster_health


# The attack power is used when the monster attacks the player
def get_monster_attack_power():
    return monster_attack_power


# I use this function to set the monster's health and attack power for the current fight
def set_monster_stat(health, attack_power, monster_name):
    global monster_health, monster_attack_power, current_monster
    monster_health = health
    monster_attack_power = attack_power
    current_monster = monster_name
    monster_defeated_status[monster_name] = False


# Player attack monster
# The damage is random based on the player's attack power
# After the attack, the monster's health is reduced by the damage amount
def player_attack():
    global monster_health
    attack_power = status.get_attack_power()
    damage = RND.randint(attack_power - 2, attack_power + 2)
    monster_health -= damage
    if monster_health < 0:
        monster_health = 0
    return f"You attack the monster, dealing {damage} damage."


# Monster attacking the player
# The damage is calculated as a random number based on the monster's attack power
# The player's health is reduced by the damage amount after the attack
# the -2 and +2 is to add some randomness to the damage dealt by the monster
# randint is used to generate a random number between the two numbers
# (in my game the monster can deal between 2 less or 2 more damage than its base attack power)
def monster_attack():
    damage = RND.randint(monster_attack_power - 2, monster_attack_power + 2)
    status.update_health(-damage)
    return f"The monster attacks you, dealing {damage} damage."


# Entire fight process
# Player attacks, checks if the monster is defeated, and handles the monster's attack
# If the monster is Bowser and is defeated, the player is moved to the game_over location
# Otherwise, the fight continues until either the player or the monster is defeated
def fight():
    global monster_defeated_status

    player_result = player_attack()
    if monster_health <= 0:
        monster_defeated_status[current_monster] = (
            True  # Update monster defeated status
        )
        # Check if Bowser is the defeated monster to end the game
        if current_monster == "Bowser":
            return parser.move_to("game_over") + "\nThe monster is defeated! You win!"
        else:
            return player_result + f"\nThe {current_monster} is defeated!"

    monster_result = monster_attack()
    if status.get_health() <= 0:
        return player_result + "\n" + monster_result + "\nYou died. Game over!"
    return (
        f"Your Health: {status.get_health()}/100 \n"
        f"Monster Health: {get_monster_health()} \n\n"
        f"{player_result}\n{monster_result}\n\n"
        "Actions: Attack or Inventory"
    )


# Checks if a specific monster has been defeated
# True if the monster is defeated , False otherwise
def is_monster_defeated(monster_name):
    return monster_defeated_status.get(monster_name, False)


# Testing the fight module against a Goomba
if __name__ == "__main__":
    print("Monster Fight module")
    initiate_fight("Goomba")
    print(fight())
