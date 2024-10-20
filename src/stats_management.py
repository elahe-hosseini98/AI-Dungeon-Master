import random
from src.query_openAI import query_openAI
from config.statistics import stats
from config.openAI_config import available_models

model = available_models[0]

player_stats = None


def init_stats():
    global player_stats
    player_stats = stats

    return player_stats


def correct_response_format(response):
    global player_stats
    has_update = False

    try:
        updated_stats = eval(response)

        if isinstance(updated_stats, dict) and all(
                key in updated_stats for key in [
                    'Damage', 'Strength', 'Wisdom', 'Skill'
                ]
        ):
            if player_stats != updated_stats:
                has_update = True
                player_stats = updated_stats
    except (SyntaxError, ValueError, NameError):
        print("Failed to convert the model's response into the expected dictionary format.")

    return has_update, player_stats


def update_stats(updated_game_quests, game_quests, last_action, last_response, game_history):
    global player_stats
    has_updated = False

    for updated_quest, original_quest in zip(updated_game_quests, game_quests):
        if original_quest['status'] == 'Undone' and updated_quest['status'] == 'Done':
            if updated_quest['effect'] == 'Wisdom':
                player_stats['Wisdom']['value'] += 1
            elif updated_quest['effect'] == 'Skill':
                player_stats['Skill']['value'] += 1
            has_updated = True

    if not has_updated:
        prompt = (f"Based on the player's last action: {last_action}\n and the response: {last_response}\n, "
                  f"update the player's stats ({player_stats}) as follows:\n"
                  f"- If the player engaged in a fight, increase 'Damage' by 1.\n"
                  f"- If the player ate food or rested, increase 'Strength' by 1 (for food) and decrease 'Damage' by 1 (for both food and resting, but only if 'Damage' is greater than 0).\n"
                  f"Return only the updated {player_stats} dictionary, with no extra text or explanation.\n"
                  f"If the player neither ate healthy food, rested, nor engaged in a fight, return {player_stats} unchanged.")

        response = query_openAI(prompt, model)
        has_updated, player_stats = correct_response_format(response)

    return has_updated, player_stats


if __name__ == '__main__':
    init_stats()

    game_history = ("Adventure Premise: In the peaceful village of Eldergrove, an ancient tree known as"
                    " the Heartwood has begun to wither, threatening the land's magic. The villagers "
                    "believe a long-lost artifact lies hidden within the Shadow Woods, guarded by a "
                    "mischievous spirit. A band of unlikely heroes must brave the enchanted forest, "
                    "facing challenges and forming bonds to restore the Heartwood's life. Will they "
                    "succeed before darkness swallows Eldergrove?")

    game_quests = [
        {'main_quest': 'Retrieve the Lost Artifact from the Shadow Woods.', 'status': 'Undone', 'effect': 'Skill'},
        {'side_quest': 'Gain the Spirit’s Favor by solving its riddle.', 'status': 'Done', 'effect': 'Wisdom'},
        {'side_quest': 'Collect rare herbs to heal the Heartwood.', 'status': 'Undone', 'effect': 'Skill'}
    ]

    updated_game_quests = [
        {'main_quest': 'Retrieve the Lost Artifact from the Shadow Woods.', 'status': 'Undone', 'effect': 'Skill'},
        {'side_quest': 'Gain the Spirit’s Favor by solving its riddle.', 'status': 'Done', 'effect': 'Wisdom'},
        {'side_quest': 'Collect rare herbs to heal the Heartwood.', 'status': 'Undone', 'effect': 'Skill'}
    ]

    last_action = "i eat fresh apples!"
    last_response = "You ate apples. What will you do next?"

    print(update_stats(updated_game_quests, game_quests, last_action, last_response, game_history))