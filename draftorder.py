import json, time
import numpy as np
from messagesender import FacebookMessenger

"""
I wrote this script to run my fantasy basketball league's draft lottery.
I wanted to do it the way the nba draft lottery is meant to emulate, with 1000
lottery "balls" in play. Random numbers balls are drawn, which each have a name
"on" them based on the probabilities assigned to each player.
"""

# 1.0 Establishing globals. All of these should be pretty obvious.
PICK_NAMES = '1st,2nd,3rd,4th,5th,6th,7th,8th,9th,10th,11th,12th'.split(',')

PLAYER_FILE = 'player_values_2019.json'

CREDS = 'creds.json'

# Not all picks are lotteried, only the first 6 choice spots. Players are allowed
# to choose which pick they want if they win the lottery.
LOTTERIED = 6

if __name__ == '__main__':

    # 2.0 Loading files
    # 2.1 Loads the dictionary of all player information, from finish to odds, to preferences
    with open(PLAYER_FILE, 'rb') as file:
        players_dict = json.load(file)

    # 2.2 Loads the credentials to log in to the FacebookMessenger class
    # with open(CREDS, 'rb') as file:
    #     credentials = json.load(file)

    # 3.0 Setting up the important variables
    #     Set of taken picks, list of players selected (which needs to be ordered)
    #     all of the ball pit, and all of the information on the players.
    taken_picks = {0}
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

    # 4.0 Initialize the chat client. If there are creds problems, will immediately die.
    # chat_client = FacebookMessenger(credentials)

    # 5.0 Here's the meat and potatoes
    #     TODO: Make this cleaner, better, make it a class maybe?

    # 5.1 This way it ends when 6 picks have been lotteried, as the 7th one breaks
    while len(taken_picks) <= LOTTERIED:
        # 5.2 Draws the next player and iterates
        ball_drawn = ball_pit[i]
        i += 1
        player_drawn = combos[ball_drawn]

        # 5.3 Checks if player has already been drawn
        if player_drawn in selected_players:
            print('Player picked again!')
            pass
        else:
            # 5.4.0 If a new player's name has been drawn, adds them
            print('{} player picked! I wonder who it is...'.format(PICK_NAMES[len(taken_picks) - 1]))
            selected_players.append(player_drawn)
            # 5.4.1 Checks their preferences to see which pick they actually get
            pick_prefs = players[player_drawn][1]
            current_pick = 0
            j = 0
            while current_pick in taken_picks:
                current_pick = pick_prefs[j]
                j += 1
            # 5.5 Adds it to the record
            taken_picks.update([current_pick])
            player_pick_dict[PICK_NAMES[current_pick - 1]] = player_drawn
    # That's the end of the lottery

    # Just for fun, calculate the probability of the result. Rull easy.
    prob = 1
    for name in selected_players:
        k = players[name][0]
        player_prob = k/balls
        prob *= player_prob
        balls -= k
    print('The probability of this result was {}%!'.format(round(prob * 100, 5)))

    # 6.0 This is a similar process, but for the non-lotteried picks. These are
    #     by playoff finish.
    for name in placement:
        if name not in selected_players:
            selected_players.append(name)
            pick_prefs = players[name][1]
            current_pick = 0
            while current_pick in taken_picks:
                current_pick = pick_prefs[0]
                pick_prefs = pick_prefs[1:]
            taken_picks.update([current_pick])
            player_pick_dict[PICK_NAMES[current_pick - 1]] = name

    # 7.0 Finale time!
    #     This sends the final lottery results to the group, in order from last
    #     to first!

    # 7.1 I put my thang down flip it and reverse it
    PICK_NAMES.reverse()
    for i, name in enumerate(PICK_NAMES):
        print('The {} pick goes to...'.format(name))
        # 7.2 sleeps added to build DRAMA
        s1 = i/(i + 1)
        time.sleep(s1)
        print('{}!'. format(player_pick_dict[name]))
        if i:
            time.sleep(s1 ** 0.5)
