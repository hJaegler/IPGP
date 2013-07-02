#! user/hugojaegler/Obspy/bin/python
# _*_coding:Utf-8 _* 
'''
Created on 2 juil. 2013

@author: hugojaegler
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
        
        self.bouton_enregistrer = Button(self, text="Record and Quit", command=self.cb)
        self.bouton_enregistrer.pack()
        
    def create_cbuts(self):
        for index, item in enumerate(cbuts_text):
            self.var[index] = IntVar()
            cbuts.append(Checkbutton(self,text = 'parameter {}'.format(item), variable=self.var[index]))
            cbuts[index].pack()
            
    def cb(self):
        for index, item in enumerate(cbuts_text):
            cbuts_var[index] = self.var[index].get()
        self.quit()
        
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
On va maintenant demander d'entrer le nom du sismo. On affichera les paramètres de ce sismo 
ainsi que la courbe où l'on pourra pointer.
'''

X = read(raw_input('Which file\'s path ? ')) 

tr = X[0]

class RecapEtOptionsCalculs(Frame):
    '''
    #Interface graphique récapitulant les caractéristique du sismogramme
    #présentant les options de filtrage et de calculs du noyau de sensibilité 
    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        self.message = Label(self, text="Récapitulatif du sismogramme")
        self.message.pack()
        
        self.recap = Text(self, height =12, width = 70)
        self.recap.insert(INSERT, "network: {}\n".format(tr.stats.network))
        self.recap.insert(INSERT, "station: {}\n".format(tr.stats.station))
        self.recap.insert(INSERT, "location: {}\n".format(tr.stats.location))
        self.recap.insert(INSERT, "channel: {}\n".format(tr.stats.channel))
        self.recap.insert(INSERT, "starttime: {}\n".format(tr.stats.starttime))
        self.recap.insert(INSERT, "endtime: {}\n".format(tr.stats.endtime))
        self.recap.insert(INSERT, "sampling rate: {}\n".format(tr.stats.sampling_rate))
        self.recap.insert(INSERT, "delta: {}\n".format(tr.stats.delta))
        self.recap.insert(INSERT, "number points: {}\n".format(tr.stats.npts))
        self.recap.insert(INSERT, "calibration: {}\n".format(tr.stats.calib))
        self.recap.insert(INSERT, "format: {}\n".format(tr.stats._format))
        self.recap.pack()
        self.bouton_quitter = Button(self, text="continue", command=self.quit)
        self.bouton_quitter.pack(side="bottom")
        
fenetre = RecapEtOptionsCalculs()
fenetre.master.title("Recap et Options de Calculs")
fenetre.master.maxsize(300, 500)
fenetre.mainloop()


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
        line.figure.canvas.mpl_connect('button_press_event', self)
        
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
