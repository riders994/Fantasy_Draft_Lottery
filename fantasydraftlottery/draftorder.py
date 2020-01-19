import json
import numpy as np

# 1.0 Establishing globals.


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


PLAYER_FILE = './resources/player_values_2019.json'
with open(PLAYER_FILE, 'rb') as file:
    PLAYERS_DICT = json.load(file)


class Lottery:
    messages = []
    pick_messages = []

    def __init__(self):
        pass

    def run(self, player_dict, lotteried=None):
        # 3.0 Setting up the important variables
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

        # 5.0 Here's the meat and potatoes

        # 5.1 This way it ends when 6 picks have been lotteried, as the 7th one breaks
        while len(taken_picks) <= lotteried:
            # 5.2 Draws the next player and iterates
            ball_drawn = ball_pit[i]
            i += 1
            player_drawn = combos[ball_drawn]

            # 5.3 Checks if player has already been drawn
            if player_drawn in selected_players:
                self.messages.append('Player picked again!')
                pass
            else:
                # 5.4.0 If a new player's name has been drawn, adds them
                self.messages.append('{} player picked! I wonder who it is...'.format(pick_names[len(taken_picks) -
                                                                                                      1]))
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
                player_pick_dict[pick_names[current_pick - 1]] = player_drawn
        # That's the end of the lottery

        # Just for fun, calculate the probability of the result. Rull easy.
        prob = 1
        for name in selected_players:
            k = players[name][0]
            player_prob = k / balls
            prob *= player_prob
            balls -= k
        self.messages.append('The probability of this result was {}%!'.format(round(prob * 100, 5)))

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
                player_pick_dict[pick_names[current_pick - 1]] = name

        # 7.0 Finale time!
        #     This sends the final lottery results to the group, in order from last
        #     to first!

        # 7.1 I put my thang down flip it and reverse it
        pick_names.reverse()
        for i, name in enumerate(pick_names):
            self.pick_messages.append('The {} pick goes to...'.format(name))
            self.pick_messages.append('{}!'.format(player_pick_dict[name]))


if __name__ == '__main__':
    lotto = Lottery()
    lotto.run(PLAYERS_DICT, 6)
    for msg in lotto.pick_messages:
        print(msg)
