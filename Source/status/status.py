# Global variables
player_health = 100
attack_power = 10


# Health management
# to track the player health and update it during fights and when using a potion
def get_health():
    return player_health


def update_health(amount):
    global player_health
    player_health = max(0, min(100, player_health + amount))
    return f"Health updated: {player_health}"


# Attack power management
# to track the player's attack power and update it when the player receives a sword
# Also used to display the player's attack power in the gui
def get_attack_power():
    return attack_power


# Here I increase the player's attack power when they receive a sword
# The += operator is used to add the amount to the current attack power
def increase_attack(amount):
    global attack_power
    attack_power += amount
    return f"Attack power increased by {amount}! Current attack power: {attack_power}"


# i use this to display all the player's current stats in the gui
# i didnt have time to add more depth with a defense system in my game like defend and a def stat and armor
def player_current_status():
    return f"Health: {get_health()} | Attack Power: {get_attack_power()}"


# Test the status module
if __name__ == "__main__":
    print("Status Module Test")
    print(increase_attack(5))
    print(update_health(-30))
