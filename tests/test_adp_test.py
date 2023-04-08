import pytest
from fantasydraftlottery import Lottery


PLAYERS_DICT = {
    "players": {
        "Alex K": [120, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        "Alison": [75,  [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]],
        "Alex W": [100, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        "Chris":  [90,  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        "James":  [100, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
        "John":   [110, [3, 10, 9, 8, 7, 6, 2, 1, 4, 5]],
        "Neil":   [125, [4, 2, 3, 1, 5, 6, 7, 8, 9, 10]],
        "Ravi":   [85,  [4, 5, 6, 7, 3, 2, 1, 8, 9, 10]],
        "Rohan":  [115, [1, 2, 3, 4, 5, 6, 10, 9, 8, 7]],
        "Sahil":  [80,  [6, 7, 10, 8, 4, 3, 5, 1, 2, 9]]
    },
    "placement": "Ravi,Chris,Rohan,John,Neil,Alex K,Alex W,James,Sahil,Alison"
}
LOTTERIED = 4

lotto = Lottery(PLAYERS_DICT, LOTTERIED)
lotto.run()


def test_lotto_size():
    assert len(lotto.pick_messages)/2 == len(PLAYERS_DICT['players'])

def test_df():
    pass

def test_balls():
    pass
