from src.query_openAI import query_openAI
from config.openAI_config import available_models

model = available_models[0]


def summarize(text):
    prompt = (
        f"Generate a structural summary of the given text {text}. The important changes in user "
        f"actions and AI responses must be included. Only return a text summary without any extra word of "
        f"explanation and please normalize the text by deleting extra newline characters and formatting it into a single line.!")
    return query_openAI(prompt, model)


if __name__ == '__main__':
    text = "Adventure Premise: In the land of Eldergrove, ancient trees whisper secrets of a lost civilization that vanished centuries ago. One day, a vibrant flower blooms in the heart of the enchanted forest, stirring dreams of adventure and unexplored ruins. The players, a group of curious travelers, must uncover the truth behind this magical bloom while facing mischievous forest spirits and the challenges of a world filled with wonders. Their main quest is to locate the Eldergrove Blossom, which holds the essence of the lost civilization's magic. Along the way, they can take on side quests to free a trapped forest spirit by gathering three sacred relics and explore ancient ruins to discover forgotten treasures. Will they unlock the secrets of Eldergrove, or will its mysteries engulf them? 1- Player: what do i see and where should i go first? AI DM: You see a fork in the road. One path leads into the forest, the other to the mountains. Which way? 2- Player: i choose to go toward the mountains. AI DM: You ascend the mountain path, discovering a hidden cave entrance ahead. What do you do?"
    print(summarize(text))
