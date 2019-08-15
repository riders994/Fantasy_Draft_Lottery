import numpy as np
import pandas as pd


"""
This is a dumb average-draft-position simulator. I'm sure I could compute the
probability given enough time (and ignoring pick preference) but honestly this
was way easier. Runs 10k simulations of a 10 man and 12 man draft with the provided
odds. Based on my other lottery script, but stripped down (slightly). Can be
expanded to take other arrangements pretty easily.
"""


PLAYERS_10 = 'a,b,c,d,e,f,g,h,i,j'.split(',')
PLAYERS_12 = 'a,b,c,d,e,f,g,h,i,j,k,l'.split(',')
ODDS_10 = [125, 120, 115, 110, 105, 95, 90, 85, 80, 75]
ODDS_12 = [116, 111, 105, 98, 92, 86, 80, 74, 68, 63, 57, 50]

LOTTERIED = 6


def adp_sim(odds=ODDS_10, players=PLAYERS_10):
    ball_pit = np.arange(1000)
    np.random.shuffle(ball_pit)
    selected_players = set()
    player_pick_dict = {}
    pick = 1
    i = 0
    combos = np.array(sum([[players[j]] * odds[j] for j in range(len(odds))], []))

    while pick <= LOTTERIED:
        ball_drawn = ball_pit[i]
        i += 1
        player_drawn = combos[ball_drawn]
        if player_drawn not in selected_players:
            selected_players.update(player_drawn)
            player_pick_dict.update({player_drawn: [pick]})
            pick += 1

    for player in players:
        if player not in selected_players:
            selected_players.update(player)
            player_pick_dict.update({player: [pick]})
            pick += 1

    return player_pick_dict


def build_df(simulation):
    return pd.DataFrame.from_dict(simulation).reset_index(drop=True)


def adp_chart(odds=ODDS_10, players=PLAYERS_10, trials=10000):
    trials = [build_df(adp_sim(odds, players)) for i in range(trials)]
    full_df = pd.concat(trials)
    print(full_df.mean(0))


if __name__ == '__main__':
    adp_chart()
    adp_chart(ODDS_12, PLAYERS_12)
