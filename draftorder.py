import json, time
import numpy as np
from messagesender import FacebookMessenger


pick_names = '1st,2nd,3rd,4th,5th,6th,7th,8th,9th,10th,11th,12th'.split(',')

PLAYER_FILE = 'player_values_2018.json'

CREDS = 'creds.json'

LOTTERIED = 6

if __name__ == '__main__':

    with open(PLAYER_FILE, 'rb') as file:
        players_dict = json.load(file)

    # with open(CREDS, 'rb') as file:
    #     credentials = json.load(file)

    taken_picks = [0]
    selected_players = []

    i = 0
    player_pick_dict = {}

    players = players_dict['players']
    placement = players_dict['placement'].split(',')
    combos = np.array(sum([[player] * odds_prefs[0] for player, odds_prefs in players.items()], []))
    balls = combos.size
    ball_pit = np.arange(balls)
    np.random.shuffle(ball_pit)
    np.random.shuffle(combos)

    # chat_client = FacebookMessenger(credentials)

    while len(taken_picks) <= LOTTERIED:
        ball_drawn = ball_pit[i]
        i += 1
        player_drawn = combos[ball_drawn]
        if player_drawn in selected_players:
            print('Player picked again!')
            pass
        else:
            print('{} player picked! I wonder who it is...'.format(pick_names[len(taken_picks) - 1]))
            selected_players.append(player_drawn)
            pick_prefs = players[player_drawn][1]
            current_pick = 0
            j = 0
            while current_pick in taken_picks:
                current_pick = pick_prefs[j]
                j += 1
            taken_picks.append(current_pick)
            player_pick_dict[pick_names[current_pick - 1]] = player_drawn
    print(player_pick_dict)
    prob = 1
    for name in selected_players:
        k = players[name][0]
        player_prob = k/balls
        prob *= player_prob
        balls -= k
    print('The probability of this result was {}%!'.format(round(prob * 100, 5)))
    for name in placement:
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
        print('The {} pick goes to...'.format(name))
        s1 = i/(i + 1)
        time.sleep(s1)
        print('{}!'. format(player_pick_dict[name]))
        if i:
            time.sleep(s1 ** 0.5)
