"""
Exact pick-by-pick odds (and therefore exact ADP) for a lottery config.

The lottery draws balls without replacement and skips names it has already
pulled, which is the same thing as weighted sampling without replacement. With
16 players, 9 of whom own any balls at all, and 5 lotteried picks, there are
only 9*8*7*6*5 = 15,120 possible lottery orders -- few enough to walk every one
of them and add up its probability instead of simulating. Everything below the
lottery is deterministic: the leftover picks go out in reverse placement order.

Run it to dump the two chart tables to JSON:
    python -m fantasydraftlottery.adp_charts [lotteried] [out.json]
"""

import json
import sys
from collections import defaultdict

from .draftorder import PLAYERS_DICT, Lottery, ordinal


def _draft_order(player_dict, lotteried):
    """Reverse-placement order used to fill the picks the lottery didn't."""
    placement = player_dict['placement'].split(',')
    placement.reverse()
    return placement


def exact_distribution(player_dict, lotteried):
    """P(player lands on pick) for every player/pick pair.

    Returns (players, matrix) where matrix[name][i] is the probability that
    `name` ends up with pick i + 1.
    """
    players = player_dict['players']
    placement = _draft_order(player_dict, lotteried)
    player_num = len(placement)
    weights = {name: prefs[0] for name, prefs in players.items()}
    contenders = [name for name in placement if weights.get(name, 0) > 0]

    # More lotteried picks than names with balls would spin _lottery forever.
    lotteried = min(lotteried, len(contenders))

    dist = {name: [0.0] * player_num for name in placement}

    def record(drawn, prob):
        order = drawn + [name for name in placement if name not in drawn]
        for pick_index, name in enumerate(order):
            dist[name][pick_index] += prob

    def walk(drawn, drawn_set, pool_weight, prob):
        if len(drawn) == lotteried:
            record(drawn, prob)
            return
        for name in contenders:
            if name in drawn_set:
                continue
            w = weights[name]
            drawn.append(name)
            drawn_set.add(name)
            walk(drawn, drawn_set, pool_weight - w, prob * w / pool_weight)
            drawn.pop()
            drawn_set.discard(name)

    walk([], set(), sum(weights[name] for name in contenders), 1.0)
    return placement, dist


def adp(dist):
    """Average draft position: the expected pick number for each player."""
    return {name: sum((i + 1) * p for i, p in enumerate(probs))
            for name, probs in dist.items()}


def quantile(probs, q):
    """Lowest pick whose cumulative probability reaches q."""
    total = 0.0
    for i, p in enumerate(probs):
        total += p
        if total >= q - 1e-12:
            return i + 1
    return len(probs)


def simulate(player_dict, lotteried, trials=20000, seed=None):
    """Monte Carlo over the real Lottery class, to check the exact math."""
    import numpy as np

    if seed is not None:
        np.random.seed(seed)
    placement = _draft_order(player_dict, lotteried)
    counts = {name: [0] * len(placement) for name in placement}
    for _ in range(trials):
        lotto = Lottery(player_dict, lotteried)
        # Lottery keeps its bookkeeping on the class, not the instance, so a
        # fresh run needs its own copies or every trial piles onto the last.
        lotto.messages = []
        lotto.pick_messages = []
        lotto.taken_picks = {0}
        lotto.selected_players = []
        lotto.player_pick_dict = {}
        lotto.winner = None
        lotto.tracker = defaultdict(int)
        lotto.run(proba=False)
        for pick in range(1, len(placement) + 1):
            counts[lotto.player_pick_dict[ordinal(pick)]][pick - 1] += 1
    return {name: [c / trials for c in row] for name, row in counts.items()}


def build_tables(player_dict=PLAYERS_DICT, lotteried=5):
    placement, dist = exact_distribution(player_dict, lotteried)
    means = adp(dist)
    balls = {name: prefs[0] for name, prefs in player_dict['players'].items()}
    total_balls = sum(balls.values())
    rows = []
    for name in sorted(placement, key=lambda n: means[n]):
        probs = dist[name]
        picks = [i + 1 for i, p in enumerate(probs) if p > 0]
        rows.append({
            'name': name,
            'balls': balls.get(name, 0),
            'odds': balls.get(name, 0) / total_balls,
            'adp': means[name],
            'best': min(picks),
            'worst': max(picks),
            'p10': quantile(probs, 0.10),
            'median': quantile(probs, 0.50),
            'p90': quantile(probs, 0.90),
            'probs': probs,
        })
    return {
        'lotteried': lotteried,
        'picks': len(placement),
        'total_balls': total_balls,
        'players': rows,
    }


if __name__ == '__main__':
    lotteried = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    tables = build_tables(PLAYERS_DICT, lotteried)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    if out:
        with open(out, 'w') as fh:
            json.dump(tables, fh)
    width = max(len(r['name']) for r in tables['players'])
    print('{:<{w}} {:>6} {:>7} {:>6}  {}'.format(
        'player', 'balls', 'odds', 'adp', 'range', w=width))
    for r in tables['players']:
        print('{:<{w}} {:>6} {:>6.2%} {:>6.2f}  {}-{}'.format(
            r['name'], r['balls'], r['odds'], r['adp'], r['best'], r['worst'], w=width))
