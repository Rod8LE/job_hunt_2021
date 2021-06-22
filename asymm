import scipy
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import numpy as np
import tensorflow as tf


def showcase_pandas(input_list=None, showcase_print=True):
    if input_list is None:
        input_list = [1, 2, 3, 4, 5, 6, 1, 2, 8, 7, 4, 5, 9, 8]
    index = range(len(input_list))
    df = pd.DataFrame({'data': input_list}, index=index)
    df['above_5'] = df['data'] > 5
    df['index_equals_value'] = int(df.loc[df.index == df.data, 'data'])
    if showcase_print:
        print(df.head())
        print(df.groupby('data').sum())
    return df


def showcase_matplotlib(df=showcase_pandas(input_list=None, showcase_print=False)):
    x_axis = df.index
    fig, ax = plt.subplots()
    ax.plot(x_axis, df.data, label='data')
    ax.plot(x_axis, df.above_5, label='above_5')
    ax.set_xlabel('dummy Data Frame index')
    ax.set_ylabel('dummy values')
    ax.set_title("matplotlib dummy plot")
    ax.legend()
    plt.show()
    return None


def showcase_sklearn():
    return None


def showcase_tf():
    return None
