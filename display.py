#!/usr/bin/env python3
# "3D" project  -- raycasting 
# display module 
# by Mihail Kirov - 2018 

from map import * 
from joueur1 import*

HAUTMURS = 64

def distance_ecran(angle, width):
	""" La fonction retourne la distance
		entre la camera et l'ecran virtuel 
	"""

	return width/2*round(math.tan(math.radians(angle/2)), 6)


def hauteur_colonne(dist, distec): # hautm - hauteur mur, distec - distance ecran
	""" La fonction retourne la hauteur correspondant
		du mur sur l'ecran de projection en fonction 
		de la distance reelle de joueur au mur,
		l'hauteur de mur et la distance d'ecran
		virtuel
	"""

	return round(HAUTMURS*distec/dist, 3)


def dessin_mur(screen, start, end, couleur, distmax, distint):
	""" Remplissage d'un colonne de pixels sur screen
		correspondant au murs + ombrages"""
	
	p = 1 - distint/distmax # pour ombrage
	couleur = list(map(lambda x: x*p, couleur)) # modification de la couleur du mur
	pygame.draw.line(screen, couleur, start, end ,1)


def dessine_plafond(screen, start1, end1, couleur): # start, end - tuples (x, y)
	""" Remplissage d'un colonne de pixels sur screen
		correspondant au sol """

	pygame.draw.line(screen, couleur, start1, end1 ,1)



def affiche_info(pos, fps, orient, fov, couleur, screen, hight):
	""" Affichage de la position (x,y ) de joueur, le fps
		l'orientation (angle) et angle de voue (FOV)
	"""

	coordo_txt = pol.render("posx:  {}   posy : {} ".format(round(pos[0],2), round(pos[1], 2)), 1, couleur)
	fps_txt = pol.render("fps : {}".format(fps), 1, couleur)
	fov_txt = pol.render("FOV: {}".format(fov), 1 , couleur)
	orient_txt = pol.render("angle orient :{}".format(orient), 1, couleur)

	# Positionnement du text sur l'ecran
	screen.blit(coordo_txt, (0, hight - taille_police))
	screen.blit(fps_txt, (0, hight - 2*taille_police))
	screen.blit(fov_txt, (0, hight - 3*taille_police))
	screen.blit(orient_txt, (0, hight - 4*taille_police))



def dessine_sol(screen, start2, end2, couleur):
	""" Remplissage d'un colonne de pixels sur screen
		correspondant au  plafond """

	
	pygame.draw.line(screen, couleur, start2, end2, 1)


def coord_murs_cam_centre(x, milieu, hautcol): # hautcol = hauteur de la colonne 
	""" La fonction renvoie les coordonnes 
		du mur quand la camera est centree 
	"""

	return [x, milieu - hautcol/2], [x, milieu + hautcol/2]



def floor_coord(x, milieu, hautcol, hight):
	""" La fonction retourne les coordonnes xdebut,ydebut
		xfin,yfin qui seront utilise pour dessiner le sol
		(colonnes de pixles <==> droite )
	""" 
	
	start = milieu + hautcol/2 
	return [x, start], [x, hight]


def coord_plafond(x, milieu, hautcol):
	""" Retour des coordonnees de plafond """ 
	
	start =  milieu - hautcol/2 
	return [x, start] , [x, 0]

# Textures 
def dessin_mur_textures(x1 ,xint, yint, hautcol, image, sizecase, screen, imagew, imageh): # imageh - hauteur de l'image
	""" Dessin des texture des murs """

	x = xint/sizecase # position dans l'ecran 
	posimx = int((x%1)*imagew) # position dans l'image
	s = image.subsurface((posimx, 0, 1, imageh)) # creation d'une lamelle (surface)
	s = pygame.transform.scale(s, (1, int(hautcol))) # redimentionnement
	screen.blit(s, (x1, yint))	


