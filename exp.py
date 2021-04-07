#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from helpers import *
from trial_func import *


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)
# A: expand, B: shrink, C: large, D: small
myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152', '2560*1440'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
resolution = ok_data[3]

w, h = resolution.split('*')
w = int(w)
h = int(h)

df = generate()
df_tr = generate_train()
df['pix_w'] = w
df['pix_h'] = h
a = 3*w / 20.
b = h / 12.
results = {
    'x1':[], 'p':[], 'sure':[], 'ratio':[],
    'choice': [], 'rt': [], 'id':[], 'pre_false':[]
    }

font = 'MicroSoft Yahei'
# font = 'Noto Sans Mono CJK SC Regular'
win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0])

# Confirm button
ok = visual.TextStim(win, text=u"确认", pos=(0, -3*h/8), height=h / 36, font=font)
ok_shape = visual.ShapeStim(win, lineColor=[0.8, 0.8, 0.8], lineWidth=2)
ok_shape.vertices = [[-0.5 * a, -5 * b], [-0.5 * a, -4 * b], [0.5 * a, -4 * b], [0.5 * a, -5 * b]]
buttons = [ok, ok_shape]
# 时间间隔
t_trial = {'t_fix': 0.5}
# 文本
txt = visual.TextStim(win, font=font, wrapWidth=10000)
txt.height = 64 * h / 720
txt.pos = [0, h / 4]

text = visual.TextStim(win, height=64 * h / 720, pos=(0, 0), wrapWidth=10000, font=font)
# 注视点
fix = visual.ImageStim(win, image="img/fix.png", size=64 * h / 720)
# 指导语
pic = visual.ImageStim(win, size=(w, h))
# slider
# 指导语
while True:
    for i in range(2):
        pic.image = 'img/introduction_%s.png' % (i + 1)
        pic.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        event.clearEvents()
    text.text = u"按【空格键】进入决策实验练习"
    text.draw()
    win.flip()
    key = event.waitKeys(keyList=['space', 'escape'])
    if 'space' in key:
        event.clearEvents()
        break
    event.clearEvents()
# training
clk = core.Clock()
myMouse = event.Mouse()
for i in range(len(df_tr)):
    x = df_tr.loc[i, 'x1']
    y = df_tr.loc[i, 'x2']
    fix.draw()
    win.flip()
    core.wait(0.2)
    win.flip()
    re = trial(i, win, df_tr, clk, txt)
    print(re )
    win.flip()
    core.wait(0.3)

text.text = '按【空格键】进入正式实验'
text.draw()
win.flip()
key = event.waitKeys(keyList=['space', 'escape'])

clk.reset()
for i in range(len(df)):
    if i in (np.array([130]) - 1):
        text.text = '休息一下（10s后可按空格键继续）'
        text.draw()
        win.flip()
        core.wait(10)
        key = event.waitKeys(keyList=['space', 'escape'])
    fix.draw()
    win.flip()
    core.wait(0.2)
    win.flip()
    re = trial(i, win, df, clk, txt)
    results = append_results(results, re, i)
    win.flip()
    core.wait(0.5)
dfre = pd.DataFrame(results)
dfre['part']=1
# 主动报告错误的试次
for each in np.unique(dfre.loc[dfre.pre_false>0, 'pre_false']):
    re = trial(each, win, df, clk, txt)
    win.flip()
    core.wait(0.5)
    dfre.loc[dfre.id == each, 'choice'] = re['choice']
    dfre.loc[dfre.id == each, 'rt'] = re['rt']
    dfre.loc[dfre.id == each, 'pre_false'] = -2
df1 = pd.pivot_table(dfre, values='choice', index=['p','x1'], columns='ratio')
df1['b']=df1[0.1]+2*df1[0.3]+4*df1[0.5]+8*df1[0.7]+16*df1[0.9]
df11 = df1.loc[~df1.b.isin([0,16,24,28,30,31])].copy()
index = df11.index
if len(index)>0:
    results2 = {
        'x1': [], 'p': [], 'sure': [], 'ratio': [],
        'choice': [], 'rt': [], 'id': [], 'pre_false': []
    }
    dfx = []
    for pi, xi in index:
        dfx.append(df.loc[(df.p==pi)&(df.x1==xi)].copy())
    dfx = pd.concat(dfx)
    dfx.index = range(len(dfx))
    dfx = dfx.sample(frac=1)
    dfx.index = range(len(dfx))
    for i in range(len(dfx)):
        fix.draw()
        win.flip()
        core.wait(0.2)
        win.flip()
        re = trial(i, win, dfx, clk, txt)
        results2 = append_results(results2, re, i)
        win.flip()
        core.wait(0.5)
    dfre2 = pd.DataFrame(results2)
    dfre2['part']=2
    df2 = pd.pivot_table(dfre2, values='choice', index=['p', 'x1'], columns='ratio')
    df2['b'] = df2[0.1] + 2 * df2[0.3] + 4 * df2[0.5] + 8 * df2[0.7] + 16 * df2[0.9]
    index_ = df2.loc[df2.b.isin([0, 16, 24, 28, 30, 31])].index.copy()
    if len(index_)>0:
        for each in index_:
            df1.loc[each, 'b']=df2.loc[each, 'b']
    dfre = pd.concat([dfre, dfre2])
    dfre.index = range(len(dfre))
