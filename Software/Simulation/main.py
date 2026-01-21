import pygame
import math

# ---------------- CONFIG ----------------
Screen_height = 600
Screen_width = 1000
# Swap width and height for 90-degree rotation
Main_Body_width = 320
Main_Body_height = 180
ATTACH_DISTANCE = 25

ATTACH_OFFSETS = {
    "top_left": (90, 0),     # x, y offsets
    "top_right": (-90, 0),
    "bottom_left": (90, 0),
    "bottom_right": (-90, 0),
}



# Menu
MENU_HEIGHT = 40
MENU_BG = (50, 50, 50)
MENU_TEXT = (220, 220, 220)
BUTTON_BG = (80, 80, 80)
BUTTON_HOVER = (110, 110, 110)

pygame.init()
screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("Modular Robot Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ---------------- MAIN BODY ----------------
Main_Body = pygame.Rect(
    (Screen_width - Main_Body_width) // 2,
    (Screen_height - Main_Body_height) // 2,
    Main_Body_width,
    Main_Body_height
)
main_color = (112, 108, 97)

# ---------------- MENU ----------------
menu_open = False
add_button = pygame.Rect(10, 5, 100, 30)
delete_button = pygame.Rect(120, 5, 120, 30)

def draw_menu(surface, mouse_pos):
    pygame.draw.rect(surface, MENU_BG, (0, 0, Screen_width, MENU_HEIGHT))

    add_color = BUTTON_HOVER if add_button.collidepoint(mouse_pos) else BUTTON_BG
    pygame.draw.rect(surface, add_color, add_button)
    surface.blit(font.render("Add Addon", True, MENU_TEXT),
                 (add_button.x + 10, add_button.y + 7))

    del_color = BUTTON_HOVER if delete_button.collidepoint(mouse_pos) else BUTTON_BG
    pygame.draw.rect(surface, del_color, delete_button)
    surface.blit(font.render("Delete Addon", True, MENU_TEXT),
                 (delete_button.x + 10, delete_button.y + 7))

# ---------------- ADDON CLASS ----------------
class Addon:
    def __init__(self, x, y, width=80, height=80, color=(160, 120, 90)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dragging = False
        self.attached = False
        self.attached_side = None
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event):
        # Block interaction through menu
        if menu_open and event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] <= MENU_HEIGHT:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.attached = False
                self.attached_side = None
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.x = event.pos[0] + self.offset_x
            self.rect.y = event.pos[1] + self.offset_y

    def update(self, main_body):
        if not self.attached and not self.dragging:
            # -------- 4-LEG ATTACHMENT POINTS FOR ROTATED BODY --------
            # How much the addon is offset from each corner
      
            
            points = {
                "top_left": (main_body.left - self.rect.width + ATTACH_OFFSETS["top_left"][0],
                            main_body.top - self.rect.height + ATTACH_OFFSETS["top_left"][1]),
                "top_right": (main_body.right + ATTACH_OFFSETS["top_right"][0],
                            main_body.top - self.rect.height + ATTACH_OFFSETS["top_right"][1]),
                "bottom_left": (main_body.left - self.rect.width + ATTACH_OFFSETS["bottom_left"][0],
                                main_body.bottom + ATTACH_OFFSETS["bottom_left"][1]),
                "bottom_right": (main_body.right + ATTACH_OFFSETS["bottom_right"][0],
                                main_body.bottom + ATTACH_OFFSETS["bottom_right"][1]),
            }
            closest_side = None
            closest_dist = float("inf")

            for side, (tx, ty) in points.items():
                dist = math.hypot(self.rect.x - tx, self.rect.y - ty)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_side = side

            if closest_dist < ATTACH_DISTANCE:
                self.attached = True
                self.attached_side = closest_side
                self.rect.topleft = points[closest_side]

        if self.attached:
            ox, oy = ATTACH_OFFSETS[self.attached_side]
            if self.attached_side == "top_left":
                self.rect.topleft = (main_body.left - self.rect.width + ox, main_body.top - self.rect.height + oy)
            elif self.attached_side == "top_right":
                self.rect.topleft = (main_body.right + ox, main_body.top - self.rect.height + oy)
            elif self.attached_side == "bottom_left":
                self.rect.topleft = (main_body.left - self.rect.width + ox, main_body.bottom + oy)
            elif self.attached_side == "bottom_right":
                self.rect.topleft = (main_body.right + ox, main_body.bottom + oy)



        # -------- EDGE DETECTION --------
        self.rect.x = max(0, min(self.rect.x, Screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, Screen_height - self.rect.height))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# ---------------- CREATE ADDONS ----------------
addons = [
    Addon(10, MENU_HEIGHT + 10),
    Addon(10, MENU_HEIGHT + 30),
]
addon_spawn_index = len(addons)

# ---------------- MAIN LOOP ----------------
dragging_main = False
offset_x = 0
offset_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Ctrl + M toggles menu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
                menu_open = not menu_open

        # Menu clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_open and event.pos[1] <= MENU_HEIGHT:
                if add_button.collidepoint(event.pos):
                    addons.append(
                        Addon(
                            10,
                            MENU_HEIGHT + 10 + addon_spawn_index * 20
                        )
                    )
                    addon_spawn_index += 1
                elif delete_button.collidepoint(event.pos) and addons:
                    addons.pop()
                    addon_spawn_index = max(0, addon_spawn_index - 1)
                continue

            # Main body dragging
            if (not menu_open or event.pos[1] > MENU_HEIGHT) and Main_Body.collidepoint(event.pos):
                dragging_main = True
                offset_x = Main_Body.x - event.pos[0]
                offset_y = Main_Body.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging_main = False

        elif event.type == pygame.MOUSEMOTION and dragging_main:
            Main_Body.x = event.pos[0] + offset_x
            Main_Body.y = event.pos[1] + offset_y

            Main_Body.x = max(0, min(Main_Body.x, Screen_width - Main_Body_width))
            Main_Body.y = max(0, min(Main_Body.y, Screen_height - Main_Body_height))

        # Send events to addons
        for addon in addons:
            addon.handle_event(event)

    # Update addons
    for addon in addons:
        addon.update(Main_Body)

    # -------- DRAW --------
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, main_color, Main_Body)

    for addon in addons:
        addon.draw(screen)

    if menu_open:
        draw_menu(screen, pygame.mouse.get_pos())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
