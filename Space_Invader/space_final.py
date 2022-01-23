import tkinter as tk  
import random as rd
 
class Vaisseau:#Cette classe crée et gère les déplacements du vaisseau.

    def __init__(self, canvas, game, x_pos=275, y_pos=550): # On initie tous les attributs du vaisseau
       
        self.canvas = canvas
        self.image = tk.PhotoImage(file='vaisseau.png').subsample(10,10) #50px*50px
        self.sprite= canvas.create_image(x_pos,y_pos,image=self.image, anchor='nw')
        self.direction = 0
        self.game = game
        self.timer_shot = 1000
        self.shot = False
 
    def deplacement_gauche(self, event):
        if self.game.game_over:
            return
        self.direction=-1
 
    def deplacement_droite(self, event):
        if self.game.game_over:
            return
        self.direction=1
 
    def stop_move(self, event):
        if self.game.game_over:
            return
        if (event.keysym == "q" and self.direction == -1) or (event.keysym == "d" and self.direction == 1):
            self.direction = 0
        if (event.keysym == "space" and self.shot == 1):
            self.shot = False
 
    def mouvement_vaisseau(self):  # Déplacement du sprite
        if self.game.game_over:
            return
           
        if (self.canvas.coords(self.sprite)[0] <= 4 and self.direction==-1) or (self.canvas.coords(self.sprite)[0] >= 550 and self.direction==1) :
            self.direction=0 # On fait attention à ne pas dépasser les bordures
        else:
            self.canvas.move(self.sprite, self.direction*5,0)
        self.canvas.after(16,self.mouvement_vaisseau)
       
        if self.shot == True and self.timer_shot >= 25 and not(self.game.transition):
            self.game.current_shots.append(Shot(self.canvas, self.game, self.canvas.coords(self.sprite)[0], self.canvas.coords(self.sprite)[1], -1))
            self.timer_shot = 0 # Remise à zéro du timer après un tir du vaisseau
 
    def new_shot(self, event):
        if self.game.game_over:
            return
        if self.timer_shot >= 25:   # Impose un timer pour ne pas pouvoir tirer indéfiniment
            self.shot = True
   
    def no_shot(self):   # Incrémentation du timer entre deux tirs
        if self.game.game_over:
            return
        self.timer_shot += 1
 
        self.canvas.after(16, self.no_shot) # permet de choisir la fréquence de tirs
        
        
class Aliens:#Cette classe permet de créer les aliens.

 
    def __init__(self, canvas, game, Horde, x_pos=6, y_pos=1, direction = 1, speed = 2, frequence = 16, kind=2):
        self.kind = kind
        self.canvas = canvas
        self.x_pos = x_pos
        self.set_image = [tk.PhotoImage(file='alien1.png'),
                          tk.PhotoImage(file='alien2.png'),
                          tk.PhotoImage(file='alien22.png')] #50px*50px
        self.y_pos= y_pos # Pourrait être utile. Position dans la grille de la horde
        self.sprite= canvas.create_image(50*x_pos,50*y_pos+50,image=self.set_image[kind-1], anchor='nw')
        self.direction = direction # utile pour les solitaires hors hordes qui donnent des bonus
        self.image=self.set_image[kind-1]
        self.Horde = Horde        
        self.game = game
        self.speed = speed
        self.frequence = frequence
        self.score = 50*kind**2
        self.pv = kind
        if self.pv == 3:
            self.pv = 1
            
 
