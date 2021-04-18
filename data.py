import random as rnd

from flask import session

GUESS_MIN = 10
GUESS_MAX = 99
PYTHONESS_COUNT = 3
USER_HISTORY_KEY = "user_history"
PYTHONESS_HISTORY_KEY = "pythoness_history"
CONFIDENCE_LEVEL_KEY = "confidence_level"


class Model:
    def __init__(self):
        self.pythonesses = []  # list of Pythoness instances
        i = 0
        while i < PYTHONESS_COUNT:
            self.pythonesses.append(Pythoness(i))
            i += 1

    def result(self, selected_number: int):
        # store value to user history
        user_history_value = []
        if USER_HISTORY_KEY in session:
            user_history_value = session.get(USER_HISTORY_KEY)
        user_history_value.append(selected_number)
        session[USER_HISTORY_KEY] = user_history_value
        # calculate pythonesses results
        for pythoness in self.pythonesses:
            pythoness.result(selected_number)

    @property
    def user_history(self) -> []:
        if USER_HISTORY_KEY in session:
            return session.get(USER_HISTORY_KEY)
        return []


class Pythoness:
    def __init__(self, index: int):
        self.index = index
        self.name = "pythoness_" + str(index)
        self.guess = rnd.randint(GUESS_MIN, GUESS_MAX)

    def result(self, selected_number: int):
        # init properties
        confidence_level = 0
        history = []
        # get history
        if self.name in session:
            data_object = session.get(self.name)
            if CONFIDENCE_LEVEL_KEY in data_object:
                confidence_level = data_object[CONFIDENCE_LEVEL_KEY]
            if PYTHONESS_HISTORY_KEY in data_object:
                history = data_object[PYTHONESS_HISTORY_KEY]
        # calculate value
        if self.guess == selected_number:
            confidence_level += 1
        else:
            confidence_level -= 1
        # store result
        history.append(self.guess)
        session[self.name] = {CONFIDENCE_LEVEL_KEY: confidence_level,
                              PYTHONESS_HISTORY_KEY: history}
        # update guess
        self.guess = rnd.randint(GUESS_MIN, GUESS_MAX)

    @property
    def confidence_level(self) -> int:
        if self.name in session:
            data_object = session.get(self.name)
            if CONFIDENCE_LEVEL_KEY in data_object:
                return data_object[CONFIDENCE_LEVEL_KEY]
        return 0

    @property
    def history(self) -> []:
        if self.name in session:
            data_object = session.get(self.name)
            if PYTHONESS_HISTORY_KEY in data_object:
                return data_object[PYTHONESS_HISTORY_KEY]
        return []
