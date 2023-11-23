import pygame
import sys
import random
import serial

# Initialize Pygame
pygame.init()
width, height = 600, 1200
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Avoid the Obstacle Car Game")

# Load road background
road_image = pygame.image.load("road.jpg")
road_image = pygame.transform.scale(road_image, (width, height))

# Set up the car
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (150, int(150 / car_image.get_width() * car_image.get_height())))
car_rect = car_image.get_rect()
car_rect.center = (width / 2, height - 150)

# Set up obstacles
obstacle_image = pygame.image.load("obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (int(0.1 * obstacle_image.get_width()), int(0.1 * obstacle_image.get_height())))
obstacle_rect = obstacle_image.get_rect()
obstacle_rect.center = (random.randint(0, width), -obstacle_rect.height)

# Scrolling background variables
scroll_speed = 10
background_y = 0
car_speed = 20
score = 0
is_in_menu = True
serial_data = ""

ser = serial.Serial('COM3', 115200)

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ser.in_waiting > 0:
        serial_data = ser.readline().decode().strip()

    keys = pygame.key.get_pressed()
    if is_in_menu:
        if serial_data == "s" or keys[pygame.K_SPACE]:
            is_in_menu = False
            score = 0
    else:
        # Game logic
        if serial_data == "w":
            car_rect.y -= car_speed / 2
        elif serial_data == "s":
            car_rect.y += car_speed / 2
        elif serial_data == "a":
            car_rect.x -= car_speed
        elif serial_data == "d":
            car_rect.x += car_speed

        # Update obstacle position
        obstacle_rect.y += scroll_speed
        if obstacle_rect.y > height:
            obstacle_rect.y = 0
            obstacle_rect.x = random.randint(0, width)
            score += 1

        # Update scrolling background position
        background_y += scroll_speed
        if background_y >= height:
            background_y = 0

        # Ensure car stays within the window
        car_rect.x = max(0, min(car_rect.x, width - car_rect.width))
        car_rect.y = max(0, min(car_rect.y, height - car_rect.height))
        obstacle_rect.x = max(0, min(obstacle_rect.x, width - obstacle_rect.width))

        # Check for collisions
        if car_rect.colliderect(obstacle_rect):
            is_in_menu = True
            car_rect.center = (width / 2, height - 150)
            obstacle_rect.center = (random.randint(0, width), -obstacle_rect.height)

    # Draw scrolling road background
    window.blit(road_image, (0, background_y - height))
    window.blit(road_image, (0, background_y))

    if is_in_menu:
        # Display menu text
        font = pygame.font.Font(None, 36)
        text = font.render("Swipe Down to Start!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width / 2, height / 2))
        window.blit(text, text_rect)
        # Update scrolling background position
        background_y += scroll_speed
        if background_y >= height:
            background_y = 0

    # Draw car and obstacle
    window.blit(car_image, car_rect)
    window.blit(obstacle_image, obstacle_rect)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(30)
