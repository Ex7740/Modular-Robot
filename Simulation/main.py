import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Draggable Box")
clock = pygame.time.Clock()

# Main Body
box = pygame.Rect(300, 300, 120, 80)
box_color = (80, 180, 255)

dragging = False
offset_x = 0
offset_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if box.collidepoint(event.pos):
                dragging = True
                # Store offset between mouse and box corner
                offset_x = box.x - event.pos[0]
                offset_y = box.y - event.pos[1]

        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

        # Mouse movement
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                box.x = event.pos[0] + offset_x
                box.y = event.pos[1] + offset_y

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, box_color, box)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
