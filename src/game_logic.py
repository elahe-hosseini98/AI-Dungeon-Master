from src.query_openAI import query_openAI
from config.openAI_config import available_models
import ast

model = available_models[0]


def has_won(game_quests):
    for quest in game_quests:
        if 'main_quest' in quest and quest['status'] != 'Done':
            return False
    return True


def has_lost(player_stats, player_damage_limit=3):
    if int(player_stats["Damage"]["value"]) > player_damage_limit:
        return True
    return False


def correct_ai_response_format(ai_response, game_quests):
    has_update = False

    try:
        updated_game_quests = ast.literal_eval(ai_response)

        if updated_game_quests != game_quests:
            has_update = True

        game_quests = updated_game_quests

    except (ValueError, SyntaxError):
        print("Error: The Updated game quests string could not be converted.")

    return has_update, game_quests


def has_done_side_quests(last_action, last_response, game_quests, game_history):
    global model

    prompt = (
        f"Given the player's last action: {last_action}, and the generated response to that action: {last_response},\n\n"
        f"check if the player has completed a side quest from {game_quests}. If a side quest with the status 'Undone' "
        f"has been completed, create a new list identical to {game_quests}, but update the corresponding side quest's "
        f"status to 'Done'.\n\n"
        f"If no side quest is completed, return {game_quests} unchanged.\n\n"
        f"Please return only a list of dictionaries in the exact format of {game_quests}, with no additional explanations."
    )

    ai_response = query_openAI(prompt, model)

    return correct_ai_response_format(ai_response, game_quests)


def has_done_main_quests(last_action, last_response, game_quests, game_history):
    global model
    all_done = True

    for quest in game_quests:
        if 'side_quest' in quest and quest['status'] != 'Done':
            all_done = False
            break

    if all_done:
        prompt = (
            f"Given the player's last action: {last_action}, and the response to that action: {last_response},\n\n"
            f"determine if the player has completed a main quest from {game_quests} based on this new action. "
            f"If the quest's status is 'Undone', update the status to 'Done' in a new list that mirrors {game_quests}.\n\n"
            f"If no main quest is completed, return {game_quests} unchanged.\n\n"
            f"Please return only a list of dictionaries in the exact format of {game_quests}, without any additional explanations."
        )

        ai_response = query_openAI(prompt, model)

        return correct_ai_response_format(ai_response, game_quests)

    return False, game_quests


if __name__ == '__main__':
    game_history = ("Adventure Premise: In the peaceful village of Eldergrove, an ancient tree known as"
                    " the Heartwood has begun to wither, threatening the land's magic. The villagers "
                    "believe a long-lost artifact lies hidden within the Shadow Woods, guarded by a "
                    "mischievous spirit. A band of unlikely heroes must brave the enchanted forest, "
                    "facing challenges and forming bonds to restore the Heartwood's life. Will they "
                    "succeed before darkness swallows Eldergrove?")

    game_quests = [
        {'main_quest': 'Retrieve the Lost Artifact from the Shadow Woods.', 'status': 'Undone', 'effect': 'Skill'},
        {'side_quest': 'Gain the Spirit’s Favor by solving its riddle.', 'status': 'Done', 'effect': 'Wisdom'},
        {'side_quest': 'Collect rare herbs to heal the Heartwood.', 'status': 'Done', 'effect': 'Skill'}
    ]

    last_response = "You can't retrieved the Lost Artifact yet! What would you like to do next?"
    last_action = "I retrieve the Lost Artifact from the Shadow Woods."

    print(has_done_main_quests(last_action, last_response, game_quests, game_history))