import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trapping Rain Water Animation")

# Colors
white = (255, 255, 255)
gray = (150, 150, 150)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)  # Use default font for English

# Terrain data (example)
heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
n = len(heights)
bar_width = screen_width // (2 * n + 1)
bar_spacing = bar_width
bar_scale = 50  # Height scale factor

# Precompute left_max and right_max
left_max = [0] * n
right_max = [0] * n
left_max[0] = heights[0]
for i in range(1, n):
    left_max[i] = max(left_max[i - 1], heights[i])
right_max[-1] = heights[-1]
for i in range(n - 2, -1, -1):
    right_max[i] = max(right_max[i + 1], heights[i])

# Precompute water
water = [0] * n
total_water = 0
for i in range(n):
    water[i] = max(0, min(left_max[i], right_max[i]) - heights[i])
    total_water += water[i]

# Animation state
stage = 0  # 0: terrain, 1: left_max, 2: right_max, 3: water, 4: done
index = 0  # Current bar index in the current stage
stage_names = [
    "Stage 1: Show terrain only", 
    "Stage 2: Calculate and show left_max for each position (red)", 
    "Stage 3: Calculate and show right_max for each position (green)", 
    "Stage 4: Calculate and show trapped water for each position (blue)", 
    "Stage 5: Final result, total trapped water: {}".format(total_water)
]

# Drawing functions
def draw_text(text):
    img = font.render(text, True, black)
    screen.blit(img, (30, 30))

def draw_terrain(current_heights):
    for i, height in enumerate(current_heights):
        x = i * (bar_width + bar_spacing) + bar_spacing
        y = screen_height - height * bar_scale
        pygame.draw.rect(screen, gray, (x, y, bar_width, height * bar_scale))

def draw_left_max(current_left_max):
    for i, max_h in enumerate(current_left_max):
        if max_h > 0:
            x = i * (bar_width + bar_spacing) + bar_spacing + bar_width // 2
            y = screen_height - max_h * bar_scale
            pygame.draw.circle(screen, red, (x, y), 7)

def draw_right_max(current_right_max):
    for i, max_h in enumerate(current_right_max):
        if max_h > 0:
            x = i * (bar_width + bar_spacing) + bar_spacing + bar_width // 2
            y = screen_height - max_h * bar_scale
            pygame.draw.circle(screen, green, (x, y), 7)

def draw_water(current_water, current_heights):
    for i, water_level in enumerate(current_water):
        if water_level > 0:
            x = i * (bar_width + bar_spacing) + bar_spacing
            y = screen_height - (current_heights[i] + water_level) * bar_scale
            pygame.draw.rect(screen, blue, (x, y, bar_width, water_level * bar_scale))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if stage == 0:
                    # Stage 0: only one step to next stage
                    stage = 1
                    index = 0
                elif stage == 1:
                    index += 1
                    if index >= n:
                        index = n - 1  # Clamp
                        stage = 2
                        index = n - 1  # Start from right for right_max
                elif stage == 2:
                    index -= 1
                    if index < 0:
                        index = 0
                        stage = 3
                        index = 0
                elif stage == 3:
                    index += 1
                    if index >= n:
                        index = n - 1
                        stage = 4

    screen.fill(white)
    draw_text(stage_names[stage])

    # Stage 0: Show terrain only
    if stage == 0:
        draw_terrain(heights)
    # Stage 1: Show left_max step by step (left to right)
    elif stage == 1:
        draw_terrain(heights)
        left_max_partial = [left_max[i] if i <= index else 0 for i in range(n)]
        draw_left_max(left_max_partial)
    # Stage 2: Show right_max step by step (right to left)
    elif stage == 2:
        draw_terrain(heights)
        draw_left_max(left_max)
        right_max_partial = [right_max[i] if i >= index else 0 for i in range(n)]
        draw_right_max(right_max_partial)
    # Stage 3: Show water step by step (left to right)
    elif stage == 3:
        draw_terrain(heights)
        draw_left_max(left_max)
        draw_right_max(right_max)
        water_partial = [water[i] if i <= index else 0 for i in range(n)]
        draw_water(water_partial, heights)
    # Stage 4: Show all
    else:
        draw_terrain(heights)
        draw_left_max(left_max)
        draw_right_max(right_max)
        draw_water(water, heights)
        # Highlight total water
        total_text = font.render(f"Total trapped water: {total_water}", True, blue)
        screen.blit(total_text, (30, 70))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()