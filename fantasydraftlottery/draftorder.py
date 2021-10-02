import json
import numpy as np
import time
from random import random

# 1.0 Establishing globals.

# 1.1 This function is super great, found on SO


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])

# 1.2 just loading the defaults for testing


PLAYERS_DICT = {
    "players": {
        "Aaron":  [80,  [1, 2, 12, 11, 3, 10, 9, 8, 7, 4, 5, 6]],
        "Alex K": [75, [12, 11, 10, 8, 9, 7, 6, 2, 3, 4, 5, 1]],
        "Alison": [68,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "Alex W": [116, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "Chris":  [62,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "James C":  [105,  [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]],
        "James W":  [86,  [6, 5, 7, 4, 8, 3, 9, 10, 11, 12, 1, 2]],
        "John":   [58,  [4, 9, 10, 11, 1, 2, 3, 5, 6, 7, 8, 12]],
        "Neil":   [98,  [4, 5, 6, 1, 2, 3, 7, 8, 9, 10, 11, 12]],
        "Ravi":   [110,  [3, 4, 2, 5, 1, 6, 8, 9, 7, 10, 11, 12]],
        "Rohan":  [92,  [3, 4, 2, 5, 1, 6, 8, 9, 7, 10, 11, 12]],
        "Sahil":  [50,  [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]],
    },
    "placement": "Sahil,John,Neil,James C,Ravi,Aaron,James W,Alex W,Rohan,Alex K,Alison,Chris"
}


class Lottery:
    messages = []
    pick_messages = []

    def run(self, player_dict, lotteried=None):
        # 2.0 Setting up the important variables
        #     Set of taken picks, list of players selected (which needs to be ordered)
        #     all of the ball pit, and all of the information on the players.
        placement = player_dict['placement'].split(',')
        players = player_dict['players']
        if not lotteried:
            lotteried = len(placement)
        taken_picks = {0}
        selected_players = []

        i = 0
        player_pick_dict = {}

        combos = np.array(sum([[player] * odds_prefs[0] for player, odds_prefs in players.items()], []))
        balls = combos.size
        ball_pit = np.arange(balls)
        np.random.shuffle(ball_pit)
        np.random.shuffle(combos)
        pick_names = [ordinal(n) for n in range(1, len(placement) + 1)]

        # 3.0 Here's the meat and potatoes

        # 3.1 Sets limit for how many picks to go through
        while len(taken_picks) <= lotteried:
            # 3.2 Draws the next player and iterates
            ball_drawn = ball_pit[i]
            i += 1
            player_drawn = combos[ball_drawn]

            # 3.3 Checks if player has already been drawn
            if player_drawn in selected_players:
                self.messages.append('Player picked again!')
                pass
            else:
                # 3.4.0 If a new player's name has been drawn, adds them
                self.messages.append('{} player picked! I wonder who it is...'.format(pick_names[len(taken_picks) -
                                                                                                      1]))
                selected_players.append(player_drawn)
                # 3.4.1 Checks their preferences to see which pick they actually get
                pick_prefs = players[player_drawn][1]
                current_pick = 0
                j = 0
                while current_pick in taken_picks:
                    current_pick = pick_prefs[j]
                    j += 1
                # 3.5 Adds it to the record
                taken_picks.update([current_pick])
                player_pick_dict[pick_names[current_pick - 1]] = player_drawn
        # That's the end of the lottery

        # 4.0 Just for fun, calculate the probability of the result. Rull easy.
        prob = 1
        for name in selected_players:
            k = players[name][0]
            player_prob = k / balls
            prob *= player_prob
            balls -= k
        self.messages.append('The probability of this result was {}%!'.format(round(prob * 100, 5)))

        # 5.0 This is a similar process, but for the non-lotteried picks. These are
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
                player_pick_dict[pick_names[current_pick - 1]] = name

        # 6.0 Finale time!
        #     This sends the final lottery results to the group, in order from last
        #     to first!

        # 6.1 I put my thang down flip it and reverse it
        pick_names.reverse()
        for i, name in enumerate(pick_names):
            self.pick_messages.append('The {} pick goes to...'.format(name))
            self.pick_messages.append('{}!'.format(player_pick_dict[name]))


if __name__ == '__main__':
    lotto = Lottery()
    lotto.run(PLAYERS_DICT, 5)
    for i, msg in enumerate(lotto.pick_messages):
        time.sleep(random())
        print(msg)
