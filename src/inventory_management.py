import random
from src.query_openAI import query_openAI
from config.openAI_config import available_models
from config.inventories import (
    basic_equipment,
    weapons,
    armor_and_shields,
    magic_items,
    adventuring_tools,
    miscellaneous_items,
    all_inventories
)

model = available_models[0]

player_inventories = {
    "Basic Equipment": [],
    "Weapons": [],
    "Armor and Shields": [],
    "Magic Items": [],
    "Adventuring Tools": [],
    "Miscellaneous Items": []
}

def init_inventory():
    global player_inventories

    def random_items(inventory, min=1, max=None):
        if max is None: max = len(inventory)
        count = random.randint(min, max)
        return random.sample(list(inventory.items()), count)

    init_basic_equipment = random_items(basic_equipment, 3, 5)
    init_weapons = random_items(weapons, 1, 2)
    init_armor_and_shields = random_items(armor_and_shields, 1, 2)
    init_magic_items = random_items(magic_items, 0, 1)
    init_adventuring_tools = random_items(adventuring_tools,0, 1)
    init_miscellaneous_items = random_items(miscellaneous_items, 0, 1)

    player_inventories = {
        "Basic Equipment": init_basic_equipment,
        "Weapons": init_weapons,
        "Armor and Shields": init_armor_and_shields,
        "Magic Items": init_magic_items,
        "Adventuring Tools": init_adventuring_tools,
        "Miscellaneous Items": init_miscellaneous_items
    }

    return player_inventories


def correct_response_format(response):
    global player_inventories
    has_update = False

    try:
        updated_inventory = eval(response)

        if isinstance(updated_inventory, dict) and all(
                key in updated_inventory for key in [
                    'Basic Equipment', 'Weapons', 'Armor and Shields',
                    'Magic Items', 'Adventuring Tools', 'Miscellaneous Items'
                ]
        ):
            if player_inventories != updated_inventory:
                has_update = True
                player_inventories = updated_inventory
    except (SyntaxError, ValueError, NameError):
        print("Failed to convert the model's response into the expected dictionary format.")

    return has_update, player_inventories


def update_inventory(last_action, last_response, game_history):
    global player_inventories

    prompt = (
        "Analyze the following information and generate the updated player inventory accordingly. "
        "Ensure that the inventory reflects any actual changes needed based on the player's last action and the game's last response. "
        "If the last response indicates an item was successfully added or removed, ensure that the inventory is updated to reflect this change.\n\n"
        "Return the updated inventory in the following format:\n\n"
        "{'Basic Equipment': [...], 'Weapons': [...], 'Armor and Shields': [...], 'Magic Items': [...], "
        "'Adventuring Tools': [...], 'Miscellaneous Items': [...]}\n\n"
        f"1. The player's last action: {last_action}\n"
        f"2. The game's last response: {last_response}\n"
        "3. The full list of all available inventories:\n"
        f"{all_inventories}\n\n"
        "4. The current state of the player's inventory:\n"
        f"{player_inventories}\n\n"
        f"5. A summary of the player's game history: {game_history}\n"
        "Please provide the updated inventory only, without any additional text."
    )

    response = query_openAI(prompt, model)

    return correct_response_format(response)
