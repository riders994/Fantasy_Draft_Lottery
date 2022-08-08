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
        "Aaron":  [110,  [1, 2, 12, 11, 3, 10, 9, 8, 7, 4, 5, 6]],
        "Alex K": [50, [12, 11, 10, 8, 9, 7, 6, 2, 3, 4, 5, 1]],
        "Alison": [56,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "Alex W": [86, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "Chris":  [104,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
        "James":  [98,  [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]],
        "Joe":    [92,  [6, 5, 7, 4, 8, 3, 9, 10, 11, 12, 1, 2]],
        "John":   [62,  [4, 9, 10, 11, 1, 2, 3, 5, 6, 7, 8, 12]],
        "Neil":   [68,  [4, 5, 6, 1, 2, 3, 7, 8, 9, 10, 11, 12]],
        "Ravi":   [74,  [3, 4, 2, 5, 1, 6, 8, 9, 7, 10, 11, 12]],
        "Rohan":  [116,  [3, 4, 2, 5, 1, 6, 8, 9, 7, 10, 11, 12]],
        "Sahil":  [80,  [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]],
    },
    "placement": "John,Neil,James,Chris,Aaron,Rohan,Joe,Alex W,Sahil,Ravi,Alison,Alex K"
}


class Lottery:
    messages = []
    pick_messages = []
    taken_picks = {0}
    selected_players = []
    player_pick_dict = {}

    def __init__(self, player_dict, lotteried=None):
        # 2.0 Setting up the important variables
        #     Set of taken picks, list of players selected (which needs to be ordered)
        #     all of the ball pit, and all of the information on the players.

        self.placement = player_dict['placement'].split(',')
        self.players = player_dict['players']
        if lotteried:
            self.lotteried = lotteried
        else:
            self.lotteried = len(self.placement)
        self.combos = np.array(sum([[player] * odds_prefs[0] for player, odds_prefs in self.players.items()], []))
        self.balls = self.combos.size
        self.ball_pit = np.arange(self.balls)
        np.random.shuffle(self.ball_pit)
        np.random.shuffle(self.combos)
        self.pick_names = [ordinal(n) for n in range(1, len(self.placement) + 1)]

    def _get_pick_choice(self, player):
        pick_prefs = self.players[player][1]
        current_pick = 0
        j = 0
        while current_pick in self.taken_picks:
            current_pick = pick_prefs[j]
            j += 1
        return current_pick

    def _lottery(self):
        i = 0

        # 3.0 Here's the meat and potatoes

        # 3.1 Sets limit for how many picks to go through
        while len(self.taken_picks) <= self.lotteried:
            # 3.2 Draws the next player and iterates
            ball_drawn = self.ball_pit[i]
            i += 1
            player_drawn = self.combos[ball_drawn]

            # 3.3 Checks if player has already been drawn
            if player_drawn in self.selected_players:
                self.messages.append('Player picked again!')
                pass
            else:
                # 3.4.0 If a new player's name has been drawn, adds them
                self.messages.append('{} player picked! I wonder who it is...'.format(self.pick_names[
                    len(self.taken_picks) - 1
                                                                                      ]))
                self.selected_players.append(player_drawn)
                # 3.4.1 Checks their preferences to see which pick they actually get

                pick_choice = self._get_pick_choice(player_drawn)
                # 3.5 Adds it to the record
                self.taken_picks.update([pick_choice])
                self.player_pick_dict[self.pick_names[pick_choice - 1]] = player_drawn
        # That's the end of the lottery

    def _proba(self):
        # 4.0 Just for fun, calculate the probability of the result. Rull easy.
        prob = 1
        for name in self.selected_players:
            k = self.players[name][0]
            player_prob = k / self.balls
            prob *= player_prob
            self.balls -= k
        self.messages.append('The probability of this result was {}%!'.format(round(prob * 100, 5)))

    def _fill_order(self):
        # 5.0 This is a similar process, but for the non-lotteried picks. These are
        #     by playoff finish.
        for name in self.placement:
            if name not in self.selected_players:
                self.selected_players.append(name)
                pick_choice = self._get_pick_choice(name)
                self.taken_picks.update([pick_choice])
                self.player_pick_dict[self.pick_names[pick_choice - 1]] = name

    def _verbose(self):
        # 6.0 Finale time!
        #     This sends the final lottery results to the group, in order from last
        #     to first!

        # 6.1 I put my thang down flip it and reverse it
        self.pick_names.reverse()
        for i, name in enumerate(self.pick_names):
            self.pick_messages.append('The {} pick goes to...'.format(name))
            self.pick_messages.append('{}!'.format(self.player_pick_dict[name]))

    def run(self, proba=True, verbose=True):
        self._lottery()
        if proba:
            self._proba()
        self._fill_order()
        if verbose:
            self._verbose()


if __name__ == '__main__':
    lotto = Lottery(PLAYERS_DICT, 5)
    lotto.run()
    for _, msg in enumerate(lotto.pick_messages):
        time.sleep(random())
        print(msg)
