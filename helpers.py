#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

def lo(x):
    return np.log(x/(1-x))


def lo2p(x):
    return 1/(1+np.exp(-x))


def append_results(result, re, i):
    """
    append results of one trial
    :param result: list of results
    :param re: result of one trial
    :param i: trial index
    :return: result
    """
    result['choice'].append(re['choice'])
    result['rt'].append(re['rt'])
    result['id'].append(i)
    result['x1'].append(re['x'])
    result['p'].append(re['p'])
    result['sure'].append(re['sure'])
    result['ratio'].append(re['ratio'])
    result['pre_false'].append(re['pre_false'])

    return result


def get_change(df, df_re):
    """
    Run a trial of given data
    Returns the values recorded

    Parameters
    ----------
    df : pd.DataFrame
        pivot_table of exp data
    df_re : pd.DataFrame
        exp data

    Returns
    -------
    result : pd.DataFrame
    """
    df.loc[df.b == 0, ['q', 'q1', 'q2']] = [0.95, 0.8, 1]
    df.loc[df.b == 16, ['q', 'q1', 'q2']] = [0.8, 0.7, 0.9]
    df.loc[df.b == 24, ['q', 'q1', 'q2']] = [0.6, 0.5, 0.7]
    df.loc[df.b == 28, ['q', 'q1', 'q2']] = [0.4, 0.3, 0.5]
    df.loc[df.b == 30, ['q', 'q1', 'q2']] = [0.2, 0.1, 0.3]
    df.loc[df.b == 31, ['q', 'q1', 'q2']] = [0.05, 0, 0.2]
    index_ = df.loc[~df.b.isin([0, 16, 24, 28, 30, 31])].index.copy()
    if len(index_)>0:
        for p, x1 in index_:
            dfi = df_re.loc[(df_re.p==p)&(df_re.x1==x1)]
            dfi.index = range(len(dfi))
            dfi.loc[len(dfi), ['ratio', 'choice']] = [0.999, 1]
            dfi.loc[len(dfi)+1, ['ratio', 'choice']] = [0.001, 0]
            dfi['lr'] = lo(dfi.ratio)
            model = smf.glm(formula='choice~lr', data=dfi,
                            family=sm.families.Binomial(link=sm.families.links.logit())).fit()
            q = np.clip(np.round(lo2p(-model.params[0] / model.params[1]), 1), 0.1, 0.9)
            df.loc[(p, x1), ['q', 'q1', 'q2']] = [q, q-0.1, q+0.1]
    return df


def generate_second_trial(df):
    """
    generate second data
    :param df: pivot_table of exp data with change point
    :return: pd.DataFrame
    """
    index = df.index.values
    re = {
        'p':[],
        'x1':[],
        'ratio':[]
    }
    for each in index:
        for r in [0.02, 0.06, 0.1, 0.14, 0.18]:
            re['p'].append(each[0])
            re['x1'].append(each[1])
            re['ratio'].append(df.loc[each, 'q1']+r)
    df_new = pd.DataFrame(re)
    df_new['x2'] = 0
    df_new['sure'] = np.round(df_new['ratio']*(df_new.x1-df_new.x2)+df_new.x2, 1)
    df_new = df_new.sample(frac=1)
    df_new.index = range(len(df_new))
    return df_new
