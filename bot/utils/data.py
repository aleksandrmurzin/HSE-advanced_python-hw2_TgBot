"""Configuration for the Telegram bot."""

import os

import pandas as pd


class Rating:
    def __init__(self, path=None, file=None):
        """ """
        self._scores = None
        self.path = path if path else "data"
        self.file = file if file else "scores.csv"
        self.file_path = os.path.join(self.path, self.file)

        self.file_check()

    def file_check(self):
        """ """
        if not os.path.exists(self.file_path):
            if not os.path.isdir(self.path):
                os.mkdir(self.path)

            schema = {"user_id": [], "score": [], "dt": []}
            pd.DataFrame(data=schema).to_csv(self.file_path, index=False)

    @property
    def scores(self):
        """
        :return:
        """
        self._scores = pd.read_csv(self.file_path)
        return self._scores

    def update(self, *args):
        """ """
        self._update(*args)

    def _update(self, user, score, dt):
        """
        :param user: user
        :param score: score
        :param dt: dt
        """
        tmp = self.scores
        tmp.loc[len(tmp), :] = [user, score, dt]
        tmp.to_csv(self.file_path, index=False)

    @property
    def statistics(self):
        """
        :return:
        """
        return self.evaluate()["message"]

    def evaluate(self):
        """
        :return:
        """
        tmp = self.scores

        if len(tmp) == 0:
            return {"message": None}
        results = {
            "message": {
                "average_rating": round(tmp["score"].mean(), 0),
            }
        }

        return results


ratings = Rating()
