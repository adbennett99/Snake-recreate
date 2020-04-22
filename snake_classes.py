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


#---------------------------------------------------------------------------------
class Snake_head(pygame.sprite.Sprite):

	def __init__(self):
		super(Snake_head, self).__init__()
		self.surf = pygame.Surface((20, 20))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()
		self.curr_direction = "RIGHT"

	def update(self, pressed_keys):
		if pressed_keys[K_UP] and self.curr_direction != "DOWN":
			self.curr_direction = "UP"
		if pressed_keys[K_DOWN] and self.curr_direction != "UP":
			self.curr_direction = "DOWN"
		if pressed_keys[K_LEFT] and self.curr_direction != "RIGHT":
			self.curr_direction = "LEFT"
		if pressed_keys[K_RIGHT] and self.curr_direction != "LEFT":
			self.curr_direction = "RIGHT"

		if self.curr_direction == "RIGHT":
			self.rect.move_ip(20, 0)
		if self.curr_direction == "LEFT":
			self.rect.move_ip(-20, 0)
		if self.curr_direction == "DOWN":
			self.rect.move_ip(0, 20)
		if self.curr_direction == "UP":
			self.rect.move_ip(0, -20)

#---------------------------------------------------------------------------------
class Snake_body(pygame.sprite.Sprite):

	def __init__(self, length, snake_head, body_list):
		super(Snake_body, self).__init__()
		self.surf = pygame.Surface((20, 20))
		self.surf.fill((255, 255, 255))

		self.position = length
		self.snake_head = snake_head
		self.SNAKE_BODY_LIST = body_list

		if self.position == 0:
			self.curr_direction = self.snake_head.curr_direction
			prev_center = self.snake_head.rect.center
			self.rect = self.surf.get_rect(center=(prev_center[0], prev_center[1]))
		else:
			self.curr_direction = self.SNAKE_BODY_LIST[self.position - 1].curr_direction
			prev_center = self.SNAKE_BODY_LIST[self.position - 1].rect.center

			if self.curr_direction == "RIGHT":
				self.rect = self.surf.get_rect(center=(prev_center[0] - 20, prev_center[1]))
			if self.curr_direction == "LEFT":
				self.rect = self.surf.get_rect(center=(prev_center[0] + 20, prev_center[1]))
			if self.curr_direction == "DOWN":
				self.rect = self.surf.get_rect(center=(prev_center[0], prev_center[1] - 20))
			if self.curr_direction == "UP":
				self.rect = self.surf.get_rect(center=(prev_center[0], prev_center[1] + 20))

	def update(self):
		if self.position == 0:
			self.curr_direction = self.snake_head.curr_direction
		else:
			self.curr_direction = self.SNAKE_BODY_LIST[self.position - 1].curr_direction

		if self.curr_direction == "RIGHT":
			self.rect.move_ip(20, 0)
		if self.curr_direction == "LEFT":
			self.rect.move_ip(-20, 0)
		if self.curr_direction == "DOWN":
			self.rect.move_ip(0, 20)
		if self.curr_direction == "UP":
			self.rect.move_ip(0, -20)

#---------------------------------------------------------------------------------
class Apple(pygame.sprite.Sprite):
	def __init__(self, snake_body_group):
		super(Apple, self).__init__()
		self.surf = pygame.Surface((20, 20))
		self.surf.fill((255, 0, 0))

		self.snake_body_group = snake_body_group
		self.Snake_head = Snake_head

		width = 20 * random.randint(1, 29)
		height = 20 * random.randint(1, 29)
		self.rect = self.surf.get_rect(topleft=(width, height))

	def update(self):
		new_width = 20 * random.randint(0, 29)
		new_height = 20 * random.randint(0, 29)
		self.rect = self.surf.get_rect(topleft=(new_width, new_height))

		if pygame.sprite.spritecollideany(self, self.snake_body_group):
			self.update()