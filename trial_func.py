#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import numpy as np


def trial(i, win, df, clk, txt):
    """
    Run a trial of given data
    Returns the values recorded

    Parameters
    ----------
    i : int
        trial number
    win : visual.Window
        windows created by psychopy
    df : pd.DataFrame
        Exp data contains gambles and conditions
    clk : core.Clock
        clock to record time
    txt: visual.TextStim
        text stim

    Returns
    -------
    result : list
    """
    p = df.loc[i, 'p']
    x = df.loc[i, 'x1']
    y = df.loc[i, 'x2']
    sure = df.loc[i, 'sure']
    ratio = df.loc[i, 'ratio']
    w, h = win.size
    result = {
    }
    loc = [-1,1]
    np.random.shuffle(loc)
    #txt.text = "%s%%，%s元 \n %s%%，%s元" % (int(100 * p), int(x), 100 - int(100 * p), int(y))
    txt.text = '{:>2d}%, {:>3d}元\n{:>2d}%, {:>3d}元'.format(int(100 * p), int(x), 100 - int(100 * p), int(y))

    # txt.text = "%s%%，%s元" % (int(100 * p), int(x))
    txt.pos = (0.2*loc[0]*w, 0)
    txt.draw()
    if sure-int(sure)!= 0:
        sure_t = sure
    else:
        sure_t = int(sure)
    txt.text = "%s元" % sure_t
    txt.pos = (0.2*loc[1]*w, 0)
    txt.draw()
    win.flip()
    clk.reset()
    key = event.waitKeys(keyList=['f', 'j', 'escape','space'])
    rt = clk.getTime()
    result['pre_false']=-1
    if 'escape' in key:
        win.flip()
        win.close()
        core.quit()
    elif 'space' in key:
        result['pre_false'] = i-1
        key = event.waitKeys(keyList=['f', 'j'])
        rt = clk.getTime()
    if rt<0.5:
        txt.text = "按键过快！"
        txt.pos = (0, 0)
        txt.draw()
        win.flip()
        core.wait(0.5)
        # txt.text = "%s%%，%s元 \n %s%%，%s元" % (int(100 * p), int(x), 100 - int(100 * p), int(y))
        txt.text = '{:>2d}%, {:>3d}元\n{:>2d}%, {:>3d}元'.format(int(100 * p), int(x), 100 - int(100 * p), int(y))
        # txt.text = "%s%%，%s元" % (int(100 * p), int(x))
        txt.pos = (0.2 * loc[0] * w, 0)
        txt.draw()
        txt.text = "%s元" % sure_t
        txt.pos = (0.2 * loc[1] * w, 0)
        txt.draw()
        win.flip()
        clk.reset()
        key = event.waitKeys(keyList=['f', 'j'])
        rt = clk.getTime()

    if loc[1] == 1:
        # sure在右边
        if 'j' in key:
            # 选择右边
            choice = 1  # 选择了确定金额
        elif 'f' in key:
            choice = 0
    else:
        if 'j' in key:
            choice = 0
        elif 'f' in key:
            choice = 1

    result['choice'] = choice
    result['rt'] = rt
    result['x'] = x
    result['p'] = p
    result['sure'] = sure
    result['ratio'] = ratio
    return result


