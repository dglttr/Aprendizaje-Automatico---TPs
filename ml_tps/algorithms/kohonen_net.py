import numpy as np
import pandas as pd
from typing import List


def row_to_array(row: pd.Series):
    return np.array(row.values)


class KohonenPerceptron:

    def __init__(self, df: pd.DataFrame):
        self.w = row_to_array(df.iloc[np.random.randint(0, len(df.index) - 1)])

    def get_value(self, pattern: pd.Series):
        return np.dot(self.w, row_to_array(pattern))

    def update_values(self, coef, pattern: pd.Series):
        self.w += coef * (row_to_array(pattern) - self.w)


class KohonenNet:

    def __init__(self):
        self.perceptrons: List[KohonenPerceptron] = []
        self.side = 0
        self.generations = 0
        self.alpha = 0.5

    def pick_winner(self, row: pd.Series):
        i = 0
        j = 0
        max_value = self.perceptrons[0].get_value(row)

        for i_ in range(self.side):
            for j_ in range(self.side):
                value = self.perceptrons[i_ * self.side + j_].get_value(row)
                if max_value < value:
                    i = i_
                    j = j_
                    max_value = value
        return i, j

    def sigma(self):
        return 1/self.generations

    def eta(self):
        return self.generations ** -self.alpha

    def update(self, win_i: int, win_j: int, row: pd.Series):
        for i in range(self.side):
            for j in range(self.side):
                lambda_ = np.e ** -(((win_i - i)**2 + (win_j - j)**2) / (2 * self.sigma()))
                self.perceptrons[i * self.side + j].update_values(self.eta() * lambda_, row)

    def fit(self, df: pd.DataFrame, side: int):
        """Fits the Kohonen model and sets the class variables.

        :param X: Data set to be clustered.
        :param side: Specifies the side of the square Kohonen net.
        """
        self.perceptrons = [KohonenPerceptron(df) for _ in range(side*side)]
        self.side = side
        self.generations = 1

        stop = False
        while not stop:
            #          shuffle
            np.random.shuffle(df.values)
            for idx, row in df.iterrows():
                win_i, win_j = self.pick_winner(row)
                self.update(win_i,win_j,row)
            self.generations += 1
            stop = self.eta() < 1e1 # OR no changes

    def predict(self, data: pd.DataFrame):
        """Assigns each given example to the nearest net in the previously fitted model.

        :param data: Data to be assigned using the previously fitted clustering model.
        :return: Series containing the index number of each example's nearest cluster.
        """
        if self.perceptrons is []:
            raise ValueError("Model has not been fitted yet.")

        predictions = np.zeros((self.side, self.side))
        for idx, row in data.iterrows():
            i, j = self.pick_winner(row)
            predictions[i][j] += 1

        return predictions