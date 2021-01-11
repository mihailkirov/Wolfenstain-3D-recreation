#!/usr/bin/env python3
# "3D" project  -- raycasting 
# main module
# by Mihail Kirov - 2018 

# DANS CETTE VERSION DU JEU LES CASES SONT CONSIDEREES DE TAILLE 64 

######################################################################################

from map import * 
from display import *

# Variable taille d'ecran et minimap 
WIDTH, HIGHT = 520, 520
width, hight = WIDTH//4, HIGHT//4 # hauteur et largeur de la mini map
# Viewport and window
Vpxa, Vpxb = 0, width 	# abcisse of viewport pour la minimap	
Vpya, Vpyb = 0, hight	# ordonate of view port pour la minimap
VIEWPORT = ((Vpxa, Vpya), (Vpxb, Vpyb))
Wxa, Wxb =  0, 16 * 64   # abcisse of window
Wya, Wyb  =  0, 16 * 64   # ordonate of window 
WINDOW = ((Wxa, Wya), (Wxb, Wyb))

####################################################################################
# Couleurs
BLACK = (0, 0, 0)
RED =   (255,   0,   0)
GREY = [69, 69, 69]
BLUE = [0, 0, 255]
RED =   (255,   0,   0)
GREEN = [0,   255,   0]
WHITE = [255, 255, 255]

#######################################################################

milieu = HIGHT/2 # x, y
_FPS = 100
_FOV = 60
PAS = 5
_CASES = 16
SIZECASE = 64 
densite_murs = 40 # pourentage de map couvert par des murs
#######################################################################




if __name__== "__main__": 

		m = init_mat(_CASES)
		m = remplissage_matrice(m, densite_murs)
		player = init_joueur(m, _CASES)
		distec = distance_ecran(_FOV, WIDTH) # distance d'ecran (constante)

		##################################################################################################3
		screen = pygame.display.set_mode((WIDTH, HIGHT))
		pygame.display.set_caption("Wolfenstain")
		clock = pygame.time.Clock()  	 
		running = True

		# Textures
		wall_img = pygame.image.load("abc.png")
		width_wall, height_wall = wall_img.get_width(), wall_img.get_height()

		# Weapon
		weapon = pygame.image.load("awp.png")
		hweap = weapon.get_height()
		screen.fill((0, 0, 0))
		###################################################################################################
		v = lancer_rayon(_FOV , WIDTH, player[1])
		x = 1 	
		liste_textures = [] # enregistrement des coord (x1,y1 ,x2 , y2) de colonnes (murs) pour les textures
		playerdc, tmpliste = [], []
		#distmax =  math.sqrt(2)*16*64 # pour ombrages
		
		for rayon in v : 
			tmp = distance_mur(player, rayon, m) # distance d'intersection et coord d'intersection
			tmp, VERTIC = tmp[0], tmp[1] # pour la texture et la minimap
			p = transformation_wc_nc_dc(tmp[0][0], WINDOW, VIEWPORT)[:2] # efacement de la 3 ieme dimention
			tmpliste += [p] # sauvegarde des intersections transformes dans l'espace ecran pour la minimap
			distint = tmp[1]*math.cos(math.radians(abs(player[1] - rayon))) # correction de fisheye
			hc = hauteur_colonne(distint, distec)
			fc = floor_coord(x, milieu, hc, HIGHT) # dessin du sol
			rc = coord_plafond(x, milieu, hc) # dessin du plafond
			mc = coord_murs_cam_centre(x, milieu, hc) 
			#dessin_mur(screen, mc[0], mc[1], RED, distmax, tmp[1])
			dessine_sol(screen, fc[0], fc[1], BLACK)
			dessine_plafond(screen, rc[0], rc[1], GREY)
			if (VERTIC):
				dessin_mur_textures(x, tmp[0][0][1], mc[0][1], hc, wall_img, SIZECASE, screen, width_wall, height_wall)
			else:
				dessin_mur_textures(x, tmp[0][0][0], mc[0][1], hc, wall_img, SIZECASE, screen, width_wall, height_wall)
			x += 1

		
		# minimap et arme
		playerdc = transformation_wc_nc_dc(player[0], WINDOW, VIEWPORT)
		pygame.draw.circle(screen, BLACK, [int(round(playerdc[0],0)) ,int(round(playerdc[1], 0))], 4) # dessin d'un cercle (joueur)dans le minimap
		murs(m, screen, width, hight, _CASES, GREEN)
		dessin_intersect(playerdc, tmpliste, screen, BLUE)
		affiche_info(player[0], clock.get_fps(), player[1], _FOV, WHITE, screen, HIGHT)
		screen.blit(weapon, (int(WIDTH/2), HIGHT - hweap)) 
		pygame.display.update()
		pygame.key.set_repeat(400, 30)

		# BOUCLE PRINCIPALE
		
		while(running):
			pygame.display.update()
			clock.tick(_FPS) # if game loop finished before fps it pauses the loop 
			pygame.event.clear()
			event = pygame.event.wait()
			
			if event.type == KEYDOWN: # on s'appuyie au bouton
					#screen.fill((0, 0, 0))
					if (event.key  == K_ESCAPE):
						running = False

					elif event.key == K_DOWN:
						deplacement(player, "b", PAS, m)
						

					elif event.key == K_UP:
						deplacement(player, "f", PAS, m)
						

					elif event.key == K_RIGHT:
						changeorient(player, "d")
						

					elif event.key == K_LEFT:
						changeorient(player, "g")
						
			
					v = lancer_rayon(_FOV , WIDTH, player[1])
					x = 1 	
					tmpliste = []
					
					for rayon in v : 
						tmp = distance_mur(player, rayon, m) # distance d'intersection et coord d'intersection
						VERTIC = tmp[1] # variable pour savoir quelle intersection de prendre 
						tmp = tmp[0]
						p = transformation_wc_nc_dc(tmp[0][0], WINDOW, VIEWPORT)[:2] # removing the 3d dimention
						tmpliste += [p] # sauvegarde des intersections transformes dans l'espace ecran
						distint = tmp[1]*math.cos(math.radians(abs(player[1] - rayon))) # correction de fisheye
						hc = hauteur_colonne(distint, distec)
						fc = floor_coord(x, milieu, hc, HIGHT)
						rc = coord_plafond(x, milieu, hc)
						mc = coord_murs_cam_centre(x, milieu, hc) # tuple
						#dessin_mur(screen, mc[0], mc[1], RED, distmax, tmp[1]) # pour ombrages
						dessine_sol(screen, fc[0], fc[1], BLACK)
						dessine_plafond(screen, rc[0], rc[1], GREY)
						if (VERTIC):
							dessin_mur_textures(x, tmp[0][0][1], mc[0][1], hc, wall_img, SIZECASE, screen, width_wall, height_wall)
						else:
							dessin_mur_textures(x, tmp[0][0][0], mc[0][1], hc, wall_img, SIZECASE, screen, width_wall, height_wall)
						
						x += 1

					# minimap et arme
					playerdc = transformation_wc_nc_dc(player[0], WINDOW, VIEWPORT)
					pygame.draw.circle(screen, BLACK, [int(round(playerdc[0],0)) ,int(round(playerdc[1], 0))], 4) # dessine de player dans le minimap
					murs(m, screen, width, hight, _CASES, GREEN)
					dessin_intersect(playerdc, tmpliste, screen, BLUE)
					affiche_info(player[0], clock.get_fps(), player[1], _FOV, WHITE, screen, HIGHT)
					screen.blit(weapon, (int(WIDTH/2), HIGHT - hweap))


		pygame.quit()