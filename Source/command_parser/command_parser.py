import inventory.inventory as inventory
import status.status as status
import monster_fight.monster_fight as monster_fight


# my initial state before starting the game (global variables) They are all set to false and then will be updated later.
current_location = "blacksmith_basement"  # i set up the starting location of the player this way because it is very useful for testing specific location's functionalities.
talked_to_prisoner = False
cleaned_basement = False
guard_defeated = False
key_picked = False


# I used a nested dictionary to store the places and their available actions.
# a nested dictionary is a dictionary within a dictionary. And a dictionary is made of a key and a value.
# the key is the location and the value is another dictionary.
# in the other dictionary, the key is the story, actions and image, and
# the value is the story of the location, the actions available for the specific location, and the image of the location.
# i use lambda to defer the action function because i was having recursion problems without it.
location = {
    "kitchen": {
        "Story": "You are just working hard as usual fixing a kitchen sink drain.",
        "Next": lambda: move_to("drain"),  # action to move to the next location "drain"
        "Inventory": lambda: inventory.manage_inventory(),  # lambda makes it so the actions are deferred until they are called.
        "Image": "images/kitchen.png",
    },
    "drain": {
        "Story": "You hear a strange noise and suddenly you are being sucked down the drain.",
        "Resist": lambda: move_to("mario_world"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/drain.png",
    },
    "mario_world": {
        "Story": "You appear in a 3D world. It is raining heavily and you are in front of a giant monster.",
        "Next": lambda: move_to("kidnapping"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/mario_world.png",
    },
    "kidnapping": {
        "Story": "The monster is scaring you and he is holding hostage a pretty princess!",
        "Run away": lambda: move_to("town_gate"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/kidnapping.png",
    },
    "town_gate": {
        "Story": "You found a town. Maybe you could hide or find more information on what is happening.",
        "Enter town": lambda: move_to("town_center"),
        "Go to castle": lambda: (
            move_to("castle_entrance")
            if not talked_to_prisoner  # if you have not talked to the prisoner, you can only go to the castle entrance and have to defeat the guard (additional difficulty)
            else move_to(
                "east_wall"
            )  # if you have talked to the prisoner, you can go to the castle east wall
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/town_gate.png",
    },  # the town center is where everything other NPC and places are located. Flow example: When you go to the blacksmith, you need to come back to town center to go to another NPC/location.
    "town_center": {
        "Story": "You are at the center of the town. You can go anywhere from here to further your investigation or hide.",
        "Blacksmith": lambda: move_to("blacksmith"),
        "Alchemist": lambda: move_to("alchemist"),
        "Mayor": lambda: move_to("mayor"),
        "Princess father": lambda: move_to("princess_father"),
        "Prison": lambda: move_to("prison"),
        "Leave town center": lambda: move_to("town_gate"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/town_center.png",
    },
    # check if the Goomba is dead before the player can receive the sword
    # checks if the sword is already in the inventory
    # adds the sword to the inventory if it is not already there
    "blacksmith": {
        "Story": "Hi hero! I heard what happened to the princess! \nAre you preparing to save her? \nI could help you if you help me. Clean my basement and I will reward you.",
        "Go downstairs": lambda: move_to("blacksmith_basement"),
        "Leave": lambda: move_to("town_center"),
        "Receive reward": lambda: (
            "You need to help the blacksmith to clean his basement first."
            if not monster_fight.is_monster_defeated("Goomba")
            else (
                "You have already received the sword."
                if inventory.has_item(
                    inventory.item_names[0]
                )  # Updated to use the item_names tuple for sword
                else inventory.receive_sword()
            )
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/blacksmith.png",
    },
    "blacksmith_basement": {
        "Story": "You are going down the stairs to the blacksmith's basement to see what you have to clean. You see a Goomba ready to attack!",
        "Go upstairs": lambda: (
            move_to("blacksmith")
            if monster_fight.is_monster_defeated("Goomba")
            else "You need to help the blacksmith to clean his basement first."
        ),
        "Fight": lambda: (
            "You already defeated the Goomba"
            if monster_fight.is_monster_defeated("Goomba")
            else monster_fight.initiate_fight("Goomba")
            # call the initiate fight function from the monster_fight.py file to start the fight with the Goomba
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/blacksmith_basement.png",
    },
    "alchemist": {
        "Story": "Hi hero, I heard what happened! I don't have much but here, take this at least. Please save our princess.",
        "Receive": lambda: (
            "You have already received the potion."
            if inventory.has_item(
                inventory.item_names[1]
            )  # Updated to use the item_names tuple for potion
            else inventory.receive_potion()
        ),
        "Leave": lambda: move_to("town_center"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/alchemist.png",
    },
    "mayor": {
        "Story": "Ah, Mario! You need to help us. We suffered too long under Bowser's terror. Go to the prison; maybe the prisoner has some information for you!",
        "Leave": lambda: move_to("town_center"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/mayor.png",
    },
    "princess_father": {
        "Story": "Save my daughter please! I heard the blacksmith could help you, pay him a visit.",
        "Leave": lambda: move_to("town_center"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/princess_father.png",
    },
    "prison": {
        "Story": "You see a Goomba in a cage. He looks scared and ready to do anything to be free.",
        "Talk": lambda: talk_to_prisoner(),
        "Leave": lambda: move_to("town_center"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/prison.png",
    },
    "castle_entrance": {
        "Story": "You are in front of the castle and a guard carrying multiple keys on his belt is blocking the entrance.\n You will need to fight him to enter.",
        "Fight": lambda: (
            "The Castle Guard is already defeated."
            if monster_fight.is_monster_defeated("Castle Guard")
            else monster_fight.initiate_fight("Castle Guard")
        ),  # The castle guard comes from the monster_fight.py file where the monster attributes are set.
        "Leave": lambda: move_to("town_gate"),
        "Steal key": lambda: (
            "You need to defeat the guard first."
            if not monster_fight.is_monster_defeated("Castle Guard")
            else (
                "You already have the key."
                if inventory.has_item(
                    inventory.item_names[2]
                )  # Updated to use the item_names tuple for key
                else inventory.pick_up_key()
            )
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/castle_entrance.png",
        "Use key": lambda: (
            move_to("bowser_fight")
            if inventory.has_item(
                inventory.item_names[2]
            )  # Updated to use the item_names tuple for key
            else "You need a key to enter."
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/castle_entrance.png",
    },
    "east_wall": {
        "Story": "You are at the east wall of the castle. You see a golden rock and a special pipe locked.",
        # When investigating, the key should be picked up and added to the inventory
        "Investigate": lambda: (
            "You have already picked up the key."
            if inventory.has_item(
                inventory.item_names[2]
            )  # Updated to use the item_names tuple for key
            else inventory.pick_up_key()
        ),
        # Ensure the player can only use the key if it has been picked up
        "Use key": lambda: (
            move_to("bowser_fight")
            if inventory.has_item(inventory.item_names[2])
            else "You need the key to unlock the pipe."
        ),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/east_wall.png",
    },
    # Move to game over location if Bowser is defeated
    # Check first if Bowser is defeated
    # Initiate the fight only if Bowser is not defeated and the player has more than 0 health
    "bowser_fight": {
        "Story": "You are in Bowser's bedroom. He is there, ready to fight.",
        "Fight": lambda: (
            monster_fight.initiate_fight("Bowser")
            if not monster_fight.is_monster_defeated("Bowser")
            else move_to("game_over")
        ),
        "Run": lambda: move_to("castle_entrance"),
        "Inventory": lambda: inventory.manage_inventory(),
        "Image": "images/bowser_bedroom.png",
    },
    "game_over": {
        "Story": "You Win! You defeated Bowser and saved the princess. Everyone is happy! \nClick the quit button with your mouse to exit the game.",
        "Image": "images/game_over.png",
    },
}


# My navigation function
# I need it as a global variable so I can change the current location outside of the function.
# Example: current_location = "kitchen" to current_location = "drain" .
# Without it, when I want to change the current location to another location,
# it would only be changed inside the function and not outside of it.
def move_to(location):
    global current_location
    current_location = location
    return status.player_current_status() + "\n" + get_current_story()


# I get the story key from the location dictionary and return it.
# status.get_health() and status.get_attack_power() are functions from the status.py file.
# I use the f string to format the string so I can use the variables inside the string like {location}
# Then I can access the values of the dictionary location by using the key in the square brackets.
# I use the current_location variable to get the current location of the player and the key "Story" to get the story of the current location.
def get_current_story():
    return f"{location[current_location]['Story']}"


# This is the same as the get_current_story function
# but I use the key "Image" to get the image of the current location.
# The image is a key in the location dictionary and the value is the path to the image ex: "images/kitchen.png"
def get_available_commands():
    commands = [
        cmd for cmd in location[current_location] if cmd != "Story" and cmd != "Image"
    ]
    return f"Actions: {' or '.join(commands)}"


# Here I check if the player has talked to the prisoner or not.
# If he did, I set the global variable talked_to_prisoner to true.
# With that, later in the game, the player can go to the east wall of the castle
# instead of the castle entrance and avoid the guard.
# That is why I need it as a global variable so I can change it outside of the function.
# Because it is set to false by default at the beginning of the game.
def talk_to_prisoner():
    global talked_to_prisoner
    if not talked_to_prisoner:
        talked_to_prisoner = True
        return "I will tell you how to infiltrate the castle and avoid the guard by climbing the east wall pipe.\nThere is a key under a golden rock to unlock the pipe.\nBut please put in a good word for the mayor in my favor."
    return "I told you everything I know, Get me out of here!"


# I just check if the player has the key item in his inventory with the
# pick_up_key function from the inventory.py file.
# In the pick up key function, I also use the collect_item function from the inventory.py
# to append the key item to the inventory_items list.
# The list starts as empty and then I append items during the game when they are collected.
def investigate_rock():
    return inventory.pick_up_key()


# Now my game_play function works is a bit more complex.
# i get the current location of the player and store it in the current_place variable.
# i strip the command to remove any whitespace and capitalize it(to avoid errors)
# then i get the command and call the associated action from the current_place dictionary.
# also, i use a little trick with the -1 index
# Because the command can be "use potion" or "use key" and i need to get the last word to check if it is potion or key.
def game_play(command):
    global current_location
    current_place = location[current_location]
    command = command.strip().capitalize()
    if command == "Inventory":
        return inventory.manage_inventory()
    elif command.lower().startswith("use"):
        item = command.split()[-1].lower()
        if item == "potion":
            return inventory.use_item(inventory.item_names[1])
        elif item == "key":
            return inventory.use_item(inventory.item_names[2])
        else:
            return f"Cannot use {item}. It may not be in your inventory or is unrecognized."
    elif command == "Attack":
        return monster_fight.fight()
    elif command in current_place:
        action = current_place[command]
        return action()

    else:
        return f"Can't {command} \n\n{get_available_commands()}"
