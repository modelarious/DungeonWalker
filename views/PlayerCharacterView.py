from views.ViewBaseClass import ViewBaseClass
import pygame
from oldsettings import charSet

# XXX DELETE THIS CLASS 
# draws the player to the screen
class PlayerCharacterView(ViewBaseClass):
	def __init__(self, grid_size):
		self.grid_size = grid_size
		
	def updateView(self, game_screen, character_model):
		x, y = character_model.get_pos()
		BLACK = (0, 255, 0)
		#draw an x in the space alotted
		#pygame.draw.line(game_screen, BLACK, (x, y), (x+grid_size, y+grid_size))
		r = pygame.Rect(x, y, self.grid_size + x, self.grid_size + y)
		pygame.draw.rect(game_screen, BLACK, r)
		#pygame.
		#tile.draw_pygame_representation(game_screen, character_model.get_x() // grid_size, character_model.get_y() // grid_size, y % 769, (y + grid_size)% 769)


		# y = 0
		# for row in mapModel.get_board():
		# 	x = 0
		# 	for tile in row:
		# 		tile.draw_pygame_representation(game_screen, x % 1025, (x + grid_size) % 1025, y % 769, (y + grid_size)% 769)
		# 		x += grid_size

		# 	row = list(map(lambda a : a.get_char(), row))
			
		# 	# XXX this processing should be done in the board generation step
		# 	print("".join(row).replace(charSet["pathTemp"], charSet["passable"]).replace(charSet["anchor"],
		# 																				 charSet["passable"]))
		# 	y += grid_size
		# print()
