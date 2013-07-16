# -*- coding: Utf-8 -*-
'''
Created on 16 juil. 2013

@author: hugojaegler
'''

import numpy as np
import matplotlib.pyplot as plt
from pylab  import vlines
from obspy.core import read
import subprocess
from datetime import date
from Tkinter import Frame, BOTH, Label, Text, INSERT, Button, Checkbutton, IntVar, StringVar, Entry
  
          
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
        
    
class Path(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        global textPath
        opt=Frame(self, bd = 1)
        textPath = StringVar()

        lb1=Label(opt,text="Path ? ")
        entre = Entry(opt,textvariable=textPath)

        lb1.pack(side="left")
        entre.pack()
        opt.bouton_Valider = Button(self, text="Valider", command = affiche_recap)
        opt.bouton_Valider.pack(side = "bottom")
        opt.pack(side="top")


def affiche_recap():
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
            
            X=read(textPath.get())
            
            fRecap = Frame(self)
            self.recap = Text(fRecap, height =12, width = 70)
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
            fRecap.pack()            
            self.bouton_quitter = Button(self, text="continue", command=self.quit)
            self.bouton_quitter.pack(side="bottom")   
   
    fenetre = RecapEtOptionsCalculs()
    fenetre.master.title("Recap et Options de Calculs")
    fenetre.mainloop()


def generateFile():
    
    
    splited_path = textPath.get().split('.')
    with open('donnees.inf', 'w') as fichier:
        fichier.write('# 0a. Green function database information file (for a certain depth only for the instance)\n')
        text0a = raw_input('Green function database information file (for a certain depth only for the instance) ?')    
        fichier.write(text0a + '\n')
        fichier.write('# 0b. output directory (parentdir)\n')
        text0b = raw_input('output directory (parentdir) ?')
        fichier.write(text0b + '\n')
        fichier.write('# 1a. event name\n')
        fichier.write(splited_path[1] + '\n')
        fichier.write('# 1b. event latitude, longitude, depth (however, interpolation for depths won\'t be performed)\n')
        fichier.write(str(X[0].stats.sac.evla) + ", ")
        fichier.write(str(X[0].stats.sac.evlo) + ", ")
        fichier.write(str(X[0].stats.sac.evdp) + '\n')
        fichier.write('# 1c. Mrr, Mtt, Mpp, Mrt, Mrp, Mtp\n')
        fichier.write('1.0 1.0 0.0 1.0 0.0 1.0\n')
        fichier.write('# 2a. station name\n')
        text2a = raw_input('station name ?')
        fichier.write(text2a + '\n')
        fichier.write('# 2b. station latitude, longitude\n')
        fichier.write(str(X[0].stats.sac.stla) + ", ")
        fichier.write(str(X[0].stats.sac.stlo) + "\n")
        fichier.write('# 3. phase name\n')
        text3 = raw_input('phase name ?')
        fichier.write(text3 + '\n')
        fichier.write('# 4. component (Z,R,T)\n')
        fichier.write(splited_path[2] + '\n')
        fichier.write('# 5. seismic parameter (alpha, beta, or all for this version)\n#    if you choose "test" the program will only give you the synthetic\n#          (fort.13 in your directory too)\n')
        text5 = raw_input('seismic parameter (alpha, beta, all or test)')
        fichier.write(text5 + '\n')
        fichier.write('# 6a. Butterworth filter (if 1 on; if 0 off)\n')
        text6a = str(raw_input('Butterworth filter (if 1 : on; if 0 : off) ?'))
        fichier.write(text6a + '\n')
        fichier.write('# 6b. filter name (mandatory even if 6a. =0 )\n')
        text6b = raw_input('filter name ?')
        fichier.write(text6b + "\n")
        fichier.write('# 6c. if butterworth = 1; lowest freq., highest freq., number of poles\n#     if butterworth = 0; just comment out those parameters (subroutine won\'t read them)\n')
        if text6a == '1':
            text6c1 = str(raw_input('lowest frequence ?'))
            fichier.write(text6c1 + ", ")
            text6c2 = str(raw_input('highest frequence ?'))
            fichier.write(text6c2 + ", ")
            text6c3 = str(raw_input('number of poles ?'))
            fichier.write(text6c3 + '\n')
        else : fichier.write('#\n')
        fichier.write('# 7. time window t1, t2, t3, t4 \n#  (if t1=t2 and t3=t4, fwin(:) will be rectangular)\n#  (normally taper functions are sine functions)\n')
        text7_1 = str(raw_input('time window t1 ?'))
        fichier.write(text7_1 + ", ")
        text7_2 = str(raw_input('time window t2 ?'))
        fichier.write(text7_2 + ", ")
        text7_3 = str(raw_input('time window t3 ?'))
        fichier.write(text7_3 + '\n')
        text7_4 = str(raw_input('time window t4 ?'))
        fichier.write(text7_4 + '\n')
        fichier.write('# 8. itranslat (1 if you convert geodetic latitude to geocentric latitude)\n')
        text8 = str(raw_input('itranslat (1 if you convert geodetic latitude to geocentric latitude) ?'))
        fichier.write(text8 + '\n')
        fichier.write('#\n#\n#  Below are minor parameters for kernel calculations\n#                         (i.e. you can leave them as they are to start with)\n#\n# Aa. SINC interpolation window (ipdistance deg) (it works well with 10-20 degrees)\n')
        fichier.write('10.d0\n')
        fichier.write('# Ab. reducing slowness for interplation (c_red_reci s/deg) (if 0.d0 we do not perform slowness reduction)\n')
        fichier.write('0.d0\n')
        fichier.write('# Ba. fast FFT (if 1 on; if 0 off)\n#   you can re-define imin and imax for FFT of Green functions\n#   thence you can avoid reading frequencies for which you don\'t have to account.\n#\n')
        fichier.write('0\n')
        fichier.write('# Bb. if fast FFT = 1; lowest i(freq), highest i(freq) (note that freq = i(freq)/tlen)\n#     if fast FFT = 0; just comment out those parameters (subroutine won\'t read them)\n')
        fichier.write('#0  256 \n')
        fichier.write('# Ca. gridding and extent in R(longitudinal) direction (dph, ph1)\n')
        fichier.write('2.5d-1 5.d0\n')
        fichier.write('# Cb. gridding and extent in T(transverse) direction (dth, thw)\n')
        fichier.write('2.5d-1 5.d0\n')
        fichier.write('# Cd. gridding in radius (rmin, rmax, deltar : should correspond to grids in catalogue)\n# if you put 0.d0 0.d0 0.d0 then the program will take the grids in catalogue\n')
        fichier.write('0.d0 0.d0 0.d0\n')
        fichier.write('# Da. time window (start, end in sec)\n')
        fichier.write('0.d0 1.3d3\n')
        fichier.write('# Db. sampling Hz\n')
        fichier.write('2.d0\n')
        fichier.write('# Ea. ignoring criteria (calculrapide: we ignore the values below; if 0.d0 we don\'t use the algo)\n#         (in Fuji et al. 2012b, we chose 5.d-3)\n')
        fichier.write('0.d0\n')
        fichier.write('#\n# Eb. number of kernel types for the ignoring scheme (if Ea. = 0.d0, just comment out all)\n')
        fichier.write('1\n')
        fichier.write('# Ec. kernel type for ignoring scheme (if 0 we calculate for the envelop) note them vertically\n')
        fichier.write('0\n')
        fichier.write('# F. PSV/SH (PSV only = 2; SH only = 1; PSV+SH =3)\n')
        fichier.write('3\n')
        fichier.write('# don\'t forget write \'end\' at the end\n')
        fichier.write('end\n')
    
        today = date.today()
        strToday = str(today.year) + str(today.month) + str(today.day)
        newPath = (text2a + '.' + strToday + '.' + splited_path[2] + '.' + text3 + '.inf')
        subprocess.call('cp donnees.inf %s' % newPath, shell = True)
        subprocess.call('rm donnees.inf', shell = True)
    
    
    
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
    X = read("ABU.20071031.T")
    print(type(X))
    global textPath
    textPath = ""
    fenetrePath = Path()
    fenetrePath.master.title("Recap et Options de Calculs")
   
    fenetrePath.mainloop()
    
    generateFile()
    
   
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
