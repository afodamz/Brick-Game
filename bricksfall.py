import pygame
import random
import sys


pygame.init()

# set up the screen
# size = [800, 600]  # [Width, Height]
width = 800
height = 600
screen = pygame.display.set_mode([width,height])

# width, height
player_size = 50

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
player_position = [width/2, height - (2*player_size)]
BACKGROUND_COLOR = (11, 238, 207)

enemy_size = 50
enemy_position = [(random.randint(0, width/2 - enemy_size)), 0]
enemy_list = [enemy_position]
print(enemy_list)


speed_up = 10

game_over = False

score = 0

clock = pygame.time.Clock()


myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, speed_up):
	if score < 20:
		speed_up = 5
	elif score < 40:
		speed_up = 8
	elif score < 60:
		speed_up = 12
	else:
		speed_up = 15
	return speed_up
	
	# speed_up = score/5 + 1
	# return speed_up



def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_position = random.randint(0, width - enemy_size)
		y_position = 0
		enemy_list.append([x_position, y_position])


def draw_enemies(enemy_list):
	for enemy_position in enemy_list:
		pygame.draw.rect(
		    screen, BLUE, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
	for idx, enemy_position in enumerate(enemy_list):
		if enemy_position[1] >= 0 and enemy_position[1] < height:
			enemy_position[1] += speed_up
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_position):
	for enemy_position in enemy_list:
		if detect_collision(enemy_position, player_position):
			return True
	return False

def detect_collision(enemy_position, player_position):
	p_x = player_position[0]
	p_y = player_position[1]

	e_x = enemy_position[0]
	e_y = enemy_position[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if  (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True
	return False






while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
        	x = player_position[0]
        	y = player_position[1]
        	if event.key == pygame.K_LEFT and x > 0:
        		x -= 50
        	elif event.key == pygame.K_RIGHT and x < width - 50:
        		x += 50


        	player_position = [x,y]

    screen.fill(BACKGROUND_COLOR)



    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    speed_up = set_level(score, speed_up)


    text = "SCORE:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (width-200, height-40))

    if collision_check(enemy_list, player_position):
    	game_over = True

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, RED, (player_position[0], player_position[1],player_size,player_size))

    clock.tick(20)

    pygame.display.update()