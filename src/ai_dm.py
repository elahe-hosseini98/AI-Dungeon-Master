from src.query_openAI import query_openAI
from config.inventories import all_inventories
from src.query_openAI import query_openAI
from config.openAI_config import available_models
import ast

model = available_models[0]


def generate_story_line():
    base_story_prompt = (
        "Generate a simple, creative, and jargon-free fantasy adventure premise for a D&D game. "
        "It should blend magic, mystery, and a sense of danger or fear, with a dark twist. Always be creative and "
        "do not stuck to a certain type of stories .Keep the story within 3-4 sentences and under 300 characters."
    )

    return query_openAI(base_story_prompt, model)


def generate_ai_response(player_action, game_history, player_inventories, game_quests):
    prompt = (
            f"Give a proper response to the player action: {player_action}\n"
            f"Ensure the AI responds based on the player's current inventory. Do not allow the player to reference or use items "
            f"they don't have. Gently remind them if they try.\n\n"
            
            #f"If the player want to complete a quest in {game_quests} which has a 'Undone' status, help him to complete that quest in a straight-forward and creative way.\n\n"
            
            #f"Prevent player to do the main_quests if any side_quests in {game_quests} having status of 'Undone'.\n\n"
            
            f"Sometimes, encourage the player to expand their inventory by collecting items from {all_inventories} and suggest actions to help them grow their inventory.\n\n"

            f"Game History:\n" + "\n".join(game_history) + "\n\n"
            f"Player's Current Inventory:\n{player_inventories}\n\n"
            f"All Available Inventories:\n{all_inventories}\n\n"
            f"Respond as the AI Dungeon Master, keeping the response under 200 characters."
            f" Guide the player on exploring, completing side quests, expanding their inventory,"
            f" or leading them into fights."
    )

    return query_openAI(prompt, model)



def define_quests(adventure_premise, retry_count=0):
    sample_quests = [
        {'main_quest': 'Find the Ancient Sword.', 'status': 'Undone', 'effect': 'Wisdom'},
        {'side_quest': 'Rescue the Village Elder.', 'status': 'Undone', 'effect': 'Skill'},
        {'side_quest': 'Defeat the Dragon.', 'status': 'Undone', 'effect': 'Wisdom'},
    ]

    prompt = (f"Based on this adventure premise: {adventure_premise}, please define 1 or 2 main quests"
              f" and 2 to 3 side quests. as the response to this prompt please return only! a dict the same as"
              f"{sample_quests}, and set the status for all of them Undone. Note that for the 'effect' there is only"
              f"two options of 'Wisdom' and 'Skill'.")

    game_quests_str = query_openAI(prompt, model)

    try:
        game_quests = ast.literal_eval(game_quests_str)
        return game_quests

    except (ValueError, SyntaxError):
        print("Error: The generated game quests string could not be converted.")
        return []




