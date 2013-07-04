#! user/hugojaegler/Obspy/bin/python
# -*- coding: Utf-8 -*-
'''
Created on 2 juil. 2013

@author: hugojaegler
'''

import numpy as np
import matplotlib.pyplot as plt
from pylab  import vlines
from obspy.core import read
from Tkinter import *

        
class Interface(Frame):
    '''
    Interface graphique permettant de selectionner les parametres.

    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        
        self.var = []
        for index in enumerate(cbuts_text) : 
            self.var.append(0)
                
        self.message = Label(self, text="click on parameters")
        self.message.pack()
        
        self.create_cbuts()
        
        self.Button_select = Button(self, text = 'select all', command = self.select_all)
        self.Button_select.pack()
        self.Button_deselect = Button(self, text = 'select none', command = self.deselect_all)
        self.Button_deselect.pack() 
        
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

class RecapEtOptionsCalculs(Frame):
    '''
    Interface graphique recapitulant les caracteristique du sismogramme
    presentant les options de filtrage et de calculs du noyau de sensibilite
    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        self.message = Label(self, text="Recapitulatif du sismogramme")
        self.message.pack()
        
        self.recap = Text(self, height =12, width = 70)
        self.recap.insert(INSERT, "network: {}\n".format(X[0].stats.network))
        self.recap.insert(INSERT, "station: {}\n".format(X[0].stats.station))
        self.recap.insert(INSERT, "location: {}\n".format(X[0].stats.location))
        self.recap.insert(INSERT, "channel: {}\n".format(X[0].stats.channel))
        self.recap.insert(INSERT, "starttime: {}\n".format(X[0].stats.starttime))
        self.recap.insert(INSERT, "endtime: {}\n".format(X[0].stats.endtime))
        self.recap.insert(INSERT, "sampling rate: {}\n".format(X[0].stats.sampling_rate))
        self.recap.insert(INSERT, "delta: {}\n".format(X[0].stats.delta))
        self.recap.insert(INSERT, "number points: {}\n".format(X[0].stats.npts))
        self.recap.insert(INSERT, "calibration: {}\n".format(X[0].stats.calib))
        self.recap.insert(INSERT, "format: {}\n".format(X[0].stats._format))
        self.recap.pack()
        self.bouton_quitter = Button(self, text="continue", command=self.quit)
        self.bouton_quitter.pack(side="bottom")    

class LineBuilder :
    '''
    Fonction permettant de creer des lignes verticales sur un sismo et
    d'enregistrer les coordonees des endroits pointes sur la courbe
    ''' 
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
        
 
 
 
def main():
    
    '''
    Premiere partie : interface graphique permettant de choisir les parametres
    '''
    global cbuts
    cbuts = []
    global cbuts_text 
    cbuts_text = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    global cbuts_var 
    cbuts_var= []


    for index in enumerate(cbuts_text) : 
        cbuts_var.append(0)
        
    interface = Interface()

    interface.mainloop()
    interface.destroy()
    print cbuts_var
    
    '''
    Deuxieme partie : l'utilisateur entre le chemin du sismo. On affiche
    alors les caracteristiques du sismo
    '''
    global X
    X = read(raw_input('Which file\'s path ? ')) 
    
    fenetre = RecapEtOptionsCalculs()
    fenetre.master.title("Recap et Options de Calculs")
    fenetre.master.maxsize(300, 500)
    fenetre.mainloop()
   
    '''
    Troisieme partie : on affiche le sismo. L'utilisateur peut pointer
    sur le sismo et on enregistrer ces coordonnees sur la courbe.
    '''

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click on graphic to store data')
    line, = ax.plot(np.arange(0, len(X[0])) , X[0].data, 'k')
    plt.xlim(0, len(X[0]))
    global ymin
    global ymax
    ymin, ymax = plt.ylim(X[0].data.min()*1.1, X[0].data.max()*1.1)
    
    global enregx
    global enregy
    enregx=[]
    enregy=[]

   
    fig.canvas.mpl_connect('button_press_event', onclick)


    line, = ax.plot([0], [0])
    linebuilder = LineBuilder(line)
    plt.show()

    print enregx    # Abscisse des points selectionnes 
    print enregy    # Ordonnees lues sur le sismo
    

if __name__ == '__main__':
    main()
