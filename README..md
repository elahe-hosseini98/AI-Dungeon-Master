# AI Dungeon Master

**AI Dungeon Master** is a web-based game that generates and manages a dynamic fantasy world with an AI-driven Dungeon Master (DM). The game provides an interactive storytelling experience by allowing players to make decisions that influence the progression of the adventure. Using prompts, the AI responds based on the player's inventory, game history, and quests, guiding them through a dark and mysterious fantasy journey.

## Features

- **Dynamic Story Generation**: The AI generates a unique fantasy adventure premise that blends magic, mystery, and danger, providing an engaging starting point for each game session.
  
- **Inventory Management**: The AI updates the player’s inventory in response to their actions, ensuring that the player can only reference and use items they actually possess. It gently encourages players to expand their inventory by collecting new items.

- **Quests and Game Progression**: Players will be given main quests and side quests, and their progress is tracked. As quests are completed, the player’s stats are updated, influencing future interactions with the world.

- **Player Stats**: The player’s actions impact their stats, such as **Damage**, **Strength**, **Wisdom**, and **Skill**. These stats directly affect their performance in various challenges, including fights and puzzles.

## How to Start the Game

After cloning the project, simply navigate to the root directory and run `app.py` to start the game:

```bash
python app.py
```
Here’s a preview of the main page of the game:

![AI Dungeon Master Main Page](![Uploading image.png…]()
)

### Requirements:
To run the game, you need an OpenRouter API key. Please add your key to the following configuration file:

```bash
config > openAI_config
```
## Game Logic Overview

1. **Base Story Generation**:
   The AI generates a simple and creative fantasy adventure premise in a few sentences, blending magic, mystery, and danger.

2. **Player Action Handling**:
   The AI responds to the player’s actions while considering their inventory, providing appropriate feedback and guidance for exploring, completing quests, or growing their inventory.

3. **Quest Management**:
   The AI defines 1 or 2 main quests and 2 to 3 side quests based on the current adventure, updating their status as the player progresses.
   
   - The player must first complete all side quests, and only after that can the main quests be completed.
   - **Win Scenario**: The player wins the game if all quests (both main and side) are completed.
   - **Lose Scenario**: The player loses the game if their damage exceeds 3.

4. **Inventory Updates**:
   The AI updates the player's inventory based on their actions, ensuring accurate changes to items added or removed from the inventory.

5. **Stats Tracking and Updates**:
   Player stats like **Damage**, **Strength**, **Wisdom**, and **Skill** are updated based on quest outcomes and other events like fighting or resting:

   - If the player completes a quest affecting **Wisdom**, their Wisdom will increase by 1.
   - If the player completes a quest affecting **Skill**, their Skill will increase by 1.
   - If the player engages in a fight, their **Damage** will increase by 1.
   - If the player rests, their **Damage** will decrease by 1.
   - After eating healthy food, the player's **Damage** will decrease by 1, and their **Strength** will increase by 1.

