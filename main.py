import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model


from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def train_and_predict(train_input_features, train_outputs, prediction_features):
    """
    :param train_input_features: (numpy.array) A two-dimensional NumPy array where each element
                        is an array that contains two numerical features
    :param train_outputs: (numpy.array) A one-dimensional NumPy array where each element
                        is the value associated with the same row of train_input_features
    :param prediction_features: (numpy.array) A two-dimensional NumPy array where each element
                        is an array that contains two numerical features
    :returns: (list) The function should return an iterable (like list or numpy.ndarray) of predictions,
                        one for each item in prediction_features
    """
    model = make_pipeline(PolynomialFeatures(degree=2), Ridge())
    model.fit(train_input_features, train_outputs)
    return model.predict(prediction_features)

#Example case
np.random.seed(1)
data = np.random.normal(size=(200, 2))
result = 2 * data[:, 0] ** 3 + 4 * data[:, 1]
X_train, X_test, y_train, y_test = train_test_split(data, result,
                                                    test_size=0.3, random_state=0)


y_pred = train_and_predict(X_train, y_train, X_test)
if y_pred is not None:
    print(metrics.mean_squared_error(y_test, y_pred))
    print(":)")
