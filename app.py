from flask import Flask, render_template, request, redirect, url_for
from src.ai_dm import generate_story_line, generate_ai_response, define_quests
from src.inventory_management import init_inventory, update_inventory
from src.stats_management import init_stats, update_stats
from src.summarizer import summarize
from src.game_logic import has_done_main_quests, has_done_side_quests, has_won, has_lost

app = Flask(__name__)
story_line = generate_story_line()
game_log = []
game_history = ""
action_count = 0
player_inventories = init_inventory()
player_stats = init_stats()
game_quests = []


@app.route('/')
def home():
    global game_log
    global story_line
    global action_count
    global player_inventories
    global player_stats
    global game_history
    global game_quests

    action_count = 0
    game_log = ['<strong style="font-size: 22px;">Adventure Premise:</strong><br>' + story_line]
    game_quests = define_quests(story_line)

    return render_template('index.html', story_line=story_line,
                           player_actions_responses=game_log, player_inventories=player_inventories,
                           player_stats=player_stats,
                           game_quests=game_quests)


@app.route('/play', methods=['POST'])
def play():
    global action_count
    global game_log
    global player_inventories
    global player_stats
    global game_history
    global game_quests

    player_input = request.form['player_input']

    action_count += 1

    game_log.append(f"<strong>{action_count}- Player:</strong> {player_input}")
    game_history += f" {action_count}- Player: {player_input}"

    ai_response = generate_ai_response(player_input, game_history, player_inventories, game_quests)
    game_log.append(f"<strong>AI DM:</strong> {ai_response}<hr>")
    game_history += f" AI DM: {ai_response}"

    game_history = summarize(game_history)

    inventories_has_update, player_inventories = update_inventory(player_input, ai_response, game_history)
    side_quests_has_update, updated_game_quests = has_done_side_quests(player_input, ai_response, game_quests, game_history)
    main_quests_has_update, updated_game_quests = has_done_main_quests(player_input, ai_response, updated_game_quests, game_history)
    stats_has_update, player_stats = update_stats(updated_game_quests, game_quests, player_input, ai_response, game_history)

    game_quests = updated_game_quests

    if has_won(game_quests):
        return redirect(url_for('win'))

    if has_lost(player_stats):
        return redirect(url_for('lose'))

    return render_template(
        'index.html', player_actions_responses=game_log,
                           player_inventories=player_inventories,
                           inventories_has_update=inventories_has_update,
                           player_stats=player_stats,
                           stats_has_update=stats_has_update,
                           game_quests = game_quests,
                           side_quests_has_update=side_quests_has_update,
                           main_quests_has_update=main_quests_has_update
                           )


@app.route('/win')
def win():
    return render_template('result.html', outcome='win', player_stats=player_stats)


@app.route('/lose')
def lose():
    return render_template('result.html', outcome='lose', player_stats=player_stats)


@app.route('/restart', methods=['POST'])
def restart():
    global story_line
    global game_log
    global action_count
    global player_inventories
    global player_stats
    global game_history
    global game_quests

    story_line = generate_story_line()
    game_quests = define_quests(story_line)

    action_count = 0

    game_log = ['<strong style="font-size: 22px;">Adventure Premise:</strong><br>' + story_line]
    game_history = ""

    player_inventories = init_inventory()
    player_stats = init_stats()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
