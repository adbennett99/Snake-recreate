import pygame
import random

from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
	K_RETURN,
)

from snake_classes import *
from snake_database import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#---------------------------------------------------------------------------------
def main_menu():

	#changes window dimensions
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

	#background
	screen.fill((0, 0, 0))

	#creates the "Snake" label
	text = pygame.font.Font('freesansbold.ttf',100)
	textSurf = text.render("Snake", True, (23, 255, 0))
	textRect = textSurf.get_rect()
	textRect.center = ((SCREEN_WIDTH / 2), 150)
	
	#Another main screen label
	text_2 = pygame.font.Font('freesansbold.ttf',60)
	textSurf_2 = text_2.render("Press 'ENTER'", True, (255, 255, 255))
	textRect_2 = textSurf_2.get_rect()
	textRect_2.center = ((SCREEN_WIDTH / 2), 320)

	#another main screen label
	text_3 = pygame.font.Font('freesansbold.ttf',60)
	textSurf_3 = text_3.render("to play", True, (255, 255, 255))
	textRect_3 = textSurf_3.get_rect()
	textRect_3.center = ((SCREEN_WIDTH / 2), 400)

	#actually puts the labels onto the window
	screen.blit(textSurf, textRect)
	screen.blit(textSurf_2, textRect_2)
	screen.blit(textSurf_3, textRect_3)

	#updates the window
	pygame.display.flip()

	#main menu loop
	main_menu_loop = True
	while main_menu_loop:

		for event in pygame.event.get():

			#if user presses the "Enter Key", the main menu loop quits and the game begins
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					main_menu_loop = False
					game_loop()

			#quits main menu loop if the window is closed
			elif event.type == QUIT:
				main_menu_loop = False

#---------------------------------------------------------------------------------
def game_over(score):
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

	#background
	screen.fill((0, 0, 0))

	current_highscore = get_high_score()
	if score > current_highscore:
		
		new_high = pygame.font.Font('freesansbold.ttf', 65)
		new_high_surf = new_high.render("New Highscore!", True, (198, 83, 198))
		new_high_rect = new_high_surf.get_rect()
		new_high_rect.center = ((SCREEN_WIDTH / 2), 200)

		# Need to figure out how to have pygame take user input 
		# to incorporate the name feature
		insert_new_score('Name', score)

		screen.blit(new_high_surf, new_high_rect)


	#game over label
	text = pygame.font.Font('freesansbold.ttf', 85)
	textSurf = text.render("Game over", True, (255, 0, 0))
	textRect = textSurf.get_rect()
	textRect.center = ((SCREEN_WIDTH / 2), 100)

	#shows the user score label
	text_4 = pygame.font.Font('freesansbold.ttf', 65)
	textSurf_4 = text_4.render("Score: " + str(score), True, (255, 255, 255))
	textRect_4 = textSurf_4.get_rect()
	textRect_4.center = ((SCREEN_WIDTH / 2), 300)
	
	#enter to play again label
	text_2 = pygame.font.Font('freesansbold.ttf',30)
	textSurf_2 = text_2.render("Press 'ENTER' to play again", True, (255, 255, 255))
	textRect_2 = textSurf_2.get_rect()
	textRect_2.center = ((SCREEN_WIDTH / 2), 420)

	#esc to quit label
	text_3 = pygame.font.Font('freesansbold.ttf',30)
	textSurf_3 = text_3.render("Press 'ESC' to quit", True, (255, 255, 255))
	textRect_3 = textSurf_3.get_rect()
	textRect_3.center = ((SCREEN_WIDTH / 2), 460)

	#commits labels to screen
	screen.blit(textSurf, textRect)
	screen.blit(textSurf_4, textRect_4)
	screen.blit(textSurf_2, textRect_2)
	screen.blit(textSurf_3, textRect_3)

	#updates the screen
	pygame.display.flip()

	#game over loop
	game_over_loop = True
	while game_over_loop:

		for event in pygame.event.get():
			if event.type == KEYDOWN:

				#if user presses "Enter" key, the game loop begins again
				if event.key == K_RETURN:
					game_over_loop = False
					game_loop()

				#if user presses "ESC" key, the window closes
				if event.key == K_ESCAPE:
					game_over_loop = False

			#ends loop if window is closed
			elif event.type == QUIT:
				game_over_loop = False

#---------------------------------------------------------------------------------
def game_loop():

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT + 40])

	score = 0

	SNAKE_BODY_LIST = []
	SNAKE_LENGTH = 0

	snake_body_group = pygame.sprite.Group()

	snake_head = Snake_head()
	apple = Apple(snake_body_group)

	clock = pygame.time.Clock()

	current_highscore = get_high_score()

	running = True
	while running:
		for event in pygame.event.get():
			
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False

			elif event.type == QUIT:
				running = False

		screen.fill((0, 0, 0))

		screen.blit(snake_head.surf, snake_head.rect)
		screen.blit(apple.surf, apple.rect)

		pygame.draw.rect(screen,(166, 166, 166),(0,600,SCREEN_WIDTH,40))
		update_score(score)
		high_score(current_highscore)

		for entity in reversed(SNAKE_BODY_LIST):
			screen.blit(entity.surf, entity.rect)
			entity.update()

		if pygame.sprite.collide_rect(snake_head, apple):
			apple.update()

			score = score + 100
			update_score(score)

			snake_part = Snake_body(SNAKE_LENGTH, snake_head, SNAKE_BODY_LIST)
			SNAKE_BODY_LIST.append(snake_part)
			snake_body_group.add(snake_part)
			SNAKE_LENGTH += 1

		pressed_keys = pygame.key.get_pressed()
		snake_head.update(pressed_keys)

		if pygame.sprite.spritecollideany(snake_head, snake_body_group):
			running = False
			game_over(score)

		if (snake_head.rect.left < 0) or (snake_head.rect.right > SCREEN_WIDTH) or (snake_head.rect.top < 0) or (snake_head.rect.bottom > SCREEN_HEIGHT):
			running = False
			game_over(score)

		pygame.display.flip()

		clock.tick(8)

#---------------------------------------------------------------------------------
def update_score(score):

	text = pygame.font.Font('freesansbold.ttf', 40)
	textSurf = text.render("Score: " + str(score), True, (0, 35, 255))
	textRect = textSurf.get_rect()
	textRect.topleft = (10, 600)

	screen.blit(textSurf, textRect)

def high_score(current_highscore):
	hscore = pygame.font.Font('freesansbold.ttf', 40)
	hscoreSurf = hscore.render("PB: " + str(current_highscore), True, (0, 35, 255))
	hscoreRect = hscoreSurf.get_rect()
	hscoreRect.topleft = (400, 600)

	screen.blit(hscoreSurf, hscoreRect)

#---------------------------------------------------------------------------------

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

main_menu()

pygame.quit()

cursor.close()
cnx.close()