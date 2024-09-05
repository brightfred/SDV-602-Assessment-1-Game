import status.status as status
import command_parser.command_parser as parser

# Tuple with all item names
# i tried multiple versions and dictionnary would have been easier to manage the state and name
# but i wanted to have at least a lear tuple use in my code
# tuple being immutable is a good way to store the item names but thenot the state as i could not update it later
item_names = ("sword", "potion", "key")

# Global variables
sword_received = False
potion_received = False
key_picked = False

# List to store item in the inventory
inventory_items = []


# Collect an item and add it to the inventory list
def collect_item(item):
    if item not in inventory_items:
        inventory_items.append(item)
    return f"{item.capitalize()} added to the inventory."


# Check if the specific item is in the inventory
# Example : i need it to check if the key is in the inventory to move to the bowser fight
def has_item(item):
    return item in inventory_items


# Use an item from the inventory
#  Check is to see if the key is in the inventory and if it is he can move to the bowser fight
# (was getting error with the lambda function in location)
#  If the potion is in the inventory he can use it to heal 50 health
def use_item(item):
    if item == item_names[1] and item in inventory_items:  # Use potion
        inventory_items.remove(item)
        status.update_health(50)
        return "Delicious! +50 health."
    elif item == item_names[2] and item in inventory_items:
        parser.move_to("bowser_fight")
        return "You used the key."
    else:
        return f"You do not have a {item}."


# Manage inventory and list of available command based on items in the inventory
def manage_inventory():
    available_commands = []

    if has_item(item_names[1]):  # Check if he has the potion
        available_commands.append("Use potion")
    if has_item(item_names[2]):  # Check if he has the key
        available_commands.append("Use key")  # Add the key to the available commands

    inventory_text = show_inventory()
    commands_text = (
        f"\nAvailable Commands: {' or '.join(available_commands)}"
        if available_commands
        else ""
    )
    return inventory_text + commands_text


# Show the player's current inventory
# I call this function in the manage_inventory function
def show_inventory():
    return f"Inventory: {', '.join(inventory_items) if inventory_items else 'Inventory is empty'}"


def receive_potion():
    global potion_received
    if not potion_received:
        potion_received = True
        return collect_item(item_names[1])
    return "You have already have the potion."


# (automatically add attack power to player, no need to equip it)
def receive_sword():
    global sword_received
    if not sword_received:
        sword_received = True
        status.increase_attack(20)
        return collect_item(item_names[0])
    return "You have already have the sword."


def pick_up_key():
    global key_picked
    if not key_picked:
        key_picked = True
        return collect_item(item_names[2])
    return "You have already picked up the key."


# Test the inventory module on receiving the sword and potion
if __name__ == "__main__":
    print("Inventory Module Test")
    print(receive_sword())
    print(receive_potion())
