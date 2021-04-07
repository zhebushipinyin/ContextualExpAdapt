#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(p=None,
             x_pair=None,
             condition='Random'
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p : list
        1-D list of series probabilities.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: random

    Returns
    -------
    df : DataFrame
    """
    if p is None:
        p = np.array([0.05, 0.25, 0.5, 0.75, 0.95])
    if x_pair is None:
        x_pair = np.array([(25, 0), (50, 0), (75, 0), (100, 0), (150, 0), (200, 0), (400, 0), (800, 0)])

    df = pd.DataFrame()
    df['p'] = np.tile(np.repeat(p, len(x_pair)), 5)
    df['x1'] = np.tile(np.tile(x_pair[:, 0], len(p)), 5)
    df['x2'] = np.tile(np.tile(x_pair[:, 1], len(p)), 5)
    df['condition'] = condition
    df['ratio'] = np.repeat([0.1, 0.3, 0.5, 0.7, 0.9], len(p)*len(x_pair))
    df['sure'] = df['ratio']*(df.x1-df.x2)+df.x2
    if condition == 'Random':
        df = df.sample(frac=1)
    else:
        raise ValueError("condition must be random")
    df.index = range(len(df))
    # df['block'] = df.index // 33 + 1
    return df


def generate_train(p=None,
             x_pair=None,
             condition='Random'
             ):
    """
    Generate exp data for training
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    p : list
        1-D list of series probabilities.
    x_pair : array
        values for probabilities, (x1, x2)
    condition : str
        exp condition: random

    Returns
    -------
    df : DataFrame
    """
    if p is None:
        p = np.array([0.25, 0.75])
    if x_pair is None:
        x_pair = np.array([[100, 0]])

    df = pd.DataFrame()
    df['p'] = np.tile(np.repeat(p, len(x_pair)), 5)
    df['x1'] = np.tile(np.tile(x_pair[:, 0], len(p)), 5)
    df['x2'] = np.tile(np.tile(x_pair[:, 1], len(p)), 5)
    df['condition'] = condition
    df['ratio'] = np.repeat([0.1, 0.3, 0.5, 0.7, 0.9], len(p)*len(x_pair))
    df['sure'] = df['ratio']*(df.x1-df.x2)+df.x2
    df = df.sample(frac=1)
    df.index = range(len(df))

    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')