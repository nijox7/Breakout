from fltk import*
from random import randint
import time

long = 1080
larg = 1920
cree_fenetre(larg, long)
#image(0, 0, 'map.gif', tag="im")

class Raquette():
    '''
    Définit les éléments principaux de la raquette
    '''

    def __init__(self):
        self.x = 890
        self.y = 950
        self.largeur = 150
        self.hauteur = 20

    def dessine(self):
        #image(self.x, self.y, 'raquette.gif', ancrage='center', tag='rqt')
        rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, remplissage='blue', tag='rqt')

class Balle:
    '''
    Définit les éléments principaux de la balle
    '''

    def __init__(self):
        self.rayon = 15
        self.x = 965
        self.y = 935
        self.vecteur = (-7,-28) #(abscisse, ordonné)

    def dessine(self):
        #image(self.x, self.y, 'balle.gif', tag='balle')
        cercle(self.x, self.y, self.rayon, remplissage='red', tag='balle')

class Obstacle():
    '''
    Définit les éléments principaux d'un obstacle
    '''

    def __init__(self, x, y, largeur, hauteur, indice, couleur):
        #Dimensions de l'obstacle
        self.largeur = largeur
        self.hauteur = hauteur
        #Position du coin supérieur gauche de l'obstacle
        self.x = x
        self.y = y
        #Indice qui permet de distingueur l'obstacle
        self.indice = indice
        #Couleur de l'obstacle
        self.couleur = couleur
        self.name = 'obst'+str(self.indice)

    def brique(self):
        rectangle(self.x, self.y,
                  self.x + self.largeur, self.y + self.hauteur,
                  remplissage=self.couleur, tag=self.name)

def obst_collision(balle, obstacles):
    for obst in obstacles:
        if obst.x - balle.rayon <= balle.x <= obst.x + obst.largeur + balle.rayon: #dans la zone abscisse
        #Coin
            if obst.y - balle.rayon <= balle.y <= obst.y + obst.hauteur + balle.rayon:
                efface(obst.name)
                obstacles.remove(obst) #supprime l'obstacle
                balle.vecteur = (- balle.vecteur[0], - balle.vecteur[1])
                break
        #Côté horizontal
            if obst.y - balle.rayon <= balle.y + balle.vecteur[1] <= obst.y + obst.hauteur + balle.rayon:
                efface(obst.name)
                obstacles.remove(obst) #supprime l'obstacle
                balle.vecteur = (balle.vecteur[0], - balle.vecteur[1])
                break
        #Coté vertical
        elif obst.y - balle.rayon <= balle.y <= obst.y + obst.hauteur + balle.rayon:
            if obst.x - balle.rayon <= balle.x + balle.vecteur[0] <= obst.x + obst.largeur :
                efface(obst.name)
                obstacles.remove(obst) #supprime l'obstacle
                balle.vecteur = (- balle.vecteur[0], balle.vecteur[1])
                break


### PROGRAMME PRINCIPAL ###

'''Dessine tous les éléments initiaux'''
#Instancie la raquette
rqt = Raquette()
rqt.dessine()
#Instancie la balle
balle = Balle()
balle.dessine()
#Instancie les obstacles
indice = 0
obstacles = []
for i in range(3):
    for j in range (11):
        obst = Obstacle(j*180, i*60, 180, 60, indice, "purple")
        obst.brique()
        indice += 1
        obstacles.append(obst)

'''Exécution du jeu'''
debut = time.time()
compt = 0
running = True
attend_ev()
while running == True:
    frametime = time.time()
    ev = donne_ev()
    tev = type_ev(ev)

    #Actions du joueur
    if tev == "Quitte":
        running = False
    rqt.x = abscisse_souris()
    efface('rqt')
    rqt.dessine()

    #Collisions de la balle
    if balle.y - balle.rayon <= 0:
        '''Bord supérieur'''
        balle.vecteur = (balle.vecteur[0], - balle.vecteur[1])
    elif balle.x - balle.rayon <= 0 or balle.x + balle.rayon >= larg:
        '''Bord droit ou gauche'''
        balle.vecteur = (- balle.vecteur[0], balle.vecteur[1])
    elif balle.y + balle.rayon >= long:
        '''Bord inférieur, réinitialisation'''
        balle.vecteur = (-7,-28)
        balle.x = rqt.x
        balle.y = rqt.y - 10
        compt += 1
        attend_ev()
    elif (rqt.y - balle.rayon <= balle.y <= rqt.y + rqt.hauteur + balle.rayon
          and rqt.x <= balle.x <= rqt.x + rqt.largeur):
        '''Raquette'''
        if balle.x < rqt.x + (rqt.largeur/2):
            balle.vecteur = (- abs(balle.vecteur[0]), - balle.vecteur[1])
        else:
            balle.vecteur = (abs(balle.vecteur[0]), - balle.vecteur[1])
    #else:
    '''Obstacles'''
    obst_collision(balle, obstacles)

    #Met à jour la position de la balle
    balle.x += balle.vecteur[0]
    balle.y += balle.vecteur[1]
    efface("balle")
    balle.dessine()
    
    #FPS
    elapsed_time = time.time() - frametime
    if elapsed_time < 1.0/60:
        time.sleep(1.0 / 60 - elapsed_time)
    #print(f'{(time.time()-frametime)*1000:4f}ms')

    #Défaite au bout de 3 essais, temps affiché depuis le début de la partie
    if compt == 3:
        tecoule = time.time() - debut
        texte(170, 100, "Vous avez perdu !",
        couleur = 'black', ancrage = 'nw', police = 'Helvetica', taille = 24)
        texte(170, 150, "Temps écoulé : " f'{time.strftime("%M:%S",time.gmtime(tecoule))}', #affiche en minute:seconde
        couleur = 'black', ancrage = 'nw', police = 'Helvetica', taille = 12)
        attend_ev()
        running = False
    if obstacles == []:
        tecoule = time.time() - debut
        texte(170, 100, "Vous avez gagné !",
        couleur = 'black', ancrage = 'nw', police = 'Helvetica', taille = 24)
        texte(170, 150, "Temps écoulé : " f'{time.strftime("%M:%S",time.gmtime(tecoule))}', #affiche en minute:seconde
        couleur = 'black', ancrage = 'nw', police = 'Helvetica', taille = 12)
        attend_ev()
        running = False

    mise_a_jour()

ferme_fenetre()
