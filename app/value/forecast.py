import numpy as np

from sklearn import linear_model


class ForecastLR:
    @staticmethod
    def get_forecast(x, y):

        number_of_quarters = 12

        x_binary = np.array([])
        for d in range(1, x.size + 1):
            x_binary = np.append(x_binary, [d])

        y_flipped = np.flip(y)

        x_binary = x_binary.reshape(-1, 1)
        y_flipped = y_flipped.reshape(-1, 1)

        regr = linear_model.LinearRegression()
        regr.fit(x_binary, y_flipped)

        x_future = np.array([])
        for n in range(x_binary.size, x_binary.size + number_of_quarters):
            x_future = np.append(x_future, [n])
        x_future = x_future.reshape(-1, 1)

        return regr.predict(x_future)
