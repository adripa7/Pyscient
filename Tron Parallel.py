import tkinter as tk
import random
import time
import numpy as np


Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

#############################################################
#
#  affichage en mode texte


def AffGrilles(G,X,Y):
    nbG, larg , haut = G.shape
    for y in range(haut-1,-1,-1) :
        for i in range(nbG) :
            for x in range(larg) :
               g = G[i]
               c = ' '
               if G[i,x,y] == 1 : c = 'M'  # mur
               if G[i,x,y] == 2 : c = 'O'  # trace
               if (X[i],Y[i]) == (x,y) : c ='X'  # joueur
               print(c,sep='', end = '')
            print(" ",sep='', end = '') # espace entre les grilles
        print("") # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

Debug = True
nb = 5 # nb de parties


def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI

    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        LPossibles = np.zeros((nb, 4), dtype=np.int8)
        Indices = np.zeros(nb, dtype=np.int8)

        Vdroite = G[I, X + 1, Y]
        Vgauche = G[I, X - 1, Y]
        Vhaut = G[I, X, Y + 1]
        Vbas = G[I, X, Y - 1]

        Vgauche = (Vgauche == 0) * 1
        LPossibles[I, Indices] = Vgauche
        Indices[(Vgauche == 1)] += 1

        Vhaut = (Vhaut == 0) * 2
        LPossibles[I, Indices] = Vhaut
        Indices[(Vhaut == 2)] += 1

        Vdroite = (Vdroite == 0) * 3
        LPossibles[I, Indices] = Vdroite
        Indices[(Vdroite == 3)] += 1

        Vbas = (Vbas == 0) * 4
        LPossibles[I, Indices] = Vbas
        Indices[(Vbas == 4)] += 1
        # marque le passage de la moto
        G[I, X, Y] = 2


        # Direction : 2 = vers le haut
        #Choix = np.ones(nb,dtype=np.uint8) * 2
        R = np.random.randint(12, size=nb)
        Indices[Indices==0]=1
        R = R%Indices

        Choix = LPossibles[I,R] #pour chaque partie je choisi une voie possible

        #DEPLACEMENT

        if (np.array_equal(Choix,np.zeros(nb, dtype=np.int8))) :
            return S
        else:

            DX = dx[Choix]
            DY = dy[Choix]
            if Debug : print("DX : ", DX)
            if Debug : print("DY : ", DY)
            X += DX
            Y += DY
            S += ds[Choix]


        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)

    print("Scores : ",np.mean(S))



Simulate(GameInit)

