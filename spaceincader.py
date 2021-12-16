from tkinter import Canvas, Tk, Label, Button, StringVar, Entry
from tkinter.constants import LEFT, RIGHT
import math,random

Mafenetre=Tk()
Mafenetre.title('Space Invader')

#Canvas
LARGEUR = 550
HAUTEUR = 550
RAYON=15
X=LARGEUR/2
Y=HAUTEUR/2
vitesse=random.uniform(1.8,2)*5
angle=random.uniform(0,2*math.pi)
DX=vitesse*math.cos(angle)
DY=vitesse*math.sin(angle)

Canevas= Canvas(Mafenetre, width= LARGEUR, height=HAUTEUR, bg='black')
Canevas.pack(padx=5,pady=5)

Balle=Canevas.create_oval(X-RAYON,Y-RAYON,X+RAYON,Y+RAYON,width=1,outline="red",fill='blue')

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
Y=Y+DY
#affichage
Canevas.coords(Balle,X-RAYON,Y-RAYON,X+RAYON,Y+RAYON)

Mafenetre.after(20,deplacement)

deplacement()
Mafenetre.mainloop()
