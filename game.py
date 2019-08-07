import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0)
BACKGROUND_COLOR = (0,0,0)

player_size = 30
player_pos = [WIDTH/2, HEIGHT-2*player_size]

""" enemy_size = 50
enemy_speed = 10 """
enemy_array = [15, 1 ]

enemy_pos = [random.randint(0, WIDTH-enemy_array[0]), 0]
enemy_list = [enemy_pos]






screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, enemy_array):
	size = enemy_array[0]
	speed = enemy_array[1]
	if score < 20:
		speed = 5
		size = 15 
	elif score < 40:
		speed = 8
		size = 25
	elif score < 60:
		speed = 12
		size = 40
	else:
		speed = 15
		size = 50
	enemy_array = [size, speed]
	return enemy_array

def drop_enemies(enemy_list, enemy_array):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0, WIDTH - enemy_array[0])
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list, enemy_array):
	size = enemy_array[0]
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], size, size))

def update_enemy_positions(enemy_list, score, enemy_array):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += enemy_array[1]
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos, enemy_array):
			return True
	return False


def detect_collision(player_pos, enemy_pos, enemy_array):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_array[0])):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_array[0])):
			return True
	return False


	

while not game_over:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			x = player_pos[0]
			y = player_pos[1]
			if event.key == pygame.K_LEFT:
				x -= player_size/2
			elif event.key == pygame.K_RIGHT:
				x += player_size/2

			player_pos = [x,y]

	
	# update pos of enemy
	screen.fill(BACKGROUND_COLOR)

	enemy_array = set_level(score, enemy_array)

	drop_enemies(enemy_list, enemy_array)

	score = update_enemy_positions(enemy_list, score, enemy_array)
	

	if collision_check(enemy_list, player_pos):
		game_over = True
		print("Game Over!")
		print("Score:" + str(score))
		break
		
	draw_enemies(enemy_list, enemy_array)
	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	pygame.draw.rect(screen, RED , (player_pos[0], player_pos[1], player_size, player_size))
	
	clock.tick(30)
	pygame.display.update()