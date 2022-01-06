
from  tkinter import *
import math,random
from random import randint,randrange



def clavier(event):
    global PosX,PosY
    touche= event.keysym
    if touche =='s':
        if PosX>30:
            PosX -= 10
    if touche =='d':
        if PosX<520:
            PosX += 20
    Canevas.coords(vaisseau,PosX -10, PosY -10, PosX+10, PosY +10)

Mafenetre = Tk()
Mafenetre.title('Space Invader')

PosX=275
PosY=520

LARGEUR = 550
HAUTEUR = 550
RAYON=15
X=LARGEUR/2
Y=HAUTEUR/2
vitesse=5
angle=random.uniform(0,2*math.pi)
DX=vitesse*math.cos(angle)
DY=vitesse*math.sin(angle)
Canevas = Canvas(Mafenetre, width=LARGEUR, height=HAUTEUR, bg='white')
Alien=Canevas.create_oval(X-RAYON,Y-RAYON,X+RAYON,Y+RAYON,width=1,outline="red",fill='blue')
Alien_2=Canevas.create_oval(X-RAYON+5,Y-RAYON+5,X+RAYON+5,Y+RAYON+5,width=1,outline="red",fill='blue')
vaisseau= Canevas.create_rectangle(PosX -10, PosY -10, PosX+10, PosY +10, width=5, outline='black', fill='red')

Canevas.focus_set()
Canevas.bind('<Key>',clavier)
Canevas.pack(padx=5,pady=5)

#Affichage résultat
LabelResultat= Label(Mafenetre,text='Score:',fg='red',bg='white')
LabelResultat.pack(side=RIGHT,padx=5,pady=5)
#Bouton qui déclenche le début d'une partie.Ne pas oublier d'ajouter la command.
BoutonLancer= Button(Mafenetre, text="Lancer une partie")
BoutonLancer.pack(side=LEFT, padx=10,pady=10)

#Bouton pour quitter.
BoutonQuitter= Button(Mafenetre, text="Quitter", command= Mafenetre.destroy)
BoutonQuitter.pack(side=LEFT, padx=5,pady=5)

def deplacement():
    global X,Y,DX,DY,RAYON,LARGEUR,HAUTEUR
    #rebond à droite
    if X+RAYON+DX > LARGEUR:
        X=2*(LARGEUR-RAYON)-X
        DX=-DX
    #rebond à gauche
    if X-RAYON+DX < 0:
        X=2*RAYON-X
        DX=-DX
    #rebond en bas
    if Y+RAYON+DY>HAUTEUR:
        Y= 2*(HAUTEUR-RAYON)-Y
        DY=-DY
    #rebond en haut
    if Y-RAYON+DY<0:
        Y=2*RAYON-Y
        DY=-DY     
    X=X+DX
    #affichage
    Canevas.coords(Alien,X-RAYON,Y-RAYON,X+RAYON,Y+RAYON)

    Mafenetre.after(20,deplacement)




#Conditions initiales
    VerifLaser=False
    YLaser=800

deplacement()
Mafenetre.mainloop()
