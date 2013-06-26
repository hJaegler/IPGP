#/usr/bin/env python

'''
Created on 21 juin 2013
clique sur le graph pour afficher des barres verticales et enregistrer les coordonn'ees des donn'ees point'ees.
Choix des param`etres 'a calculer
@author: hugojaegler
'''

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from obspy.core import read


X = read('ABU.20071031.Ts')


enregx=[]
enregy=[]

class LineBuilder : 
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
    def __call__(self, event):
        print 'click', event
        if event.inaxes!=self.line.axes: return
        self.xs = [event.xdata, event.xdata]
        self.ys = [ymin, ymax]
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        return True

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on graphic to store data')
line, = ax.plot(np.arange(0, len(X[0])) , X[0].data, 'k')
plt.xlim(0, len(X[0]))
ymin, ymax = plt.ylim(X[0].data.min()*1.1, X[0].data.max()*1.1)


def onclick(event): 
    enregx.append(event.xdata)
    enregy.append(X[0].data[event.xdata])
    vlines(event.xdata, ymin, ymax, color='k', linestyles='dashed')
fig.canvas.mpl_connect('button_press_event', onclick)

line, = ax.plot([0], [0])
linebuilder = LineBuilder(line)



fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on point to select parameters')
ax.set_axis_off()

nbrParameters = 10
select_para = []
x=[]
for i in range(nbrParameters): 
    x.append(0)
    select_para.append(0)
    ax.text(0.05, i, "parameter number %d" %(i+1))

line, = ax.plot(x, range(nbrParameters), 'ws', markersize = 20, picker = 15)
ax.axis([-0.1, 0.8 , -0.5, nbrParameters*1.001]) 

def onpick(event):
    if event.artist != line : return True
    ind = event.ind
    select_para[ind]=1
    print 'You choose parameter number:', int(ind+1)

fig.canvas.mpl_connect('pick_event',onpick) 


plt.show()

print enregx
print enregy
