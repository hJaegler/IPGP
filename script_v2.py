#! user/hugojaegler/Obspy/bin/python
# _*_coding:Utf-8 _* 
'''
Created on 1 juil. 2013

@author: hugojaegler
'''

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from obspy.core import read
from Tkinter import *

class Interface(Frame):
    '''
    Interface graphique permettant de sélectionner les paramètres.

    '''

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, ** kwargs)
        self.pack(fill=BOTH)
             
        self.message = Label(fenetre, text="click on parameters")
        self.message.pack()  
          
        self.var_para1 = IntVar()
        self.case1 = Checkbutton(fenetre, text="Parameter 1", variable=self.var_para1)
        self.case1.pack()
        self.var_para2 = IntVar()
        self.case2 = Checkbutton(fenetre, text="Parameter 2", variable=self.var_para2)
        self.case2.pack()
        self.var_para3 = IntVar()
        self.case3 = Checkbutton(fenetre, text="Parameter 3", variable=self.var_para3)
        self.case3.pack()


        self.bouton_quitter = Button(fenetre, text="Quit", command=fenetre.quit)
        self.bouton_quitter.pack(side="right")


fenetre = Tk()
interface = Interface(fenetre)

      
interface.mainloop()

parameters=[0,0,0]     # Paramètres choisis
parameters[0],parameters[1], parameters[2]=interface.var_para1.get(), interface.var_para2.get(), interface.var_para3.get()

print parameters


'''
On va maintenant afficher le sismo. On peut pointer dessus. 
'''

X = read('ABU.20071031.Ts')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on graphic to store data')
line, = ax.plot(np.arange(0, len(X[0])) , X[0].data, 'k')
plt.xlim(0, len(X[0]))
ymin, ymax = plt.ylim(X[0].data.min()*1.1, X[0].data.max()*1.1)

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

def onclick(event): 
    enregx.append(event.xdata)
    enregy.append(X[0].data[event.xdata])
    vlines(event.xdata, ymin, ymax, color='k', linestyles='dashed')
fig.canvas.mpl_connect('button_press_event', onclick)


line, = ax.plot([0], [0])
linebuilder = LineBuilder(line)
plt.show()
print enregx    # Abscisse des points sélectionnés 
print enregy    # Ordonnées lues sur le sismo

if __name__ == '__main__':
    pass