class Horde:#Cette classe permet de créer les hordes à partir des aliens.

    def __init__(self,canvas, game, length, height, speed = 1, proba = 5000,frequence = 16, direction = 1):
        self.aliens_list = []
        self.length = length
        self.height = height
        self.canvas = canvas
        self.game = game
        self.speed = speed
        self.direction = direction
        self.frequence = frequence
        self.proba = proba
       
        for i in range(length):
            for j in range(height-1):
                self.aliens_list.append(Aliens(canvas, game, self, i+(12-length)//2, j, self.direction, self.speed, self.frequence, 2))
            self.aliens_list.append(Aliens(canvas, game, self, i+(12-length)//2, height-1, self.direction, self.speed, self.frequence, 1))
            
    def mouvements(self):#Gère les mouvements de la horde
        if self.game.game_over or self.game.transition:
            return
        mouvement_ok=True
        for Aliens in self.aliens_list:
            if self.canvas.coords(Aliens.sprite)[0] + self.direction*self.speed < 0 or self.canvas.coords(Aliens.sprite)[0] + self.direction*self.speed + 50 > 600:
                mouvement_ok = False
        if mouvement_ok:
            for Aliens in self.aliens_list:
                self.canvas.move(Aliens.sprite, self.direction*self.speed, 0)
        else:
            for Aliens in self.aliens_list:
                if self.canvas.coords(Aliens.sprite)[1] + 50 + 25 > 490:
                    self.game.game_over = True
            if self.game.game_over:
                self.canvas.after(16, self.game.end_game)
                return
 
            for Aliens in self.aliens_list:
                self.canvas.move(Aliens.sprite, 0, 25)
                Aliens.direction = (Aliens.direction == -1) - (Aliens.direction == 1)
            self.direction = (self.direction == -1) - (self.direction == 1)
        self.canvas.after(self.frequence,self.mouvements)
   
    def new_shot(self):
        if self.game.game_over or self.game.transition:
            return
        for Aliens in self.aliens_list:
            shot_proba = rd.randint(0,self.proba)
            if shot_proba <= 1:
                self.game.current_shots.append(Shot(self.canvas, self.game, self.canvas.coords(Aliens.sprite)[0], self.canvas.coords(Aliens.sprite)[1], 1))
        self.canvas.after(16, self.new_shot)
               
               
           
class Shot:#Classe qui gère les tirs du vaisseau et des aliens

    def __init__(self, canvas, game, x_pos, y_pos, direction):
        self.image = [tk.PhotoImage(file='laser.png'), tk.PhotoImage(file='laser2.png')]
        self.canvas= canvas
        self.game = game
        self.direction = direction
        self.sprite = canvas.create_image(x_pos,y_pos+direction*30,image=self.image[(self.direction == -1)], anchor='nw')
 
 
 

 

 
class Brique:#Cette classe permet de créer les briques qui composent les 3 ilots

    def __init__(self, canvas, game,x_pos, y_pos):
        self.image = tk.PhotoImage(file='bloc.png').subsample(25,25)
        self.game = game
        self.canvas = canvas
        self.sprite = self.canvas.create_image(x_pos,y_pos,image=self.image, anchor='nw')
     
class Ilots:#Cette classe permet de créer les ilots à partir des blocs

    def __init__(self, canvas, game):
        self.game = game
        self.canvas = canvas
        self.blocks_list=[]
        for i in range(5):  # 5 briques par ligne
            for j in range(3):  # 3 briques par colonne
                self.blocks_list.append(Brique(canvas, game, 60+20*i, j*20+485)) # 3 ilots
                self.blocks_list.append(Brique(canvas, game, 260+20*i, j*20+485))
                self.blocks_list.append(Brique(canvas, game, 460+20*i, j*20+485))
                
                
class Menu:#Classe qui crée un objet ayant pour attributs tous les éléments du menu.

    def __init__(self):        
        self.background = tk.PhotoImage(file = 'backgroundMenu.png')
        self.logo =  tk.PhotoImage(file = 'logo.png')
        self.play_button = tk.Button( text = 'PLAY !',height = 4, width = 20,activebackground='#ECECEC',background='#FFFFFF')
        self.exit_button = tk.Button( text = 'EXIT',height = 2, width = 10,activebackground='#ECECEC',background='#FFFFFF')
        
class Jeu:#Classe permettant de gérer le canvas,la fenêtre de jeu et le bon fonctionnement de celui-ci.

    def __init__(self, window, length, height, speed = 1,proba = 4000):
 
        self.window = window # Fenetre est une fenêtre Tk()
        self.window.title('Space Invaders')
        self.window.geometry("600x600")
        self.window.resizable(width=False, height=False)
 
        self.canvas = tk.Canvas(self.window, bg='black', bd= 0, highlightthickness=0, height = 600, width = 600)
 
        self.vaisseau = Vaisseau(self.canvas, self)
 
        self.length = length
        self.height = height
        self.speed = speed
        self.proba = proba  # Proba n'est pas vraiment une probabilité, plus il baisse plus les aliens tirent fréquemment.
         # Ces 3 pour manches suivantes, incrémentés
 
 
        self.round = 1
        self.round_SV = tk.StringVar()
        self.round_SV.set(str(self.round))
 
        self.horde = Horde(self.canvas, self, self.length, self.height, self.speed,self.proba)
        self.walls = Ilots(self.canvas,self)
        self.game_over = False
        self.current_shots = []
 
        self.menu = Menu()        
 
        self.transition = False
 
        self.score = 0
        self.highscore_SV = tk.StringVar()   # On utilise une stringvariable pour pouvoir changer sa valeur ensuite
        self.temp = open("highscore.txt", "rt")
        self.highscore = int(self.temp.readline())  # Entier qui stocke le highscore, pas le même type de variable que highscore_SV
        self.temp.close()        
        self.temp = open("highscore.txt", "rt")  # On ouvre deux fois le fichiers au lieu d'une car cela génère une erreur de faire les deux manipulations en une fois
        self.highscore_SV.set('HIGHSCORE : '+self.temp.readline())
        self.temp.close()
       
       
 
    def menu_launch(self): # Affichage du menu
        self.canvas.pack(anchor='nw')
        self.background_display = self.canvas.create_image(300,300,image=self.menu.background)
        self.logo_display = self.canvas.create_image(300,133,image=self.menu.logo)
        self.play_button_display =self.canvas.create_window(300,350,window = self.menu.play_button)
        self.menu.play_button.config( command=self.start)
        self.exit_button_display = self.canvas.create_window(300,450,window = self.menu.exit_button)
        self.menu.exit_button.config( command=self.window.destroy)
        self.highscore_label = tk.Label(self.canvas, textvariable=self.highscore_SV, fg='white', bg='black', font='Helvetica 16 bold')
        self.highscore_disp = self.canvas.create_window(490,15,window = self.highscore_label)
        self.canvas.after(16, self.record)
        self.sv = tk.StringVar()
        self.sv.set('SCORE : '+str(self.score))
        self.score_label = tk.Label(self.canvas, textvariable=self.sv, fg='white', bg='black', font='Helvetica 16 bold')
   
    def start(self): # Permet de commencer la partie
        self.canvas.delete(self.play_button_display,self.exit_button_display,self.background_display,self.logo_display)
        self.canvas.pack(anchor='nw')
       
        self.score_display = self.canvas.create_window(90,15,window = self.score_label)
       
        self.canvas.after(16, self.horde.mouvements)
        self.canvas.after(16, self.vaisseau.mouvement_vaisseau)
        self.canvas.after(16, self.shots_management)
        self.canvas.after(16, self.aff_score)
        self.canvas.after(16, self.horde.new_shot)
        self.canvas.after(16, self.vaisseau.no_shot)
        self.window.bind('<q>', self.vaisseau.deplacement_gauche)
        self.window.bind('<Q>', self.vaisseau.deplacement_gauche)
        self.window.bind('<s>', self.vaisseau.deplacement_droite)
        self.window.bind('<S>', self.vaisseau.deplacement_droite)
        self.window.bind('<KeyRelease>', self.vaisseau.stop_move)
        self.window.bind('<space>', self.vaisseau.new_shot)
   
    def aff_score(self): # Affichage du score pendant la partie
        self.canvas.delete(self.score_display)
        self.sv.set('SCORE : '+str(self.score))        
        self.score_display = self.canvas.create_window(90,15,window = self.score_label)
        self.canvas.after(16, self.aff_score)
       
    def record(self): # Gère la modification en direct de la valeur du record après une partie
        self.canvas.delete(self.highscore_disp)
        self.temp = open("highscore.txt", "rt")
        self.highscore_SV.set('RECORD : '+self.temp.readline())
        self.temp.close()
        self.highscore_disp = self.canvas.create_window(490,15,window = self.highscore_label)
 
    def round_screen(self): # Ecran de transition entre deux manches
        self.round += 1
        self.round_SV.set('ROUND '+ str(self.round))
        self.round_label = tk.Label(self.canvas, textvariable=self.round_SV, fg='#FFE213', bg='black', font='Helvetica 60 bold')
        self.round_display = self.canvas.create_window(300,250,window = self.round_label)
        self.canvas.after(1000,self.new_round)  #lancement de la prochaine manche

    def new_round(self):
        self.canvas.delete(self.round_display)
        
        if self.speed < 3 :  # Augmentation de la vitesse 
            self.speed += 0.5
        if self.proba > 2100 : # Augmentation de lé fréquence de tir
            self.proba -= 900
        if self.proba > 500 and self.proba < 2100:
            self.proba -= 300        
        self.horde = Horde(self.canvas, self, self.length, self.height, self.speed,self.proba)
        self.transition = False
        self.canvas.after(16, self.horde.mouvements)
        self.canvas.after(16, self.horde.new_shot)
        self.canvas.after(16, self.shots_management)
   
 
    def end_game(self): # Ecran de game over
        self.canvas.delete('all')
        label = tk.Label(self.canvas, text='GAME OVER', fg='white', bg='black')
        label.config(font=("Liberation", 30))
        self.canvas.create_window(300, 300, window=label)
        self.background_display = self.canvas.create_image(300,300,image=self.menu.background)
       
        if self.score > self.highscore: # Sauvegarde du meilleur score si on bat le record
            temp = open("highscore.txt", "wt")
            temp.write(str(self.score))
            temp.close()
       
        self.canvas.after(500, self.restart)
       
    def restart(self): # Réinitialisation du jeu pour ré-afficher le menu et relancer une partie.
        self.canvas.delete('all')
        self.speed = 1
        self.proba = 4000
        self.round = 1
        self.vaisseau = Vaisseau(self.canvas, self)
        self.horde = Horde(self.canvas, self, self.length, self.height, self.speed)
        self.walls = Ilots(self.canvas,self)
        self.game_over = False
        self.current_shots = []
        self.score = 0
       
        self.menu = Menu()
        self.play_button = tk.Button(self.window, text = 'PLAY !',height = 4, width = 20,command=self.start,activebackground='#ffbd33',background='#FFE213')
        self.exit_button = tk.Button(self.window, text = 'EXIT',height = 2, width = 10,command=self.window.destroy,activebackground='#ffbd33',background='#FFE213')
       
        game.menu_launch()
 
    def shots_management(self): # Gestion du mouvement des lasers et de la collision, ainsi que de l'augmentation de la variable score
        if self.game_over:
            return
        for shot in self.current_shots:
            touch = False  # True si l'entité est touchée
            index_Aliens_to_delete = None
            index_block_to_delete = None
            index_Aliens_to_touch = None
 
            self.canvas.move(shot.sprite, 0,shot.direction*4)
            if abs(self.canvas.coords(shot.sprite)[0] - self.canvas.coords(self.vaisseau.sprite)[0]) < 20 and abs(self.canvas.coords(shot.sprite)[1] - self.canvas.coords(self.vaisseau.sprite)[1]) < 33 and shot.direction == 1:
               
                touch = True
                self.game_over = True
               
            for Aliens in self.horde.aliens_list:
                if abs(self.canvas.coords(shot.sprite)[0] - self.canvas.coords(Aliens.sprite)[0]) < 23 and abs(self.canvas.coords(shot.sprite)[1] - self.canvas.coords(Aliens.sprite)[1]) < 33 and shot.direction == -1:
                   
                    touch = True
                    if Aliens.pv == 1:
                        index_Aliens_to_delete = self.horde.aliens_list.index(Aliens)  # Suppression de l'aliens mort
                        self.score += Aliens.score  # Augmentation du score quand on tue un aliens
                    else:
                        Aliens.pv -= 1  # On baisse la vie de l'aliens touché
                        index_Aliens_to_touch = self.horde.aliens_list.index(Aliens)
               
 
            for block in self.walls.blocks_list: # Gestion de la destruction des blocs
                if self.canvas.coords(block.sprite)[0] - self.canvas.coords(shot.sprite)[0] < 29 and self.canvas.coords(block.sprite)[0] - self.canvas.coords(shot.sprite)[0] > 0 and self.canvas.coords(shot.sprite)[1] - self.canvas.coords(block.sprite)[1] < 9 and self.canvas.coords(block.sprite)[1] - self.canvas.coords(shot.sprite)[1] < 29:
                    touch = True
                    index_block_to_delete = self.walls.blocks_list.index(block)
           
            if index_Aliens_to_touch != None:
                temp = self.horde.aliens_list[index_Aliens_to_touch]
                self.canvas.itemconfig(temp.sprite, image=temp.set_image[temp.kind-1+len(temp.set_image)//2]) # La liste est pensée telle que la 2e moitié puisse servir à representer la premiere moitié blessée
            if index_Aliens_to_delete != None:
                self.canvas.delete(self.horde.aliens_list[index_Aliens_to_delete].sprite)
                self.horde.aliens_list.remove(self.horde.aliens_list[index_Aliens_to_delete])
            if index_block_to_delete != None:
                self.canvas.delete(self.walls.blocks_list[index_block_to_delete].sprite)
                self.walls.blocks_list.remove(self.walls.blocks_list[index_block_to_delete])
           
            if self.canvas.coords(shot.sprite)[1] >= 560 or self.canvas.coords(shot.sprite)[1] < 0 or touch == True:
                self.canvas.delete(shot.sprite)
                self.current_shots.remove(shot)
           
            if self.game_over == True:
                self.canvas.delete(self.vaisseau.sprite)
                self.canvas.after(1000, self.end_game)
                return
 
            if len(self.horde.aliens_list) == 0:
                self.transition = True
            if len(self.horde.aliens_list) == 0 and len(self.current_shots) == 0:
                self.canvas.after(1000, self.round_screen) # on lance la prochaine manche
                return
        self.canvas.after(16, self.shots_management)
       


window = tk.Tk() 
game = Jeu(window, 8, 3) # Nombre de lignes et de colonnes qui composent la horde d'aliens.
game.menu_launch()
game.window.mainloop()