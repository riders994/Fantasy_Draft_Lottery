import pandas as pd
import json
import yaml
import numpy as np


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


TEST_CONFIGS = {
    'A': {
        'ballers': {
            '0': 20,
            '1': 10
        },
        'picks': 2
    },
    'B': {
        'ballers': {
            '0': 20,
            '1': 10
        },
        'picks': 4
    },
}


class ADPTest:

    test_cases = dict()
    trial_summaries = dict()

    def __init__(self):
        pass

    @staticmethod
    def _read_file(loc, fmt):
        with open(loc) as file:
            if fmt[0] == 'y':
                return yaml.load(file, Loader=yaml.FullLoader)
            if fmt[0] == 'j':
                return json.load(file)

    def ingest_individ_config(self, config, fmt, name=None):
        fmt.lower()
        if fmt[0] == 'd':
            test_case = config
        elif fmt[0] in {'y', 'j'}:
            test_case = self._read_file(config, fmt)
        if name:
            self.test_cases.update({name: test_case})
        else:
            self.test_cases.update({'test_{}'.format(len(self.test_cases)): test_case})

    def ingest_full_config(self, config, fmt):
        fmt.lower()
        if fmt[0] == 'd':
            draft = config
        elif fmt[0] in {'y', 'j'}:
            draft = self._read_file(config, fmt)
        self.test_cases.update(draft)

    @staticmethod
    def _run_one(lotteried, combos, ball_pit, players):
        np.random.shuffle(ball_pit)
        selected_players = set()
        pick = 1
        i = 0
        res = dict()

        while pick < lotteried:
            ball = ball_pit[i]
            drawn = ordinal(int(combos[ball]) + 1)
            if drawn not in selected_players:
                res.update({drawn: pick})
                selected_players.update({drawn})
                pick += 1
            i += 1

        for p in players:
            if p not in selected_players:
                selected_players.update(p)
                res.update({p: pick})
                pick += 1
        return res

    def simulate(self, n):
        for name, test_case in self.test_cases.items():
            ballers = test_case['ballers']
            picks = test_case['picks']
            lotteried = len(ballers)
            trials = dict()

            players = [ordinal(p + 1) for p in range(picks)]
            balls = 0
            combos = np.array([])
            for order, ball_count in ballers.items():
                balls += ball_count
                combos = np.append(combos, [int(order)] * ball_count)
            ball_pit = np.arange(balls)
            for i in range(n):
                trials.update({str(i): self._run_one(lotteried, combos, ball_pit, players)})
            trial_frame = pd.DataFrame(trials)
            self.trial_summaries.update({name: trial_frame.mean(1)})

    def run(self, runs=10000):
        self.simulate(runs)
        res = pd.DataFrame(self.trial_summaries)
        print(res)
        return res


if __name__ == '__main__':
    t = ADPTest()
    t.ingest_full_config('./tests/test_configs/adp_test_config.yml', 'y')
    t.run()
    print('done')
