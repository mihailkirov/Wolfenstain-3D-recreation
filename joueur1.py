# Module joueur 
# projet Raycasting 
# Mihail Kirov - L3 Informatique

from map import *


def init_joueur(m, cases): 
	""" Initialisation du joueur - coordonnees dans l'espace 
		de joueur et  angle de orientation
	"""
	return [pos_joueur(m, cases), randint(0, 360)]


def deplacement(player, touche, pas, mapp):
	""" Procedure qui va modifier les coordonnees 
			de joueur dans le map en fonction de 
			l'angle d'orientation et la touche utilise 
	"""
	
	
	if (touche is "b") : # mouvement a l'arriere (backward)
		
		# Calcule de la distance au mur dans la direction de omega+180 
		distanceb = distance_mur(player, (player[1] + 180)%360, mapp)[0] 

		if (distanceb[1] > pas):
				player[0][0] +=  pas*math.cos(math.radians((player[1] + 180)%360)) 
				player[0][1] += pas*math.sin(math.radians((player[1] + 180)%360))


	elif (touche is "f" ) : # f pour forward ( mouvement tout droit)   
		# Calcule de la distance au mur dans la direction de omega 
		

		distancef = distance_mur(player, player[1], mapp)[0] 
		if(distancef[1] > 1.5*pas):
			player[0][0] += pas*math.cos(math.radians(player[1])) 
			player[0][1] += pas*math.sin(math.radians(player[1]))




def changeorient(player, touche):
	""" Changement d'orientation (rotation de  l'angle 
		d'orientation de 20 degres
	"""

	if touche == "d": # rotation a droite
			player[1] = (player[1] + 10)%360 
		
	elif touche == "g": # rotation a gauche  
		player[1] = (player[1] - 10)%360

