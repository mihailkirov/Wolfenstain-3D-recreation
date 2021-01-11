#!/usr/bin/env python3

# "3D" project  -- raycasting 
# Map module 
# by Mihail Kirov - 2018 

####################################################################################################################
import numpy as np 
import math 
from random import randint
import pygame 
from pygame.locals  import*
#####################################################################################################################

# VARIABLE GLOBALES 
pygame.init()
taille_police = 12
pol = pygame.font.SysFont("arial", taille_police)
################################################################################################################


# MINIMAP FUNCTIONS
def murs(mat, surface, widthdis, heightdis, nmbcase, color): 
	""" Fonction pour visualiser le minimap. 
		Les arguments doivent etre mise a jour pour chaque
		changement des parametres d'affichage (larg, haut ,nombcase)
	"""	

	width, height = widthdis // nmbcase, heightdis//nmbcase 
	for i in range(len(mat)):
		for j in range(len(mat)):
			if mat[i][j]:
				pygame.draw.rect(surface, color, [j*width   , i*height    , width  , height  ])


	
def dessin_intersect(p1 ,intersections, surface, color):
	""" La fonction dessine une droit1e entre les points p1 - (x1, y1) =>joueur) 
		et p2(x2, y2) => intersection. (minimap)	
	"""

	for inter in intersections :
		pygame.draw.line(surface, color, p1, inter, 3)


def transformation_wc_nc_dc(point, window, viewport): # window ,viewport -> ((xa,ya),(xb,yb)) 
	""" Projection  d'un point de WC a DC en passant par NC 
		Fonction creee en TP 
	""" 

	# point doit etre en coord homogenes  - [a,b,c] 


	wxa, wxb  = window[0][0], window[1][0]
	wya, wyb = window[0][1], window[1][1]  # window coordinates aren't constant in the module
	dimw = ( abs(wxb - wxa) , abs(wyb - wya))   	
	dimvp = (abs(viewport[1][0] - viewport[0][0]), abs(viewport[1][1] - viewport[0][1]))

	# matrix coeffs
	x3 = - wxa * dimvp[0]/ dimw[0]  + viewport[0][0]   
	y3 = - wya / dimw[1] * dimvp[1] + viewport[0][1]
	general_matrix = [[dimvp[0]/dimw[0], 0, x3], [0, dimvp[1]/dimw[1], y3], [0, 0, 0]]		

		
	return multiplication_matr1_matr2([point], general_matrix)



def multiplication_matr1_matr2(m1, m2):
	""" multiplication des matrices m1 et m2 """

	vect_result = []
	for i in range(len(m1)):
		add = []
		for j in range(len(m1[i])):
			add += ([sum( m2[j][k] * m1[i][k] for k in range(len(m1[i])))])
		vect_result += add 
			
	# the result is column vector 
	return vect_result


####################################################################################################
# MAP FUNCTIONS

def init_mat(param): # param - entier naturel
	""" Creation d'une matrice pleine param x param avec numpy."""

	return np.zeros((param, param), dtype = int)


def remplissage_matrice(mat, densite): # mat - matrice 
	""" La fonction remplis la matrice avec des 1 (pour representer  les murs) 
		sur les bords (extremites) de la carte (forme d'une carre)
	"""

	mat[-1][-1] = 1
	count = 1
	size = len(mat)
	
	for i in range(size - 1):
		mat[i][0] = 1 	# remplissage de la premiere colonne de la carte
		mat[0][i] = 1 	# remplissage de la premiere ligne de la carte
		mat[-1][i] = 1 	# remplissage de la derniere ligne de la carte
		mat[i][-1] = 1 	# remplissage de la derniere colonne de la carte
		count += 4
	
	# remplissage en fonction de la densite
	# 23% de la map sont initialement remplis

	nmbcase = int(densite/100 * size**2)
	while(count <= nmbcase):
		x, y = randint(0, 15), randint(0, 15)
		
		if (mat[x][y] == 0 ):
			mat[x][y] = 1 
			count += 1	

	return mat 


