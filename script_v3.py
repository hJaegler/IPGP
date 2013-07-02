#! user/hugojaegler/Obspy/bin/python
# _*_coding:Utf-8 _* 
'''
Created on 1 juil. 2013

@author: hugojaegler
'''


'''

Interface graphique permettant le choix des paramètres

'''

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from obspy.core import read
from Tkinter import *


cbuts = []
cbuts_text = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
cbuts_var = []
for index in enumerate(cbuts_text) : 
    cbuts_var.append(0)

class Interface(Frame):
    '''
    Interface graphique permettant de sélectionner les paramètres.

    '''
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, ** kwargs)
        self.pack(fill=BOTH)
        self.var = []
        for index in enumerate(cbuts_text) : 
                self.var.append(0)
        self.message = Label(self, text="click on parameters")
        self.message.pack()
        self.create_cbuts()
        Button(self, text = 'select all', command = self.select_all).pack()
        Button(self, text = 'select none', command = self.deselect_all).pack()
        self.bouton_enregistrer = Button(self, text="Enregistrer", command=self.cb)
        self.bouton_enregistrer.pack()
        self.bouton_quitter = Button(self, text="Quit", command=self.quit)
        self.bouton_quitter.pack(side="bottom")
        
    def create_cbuts(self):
        for index, item in enumerate(cbuts_text):
            self.var[index] = IntVar()
            cbuts.append(Checkbutton(self,text = 'parameter {}'.format(item), variable=self.var[index]))
            cbuts[index].pack()
            
    def cb(self):
        for index, item in enumerate(cbuts_text):
            print "variable {} is {}".format(item, self.var[index].get())
            cbuts_var[index] = self.var[index].get()
        
    def select_all(self):
        for i in cbuts :
            i.select()
        
    def deselect_all(self):
        for i in cbuts : 
            i.deselect()
        
        
fenetre = Tk()
interface = Interface(fenetre)

      
interface.mainloop()
interface.destroy()
print cbuts_var



'''
On va maintenant demander d'entrer le nom du sismo afin de l'afficher et de pointer dessus. 
'''

X = read(raw_input('Which file\'s path ? ')) 

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
