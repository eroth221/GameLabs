import pygame, sys
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
blip = pygame.mixer.Sound('sound.wav')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
opp_rect = pygame.Rect((780, 300), (PADDLE_WIDTH, PADDLE_HEIGHT))
mid_rect = pygame.Rect((400, 0), (1, 800))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
opponent = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)
#R_text = font.render(str(R_win), True, (0, 0, 0))

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_w] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	if pygame.key.get_pressed()[pygame.K_UP] and opp_rect.top > 0:
                opp_rect.top -= BALL_SPEED
        elif pygame.key.get_pressed()[pygame.K_DOWN] and opp_rect.bottom < SCREEN_HEIGHT:
                opp_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if ball_rect.right >= SCREEN_WIDTH:
		score += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
	if ball_rect.left <= 0:
		opponent += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))


	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		blip.play()
	if opp_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		blip.play()

	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), opp_rect) # opponents paddle
	pygame.draw.rect(screen, (255, 0, 0), mid_rect) # center line
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text = font.render(str(score), True, (0, 0, 0))
	opp_score = font.render(str(opponent), True, (0, 0, 0))
	screen.blit(score_text, (((SCREEN_WIDTH / 2)- 20) - font.size(str(score))[0] / 2, 5)) # The score
	screen.blit(opp_score, (((SCREEN_WIDTH / 2) + 20) - font.size(str(opponent))[0] / 2, 5))	
	# Update screen and wait 20 milliseconds
	if opponent >= 11:
		R_win = font.render("Right Wins!", True, (0, 0, 0))
		screen.blit(R_win, (400, 300))
		Restart = font.render("Restart?", True, (0, 0, 0))
		screen.blit(Restart, (400, 330))
		P_Y = font.render("Press Y", True, (0, 0, 0))
		screen.blit(P_Y , (400, 360))
	if score >= 11:
		L_win = font.render("Left Wins", True, (0, 0, 0))
		screen.blit(L_win, (290, 300))
		Restart = font.render("Restart?", True, (0, 0, 0))
		screen.blit(Restart, (290, 330))
		P_Y = font.render("Press Y", True, (0, 0, 0))
		screen.blit(P_Y , (290, 360))
	pygame.display.flip()
	pygame.time.delay(20)