text.text = '休息一下（20s后可按空格键继续）'
text.draw()
win.flip()
df1 = get_change(df1, dfre)
df_ = generate_second_trial(df1)
core.wait(20)
key = event.waitKeys(keyList=['space', 'escape'])
results3 = {
    'x1': [], 'p': [], 'sure': [], 'ratio': [],
    'choice': [], 'rt': [], 'id': [], 'pre_false': []
}
clk.reset()
for i in range(len(df_)):
    if i in (np.array([100]) - 1):
        text.text = '休息一下（10s后可按空格键继续）'
        text.draw()
        win.flip()
        core.wait(10)
        key = event.waitKeys(keyList=['space', 'escape'])
    fix.draw()
    win.flip()
    core.wait(0.2)
    win.flip()
    re = trial(i, win, df_, clk, txt)
    results3 = append_results(results3, re, i)
    win.flip()
    core.wait(0.5)
dfre3 = pd.DataFrame(results3)
dfre3['part']=3
dfre = pd.concat([dfre, dfre3])
dfre.index = range(len(dfre))
dfre.to_csv('exp_data/data_half_%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))

# 第二遍
df0 = df.sample(frac=1)
df0.index = range(len(df0))
clk.reset()
for i in range(len(df0)):
    if i in (np.array([1, 130]) - 1):
        text.text = '休息一下（10s后可按空格键继续）'
        text.draw()
        win.flip()
        core.wait(10)
        key = event.waitKeys(keyList=['space', 'escape'])
    fix.draw()
    win.flip()
    core.wait(0.2)
    win.flip()
    re = trial(i, win, df0, clk, txt)
    results = append_results(results, re, i)
    win.flip()
    core.wait(0.5)
dfre4 = pd.DataFrame(results)
dfre4['part']=4
# 主动报告错误的试次
for each in np.unique(dfre4.loc[dfre4.pre_false>0, 'pre_false']):
    re = trial(each, win, df0, clk, txt)
    win.flip()
    core.wait(0.5)
    dfre4.loc[dfre4.id == each, 'choice'] = re['choice']
    dfre4.loc[dfre4.id == each, 'rt'] = re['rt']
    dfre4.loc[dfre4.id == each, 'pre_false'] = -2
df1 = pd.pivot_table(dfre4, values='choice', index=['p','x1'], columns='ratio')
df1['b']=df1[0.1]+2*df1[0.3]+4*df1[0.5]+8*df1[0.7]+16*df1[0.9]
df11 = df1.loc[~df1.b.isin([0,16,24,28,30,31])].copy()
index = df11.index
if len(index)>0:
    results2 = {
        'x1': [], 'p': [], 'sure': [], 'ratio': [],
        'choice': [], 'rt': [], 'id': [], 'pre_false': []
    }
    dfx = []
    for pi, xi in index:
        dfx.append(df0.loc[(df0.p==pi)&(df0.x1==xi)].copy())
    dfx = pd.concat(dfx)
    dfx.index = range(len(dfx))
    dfx = dfx.sample(frac=1)
    dfx.index = range(len(dfx))
    for i in range(len(dfx)):
        fix.draw()
        win.flip()
        core.wait(0.2)
        win.flip()
        re = trial(i, win, dfx, clk, txt)
        results2 = append_results(results2, re, i)
        win.flip()
        core.wait(0.5)
    dfre5 = pd.DataFrame(results2)
    dfre5['part']=5
    df2 = pd.pivot_table(dfre5, values='choice', index=['p', 'x1'], columns='ratio')
    df2['b'] = df2[0.1] + 2 * df2[0.3] + 4 * df2[0.5] + 8 * df2[0.7] + 16 * df2[0.9]
    index_ = df2.loc[df2.b.isin([0, 16, 24, 28, 30, 31])].index.copy()
    if len(index_)>0:
        for each in index_:
            df1.loc[each, 'b']=df2.loc[each, 'b']
    dfre4 = pd.concat([dfre4, dfre5])
    dfre4.index = range(len(dfre4))
text.text = '休息一下（20s后可按空格键继续）'
text.draw()
win.flip()
df1 = get_change(df1, dfre4)
df_ = generate_second_trial(df1)
core.wait(20)
key = event.waitKeys(keyList=['space', 'escape'])
results3 = {
    'x1': [], 'p': [], 'sure': [], 'ratio': [],
    'choice': [], 'rt': [], 'id': [], 'pre_false': []
}
clk.reset()
for i in range(len(df_)):
    if i in (np.array([100]) - 1):
        text.text = '休息一下（10s后可按空格键继续）'
        text.draw()
        win.flip()
        core.wait(10)
        key = event.waitKeys(keyList=['space', 'escape'])
    fix.draw()
    win.flip()
    core.wait(0.2)
    win.flip()
    re = trial(i, win, df_, clk, txt)
    results3 = append_results(results3, re, i)
    win.flip()
    core.wait(0.5)
dfre6 = pd.DataFrame(results3)
dfre6['part']=6

# 主动报告错误的试次
for each in np.unique(dfre6.loc[dfre6.pre_false>0, 'pre_false']):
    re = trial(each, win, df0, clk, txt)
    dfre6.loc[dfre6.id == 'each', 'choice'] = re['choice']
    dfre6.loc[dfre6.id == 'each', 'rt'] = re['rt']
    dfre6.loc[dfre6.id == 'each', 'pre_false'] = -2
dfre = pd.concat([dfre, dfre4, dfre6])
dfre.index = range(len(dfre))
dfre['x2'] = 0
dfre['name'] = name
dfre['sex'] = sex
dfre['age'] = age
dfre.to_csv('exp_data/data_%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
text.text = "本实验结束，请呼叫主试"
text.draw()
win.flip()
core.wait(3)
win.close()
core.quit()