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
# Then I set the monster attributes for this fight
# Finally, I return the command_available_fight function so the player can have the option to attack during the fight
def initiate_fight(monster_name):
    global current_monster
    if monster_name == "Goomba":
        set_monster_stat(15, 3, monster_name)
    elif monster_name == "Castle Guard":
        set_monster_stat(70, 5, monster_name)
    elif monster_name == "Bowser":
        set_monster_stat(100, 8, monster_name)

    return command_available_fight()


# This function provides available commands to the player during a fight (currently only the attack option)
# I also return the monster's current health and attack power for display
def command_available_fight():
    monster_health = get_monster_health()
    monster_attack_power = get_monster_attack_power()
    return f"Monster Health: {monster_health}\nMonster Attack: {monster_attack_power}\n\nCombat Action: Attack"


# This function retrieves the monster's current health and returns it
# This value is updated during the fight as the player attacks
def get_monster_health():
    return monster_health


# This function retrieves the monster's current attack power and returns it
# The attack power is used when the monster attacks the player
def get_monster_attack_power():
    return monster_attack_power


# I use this function to set the monster's health and attack power when a fight starts
# It also sets the current monster being fought and resets the monster's defeated status to False for a fresh battle
def set_monster_stat(health, attack_power, monster_name):
    global monster_health, monster_attack_power, current_monster
    monster_health = health
    monster_attack_power = attack_power
    current_monster = monster_name  # Track the current monster being fought
    monster_defeated_status[monster_name] = (
        False  # Reset defeated status for the current monster
    )


# This function calculates the damage the player deals to the monster in an attack
# The damage is a random number based on the player's attack power, with a slight variation for realism
# After the attack, the monster's health is reduced by the damage amount
def player_attack():
    global monster_health

    attack_power = status.get_attack_power()
    damage = RND.randint(attack_power - 2, attack_power + 2)
    monster_health -= damage
    if monster_health < 0:
        monster_health = 0
    return f"You attack the monster, dealing {damage} damage."


# This function handles the monster attacking the player
# The damage is calculated as a random number based on the monster's attack power
# The player's health is reduced by the damage amount after the attack
def monster_attack():
    damage = RND.randint(monster_attack_power - 2, monster_attack_power + 2)
    status.decrease_health(damage)
    return f"The monster attacks you, dealing {damage} damage."


# This function manages the entire fight process
# It includes player attacks, checks if the monster is defeated, and handles the monster's attack
# If the monster is Bowser and is defeated, the player is moved to the game_over location
# Otherwise, the fight continues until either the player or the monster is defeated
def fight():
    global monster_defeated_status

    player_result = player_attack()
    if monster_health <= 0:
        monster_defeated_status[current_monster] = (
            True  # Mark the current monster as defeated
        )

        # Check if Bowser is the defeated monster
        if current_monster == "Bowser":
            return parser.move_to("game_over") + "\nThe monster is defeated! You win!"
        else:
            return player_result + f"\nThe {current_monster} is defeated!"

    monster_result = monster_attack()
    if status.get_health() <= 0:
        return (
            player_result
            + "\n"
            + monster_result
            + "\nYou have been defeated. Game over!"
        )

    return (
        f"Your Health: {status.get_health()}/100 \n"
        f"Monster Health: {get_monster_health()} \n\n"
        f"{player_result}\n{monster_result}\n\n"
        "Actions: Attack or Inventory"
    )


# This function checks if a specific monster has been defeated
# It returns True if the monster is defeated and False otherwise
def is_monster_defeated(monster_name):
    return monster_defeated_status.get(monster_name, False)
