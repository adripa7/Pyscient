import tkinter as tk
import random
import numpy as np
import copy
import random
import time

#################################################################################
#
#   Données de partie

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
GInit  = np.flip(GInit,0).transpose() #coordonnées (0,0)

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )
   
    
    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI 

#fonction qui simule les autres parties// retourne un score
""" Ancienne version de Simulation 

def SimulationPartie (Game):

    x, y = Game.PlayerX, Game.PlayerY
    while (True):
       CL = Cango(Game)
       if not CL:
           return (Game.Score)
       else:
           choix = CL[random.randrange(len(CL))]  # on choisit une direction possible
           Game.Grille[x, y] = 2  # laisse la trace de la moto
           x += choix[0]
           y += choix[1]
           Game.PlayerX = x
           Game.PlayerY = y
           Game.Score += 1
"""
# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)



def SimulationPartie (Game,nb):

    # on copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True

    while (boucle):


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
        # Choix = np.ones(nb,dtype=np.uint8) * 2
        R = np.random.randint(12, size=nb)
        Indices[Indices == 0] = 1
        R = R % Indices

        Choix = LPossibles[I, R]  # pour chaque partie je choisi une voie possible

        # DEPLACEMENT

        if (np.array_equal(Choix, np.zeros(nb, dtype=np.int8))):
            return np.mean(S)
        else:

            DX = dx[Choix]
            DY = dy[Choix]
            X += DX
            Y += DY
            S += ds[Choix]
"""
#fonction qui lance les simulations pour trouver le meilleure score // retourne le score total
def MonteCarlo (Game):

    total = 0
    SimulGame = Game.copy()
    total += SimulationPartie(SimulGame,5)
    return (total)
"""
#fonction qui détermine le coup à jouer // retourne le coup gagnant
def nextStep(Game, listecoup):
    max = 0
    for elt in listecoup:
        Gametest = Game.copy()
        Gametest.PlayerX += elt[0]
        Gametest.PlayerY += elt[1]
        sc = SimulationPartie(Gametest,10000)
        if sc > max:
            max = sc
            stock = elt
    return (stock)





#fonction qui donne les directions possibles// retourne une liste de tuples
def Cango(Game):

    x, y = Game.PlayerX, Game.PlayerY
    listcango = []
    if (Game.Grille[x - 1, y] == 0):  # gauche
        listcango.append((-1, 0))
    if (Game.Grille[x + 1, y] == 0):  # droite
        listcango.append((1, 0))
    if (Game.Grille[x, y - 1]== 0):  # bas
        listcango.append((0, -1))
    if (Game.Grille[x, y + 1] == 0):  # haut
        listcango.append((0, 1))
    return (listcango)




def Play(Game):
    
    x,y = Game.PlayerX, Game.PlayerY
    print(x,y)

    liste = Cango(Game)
    print(liste)
    if not liste:
        return True #partie terminée
    else:
        Game.Grille[x, y] = 2  # laisse la trace de la moto
        step = nextStep(Game, liste)
        x += step[0]
        y += step[1]
        Game.PlayerX = x  # valide le déplacement
        Game.PlayerY = y  # valide le déplacement
        Game.Score += 1
        return False  # la partie continue


"""      
    choix = liste[random.randrange(len(liste))] # on choisit une direction possible
    Game.Grille[x,y] = 2  # laisse la trace de la moto

    x += choix[0]
    y += choix[1]
    #y += 1  # on essaye de bouger vers le haut
    v = Game.Grille[x,y]


    if v > 0 :
        # collision détectée
        return True # partie terminée
    else :
       Game.PlayerX = x  # valide le déplacement
       Game.PlayerY = y  # valide le déplacement
       Game.Score += 1
       return False   # la partie continue
"""
     

################################################################################
     
CurrentGame = GameInit.copy()
 

def Partie():

    Tstart = time.time()
    PartieTermine = Play(CurrentGame)
    print(time.time()-Tstart)
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(1000,Partie) 
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

        

      
 

