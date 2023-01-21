from time import time

"""
Показ статистики по окончанию уровня или поражения, а так же победы
"""


class Stats:
    def __init__(self):
        self._start_time = time()
        self._kills = 0

    def update_kills(self):
        self._kills += 1

    def get_kills(self):
        return self._kills

    def total_time(self):
        return time() - self._start_time
