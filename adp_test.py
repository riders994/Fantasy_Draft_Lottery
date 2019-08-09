import numpy as np
import pandas as pd


PLAYERS = 'a,b,c,d,e,f,g,h,i,j'.split(',')
ODDS_10 = [125, 120, 115, 110, 105, 95, 90, 85, 80, 75]
ODDS_12 = [116, 111, 105, 98, 92, 86, 80, 74, 68, 63, 57, 50]

ball_pit = np.arange(1000)

np.random.shuffle(ball_pit)

LOTTERIED = 6


def adp_sim(num=10, odds=ODDS_10):
    ball_pit = np.arange(1000)
    np.random.shuffle(ball_pit)
    selected_players = set()
    player_pick_dict = {}
    players = PLAYERS
    pick = 1
    i = 0
    if num == 12:
        players += ['k', 'l']

    combos = np.array(sum([[players[j]] * odds[j] for j in range(num)], []))

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


def adp_chart(num=10, odds=ODDS_10, trials=10000):
    trials = [build_df(adp_sim(num, odds)) for i in range(trials)]
    full_df = pd.concat(trials)
    print(full_df.mean(0))


if __name__ == '__main__':
    adp_chart()
    adp_chart(12, ODDS_12)
