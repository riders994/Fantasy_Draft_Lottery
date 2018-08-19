import json, time
import numpy as np
from messagesender import FacebookMessenger


players = {
    'Alex': (125, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Allie': (75, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Ben': (110, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Chris': (80, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Guillem': (95, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'John': (120, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],),
    'Neil': (115, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Ravi': (85, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    'Rohan': (90, [2, 5, 7, 1, 3, 4, 6, 8, 9, 10]),
    'Sahil': (105, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
}

pick_names = '1st,2nd,3rd,4th,5th,6th,7th,8th,9th,10th'.split(',')

combos = np.array(sum([[player] * odds_prefs[0] for player, odds_prefs in players.items()], []))

np.random.shuffle(combos)

balls = np.arange(1000)

np.random.shuffle(balls)

taken_picks = [0]
selected_players = []

i = 0
player_pick_dict = {}

player_placement = 'Alex,John,Neil,Ben,Sahil,Guillem,Rohan,Ravi,Chris,Allie'.split(',')

if __name__ == '__main__':
    with open('creds.json', 'rb') as file:
        credentials = json.load(file)

    chat_client = FacebookMessenger(credentials)

    while len(taken_picks) < 6:
        ball_drawn = balls[i]
        i += 1
        player_drawn = combos[ball_drawn]
        if player_drawn in selected_players:
            chat_client.send_message('Player picked again!')
            pass
        else:
            chat_client.send_message('{} player picked! I wonder who it is...'.format(pick_names[len(taken_picks) - 1]))
            selected_players.append(player_drawn)
            pick_prefs = players[player_drawn][1]
            current_pick = 0
            while current_pick in taken_picks:
                current_pick = pick_prefs[0]
                pick_prefs = pick_prefs[1:]
            taken_picks.append(current_pick)
            player_pick_dict[pick_names[current_pick - 1]] = player_drawn
    chat_client.send_message(player_pick_dict)
    prob = 1
    balls = 1000
    for name in selected_players:
        k = players[name][0]
        player_prob = k/balls
        prob *= player_prob
        balls -= k
    chat_client.send_message('The probability of this result was {}%!'.format(round(prob * 100, 5)))
    for name in player_placement:
        if name not in selected_players:
            selected_players.append(name)
            pick_prefs = players[player_drawn][1]
            current_pick = 0
            while current_pick in taken_picks:
                current_pick = pick_prefs[0]
                pick_prefs = pick_prefs[1:]
            taken_picks.append(current_pick)
            player_pick_dict[pick_names[current_pick - 1]] = name
    pick_names.reverse()
    for i, name in enumerate(pick_names):
        chat_client.send_message('The {} goes to...'.format(name))
        s1 = i/(i + 1)
        time.sleep(s1)
        chat_client.send_message('{}!'. format(player_pick_dict[name]))
        if i:
            time.sleep(s1 ** 0.5)