def pos_joueur(mat, nmbcases):
	""" Positionnement aletoire du joueur sur une case
		libre (x ET y != 1) dans la matrice 
	"""

	x, y = randint(0, 64 * nmbcases), randint(0, 64 * nmbcases)
	
	if(mat[int(y//64)][int(x//64)]): 
		x, y = pos_joueur(mat, nmbcases)

	return [x, y] 


#############################################################################################################################################################33

# RAYCASTING FUNCTIONS

def lancer_rayon(fov, width, orient): # fov - champ de vue , width - taille de la resolution horizontale, orient-angle d'orientation dans cercle trigo
	""" Le generateur va renvoyer des rayons uniformement
		repartis  sur le fov (field of view)
	"""

	start, end =  (orient - fov/2), (orient + fov/2)
	ecarte = fov/width  # angle entre 2 rayons consecutive (pour chaque colonne des pixel de width)
	
	while (start <= end):
		yield start%360
		start = (start + ecarte) 


def vertical_intersect(x, y, omega): # omega - angle , (x,y) -> entiers
	""" La fonction calcule la premiere intersection  verticale de point (x,y)  """ 

	# je considere que le joueur va visiter des coord multiple de 64 sur x et sur y 
	
	if  (omega < 90 or omega > 270):
			xv = int(x//64)*64  + 64
			yv = y + abs(x - xv)*(math.tan(math.radians(omega))) 

	else :
			xv = int(x//64)*64
			yv = y + abs(x - xv)*math.tan(math.radians(omega))*(-1)  # changement des signes aux quadrants 2 et 3 

	return xv, yv 


def horizontal_intersect(x, y, omega):
	""" La fonction calcule l'intersection de point (x,y) avec la premiere ligne horizontale"""

	if  (0 < omega < 180):
		yh = int(y//64)*64  + 64 
		xh = x + abs(y - yh)/(math.tan(math.radians(omega))) # valuer absolu pour quadrant 2 et 4 
	
	else : 
		yh = int((y)//64)*64 
		xh = x + abs(y - yh)/(math.tan(math.radians(omega)))*(-1) # valuer absolu pour quadrant 2 et 4 

	return xh, yh 


def calcul_distance_vertical(x, y, omega, mapp, distancev,):
		""" La fonction retourne la distance de la premiere intersection verticale 
			avec un mur ainsi que les coordonnees de x,y de l'intersection 
		"""

		xv, yv = vertical_intersect(x, y, omega) # premiere intersection
		nonintersect = True 
		# premieres indices dans la matrice
		inda = int(yv//64)  # lignes
		indb = int(xv//64) - 1 if  90 < omega < 270 else int(xv//64)
		intersect = []
		
		pas = 1 if  (omega < 90 or omega > 270) else -1 
		# deplacement dans la matrice en fonction d'angle 
		pasmatabsc = -1 if 90 < omega < 270 else 0 
		
		while(nonintersect and (0 <= inda < 16  and 0 <= indb < 16)):		
			
			if (mapp[inda][indb] == 1): # on a un mur a l'intersection verticale
				distancev = math.hypot((x - xv), (y - yv))
				intersect += [[xv, yv, 1]]			
				nonintersect = False			
			
			else:
				xv  += 64*pas # distance fixe entre deux case contigues
				# Avancer ou reculer en fonction de l'angle
				
				yv += 64*(math.tan(math.radians(omega)))*pas 

				# Indices dans la matrice 
				inda = int(yv//64)  
				indb = int(xv//64) + pasmatabsc
		
		return [intersect, round(distancev, 4)]
	
		
def calcul_distance_horizontal(x, y, omega, mapp, distanceh):
		""" La fonction retourne la distance de la premiere intersection horizontale 
			avec un mur ainsi que les coordonnees de x,y de l'intersection 
		"""
		
		xh, yh  = horizontal_intersect(x, y, omega)	# premiere intersection
		inda = int(yh//64) - 1 if  180 < omega < 360 else int(yh//64)
		indb = int(xh//64)		
		nonintersect = True 		
		intersect = []
		pas = 1  if  0 < omega < 180  else -1
		# deplacement dans la matrice en fonction d'angle 
		pasmatord = 0 if  0 < omega < 180 else -1 # deplacement dans la matrice en fonction d'angle 
		
		while(nonintersect and  (0 <= inda < 16 and 0 <= indb < 16)):
			
			if (mapp[inda][indb] == 1): # on a un mur a l'intersection horizontale
				distanceh = math.hypot((x - xh), (y - yh))
				nonintersect = False
				intersect += [[xh, yh, 1]] # coord homogenes		
			
			else:	
				yh += 64*pas
				# Avancer ou reculer sur x en fonction de l'angle
				
				xh += 64/math.tan(math.radians(omega))*pas

				# Indices dans la matrice 
				inda = int(yh//64) + pasmatord
				indb = int(xh//64) 
				 
		return [intersect, round(distanceh, 4)] 				
		


def distance_mur(player, omega, mapp): # player - [(x, y), theta] ; omega - angle (degre) de rayon p/r une droite de reference , map - matrice
	""" Calcule de la distance du rayon ,oriente d'angle omega, du mur le plus proche dans la map 
		en calculant successivement intersection avec les lignes verticales et horizontales. La fonction 
		aussi retourne les coordonnes de l'intersection 
	"""
	global INTER
	x, y = player[0][0], player[0][1] 	
	point_disth, point_distv =[[], 2*16*64], [[], 2*16*64]  # distances impossible a atteindre dans cette situation MODIFIER  
	# la liste va contenir les coord (x, y) de l'intersection avec le mur le plus proche

	# Repere inverse ==>
	# intersection vertical sera sur x 
	# intersection vertical sur y 

	if (omega != -270 and omega != 90): # si on a un angle qui n'est pas un multiple de pi/2
		point_distv = calcul_distance_vertical(x, y, omega, mapp, point_distv[1])
	
	if(omega != 180 and omega != 0): # si on a un angle qui n'est pas un multiple de pi
		point_disth = calcul_distance_horizontal(x, y, omega, mapp, point_disth[1])	
				

	if point_disth[1] > point_distv[1] :
		return point_distv,1 # retorur des coord de l'intersection la plus proche ( entre intersect verticale et horizontale)  

	else:
		return point_disth,0
