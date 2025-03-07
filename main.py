import pygame
import random
import sys

# ========================
# Configuració inicial
# ========================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACE_BLUE = (10, 10, 50)  # Blau espacial fosc
NEON_BLUE = (30, 144, 255)  # Blau neó vibrant
DEEP_PURPLE = (75, 0, 130)  # Porpra profund (Indigo)
LAVENDER = (150, 100, 255)  # Lavanda suau
CYAN_GLOW = (0, 255, 255)  # Blau cian lluminós
SOFT_LILAC = (200, 162, 200)  # Lila suau
DARK_PURPLE = (48, 25, 52)  # Porpra fosc
RED = (255, 0, 0)  # ✅ Color vermell per als projectils
SPACE_BLUE = (10, 10, 50)  # Un to blau fosc espacial
NEON_GREEN = (57, 255, 20)  # Verd neó
NEON_RED = (255, 0, 50)  # Vermell neó

# Colors alternatius si vols una mica més de varietat:
MIDNIGHT_BLUE = (25, 25, 112)  # Blau mitjanit
ELECTRIC_PURPLE = (138, 43, 226)  # Púrpura elèctric


# Inicialitzar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Joc de l'Astronauta 🚀")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Orbitron", 28) or pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Orbitron", 70) or pygame.font.SysFont("Arial", 70)

# Música i efectes de so
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
powerup_sound = pygame.mixer.Sound("powerup.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
shoot_sound = pygame.mixer.Sound("shoot.wav")

# Carregar imatges
astronauta_img = pygame.image.load("astronauta.png")
astronauta_img = pygame.transform.scale(astronauta_img, (100, 100))
asteroide_img = pygame.image.load("asteroide.png").convert_alpha()
energia_img = pygame.image.load("energia.png")
energia_img = pygame.transform.scale(energia_img, (60, 60))
vida_icon = pygame.transform.scale(energia_img, (30, 30))

# ========================
# Variables Globals
# ========================
score = 0
difficulty_level = 1
lives = 3
paused = False
running = True
ADD_OBSTACLE = pygame.USEREVENT + 1
ADD_POWERUP = pygame.USEREVENT + 2

# ========================
# Funcions Auxiliars
# ========================

def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_lives(surface, x, y, lives):
    for i in range(lives):
        surface.blit(vida_icon, (x + i * 35, y))
# ========================
# Pantalla de pausa
# ========================
def show_pause_screen():
    """Mostra un missatge de pausa en pantalla."""
    screen.fill(DARK_PURPLE)  # Fons porpra fosc
    draw_text(screen, "PAUSA", big_font, NEON_BLUE, WIDTH // 2, HEIGHT // 2 - 50, center=True)
    draw_text(screen, "Prem P per continuar", font, WHITE, WIDTH // 2, HEIGHT // 2 + 20, center=True)
    pygame.display.flip()

    paused_waiting = True
    while paused_waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused_waiting = False  # Reprendre el joc

# ========================
# Pantalla d'inici
# ========================
def show_start_screen():
    """Mostra la pantalla d'inici amb un estil millorat."""
    screen.fill(SPACE_BLUE)  # Fons blau espacial fosc
    draw_text(screen, " JOC DE L'ASTRONAUTA ", big_font, NEON_BLUE, WIDTH // 2, 100, center=True)
    draw_text(screen, "OBJECTIU: Sobreviu i evita els asteroides!", font, CYAN_GLOW, WIDTH // 2, 180, center=True)
    draw_text(screen, "CONTROLS:", font, ELECTRIC_PURPLE, WIDTH // 2, 250, center=True)
    draw_text(screen, " FLETXES : Moure", font, LAVENDER, WIDTH // 2, 280, center=True)
    draw_text(screen, " ESPAI : Disparar", font, LAVENDER, WIDTH // 2, 310, center=True)
    draw_text(screen, " P : Pausa", font, LAVENDER, WIDTH // 2, 340, center=True)
    draw_text(screen, " Recull energia per guanyar vides!", font, SOFT_LILAC, WIDTH // 2, 380, center=True)
    draw_text(screen, " PREM QUALSSEVOL TECLA PER COMENÇAR ", font, ELECTRIC_PURPLE, WIDTH // 2, 450, center=True)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# ========================
# Classes del Joc
# ========================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = astronauta_img
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        """Dispara un projectil."""
        shoot_sound.play()
        shot = Shot(self.rect.right, self.rect.centery)
        all_sprites.add(shot)
        shots.add(shot)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(asteroide_img, (random.randint(40, 80), random.randint(40, 80)))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)

    def update(self):
        global score
        if not paused:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                score += 1
                self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = energia_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(50, HEIGHT - 50)
        self.speed = 4

    def update(self):
        if not paused:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.kill()

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# ========================
# Funció per reiniciar el Joc
# ========================

def new_game():
    global score, difficulty_level, lives, paused
    score = 0
    difficulty_level = 1
    lives = 3
    paused = False
    pygame.time.set_timer(ADD_OBSTACLE, 1500)
    pygame.time.set_timer(ADD_POWERUP, 5000)
    global all_sprites, obstacles, powerups, player, shots
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

# ========================
# Pantalla de Game Over
# ========================
def show_game_over(final_score):
    """Mostra una pantalla de Game Over millorada."""
    screen.fill(NEON_RED)
    draw_text(screen, "GAME OVER", big_font, WHITE, WIDTH // 2, 200, center=True)
    draw_text(screen, f"Puntuació Final: {final_score}", font, WHITE, WIDTH // 2, 300, center=True)
    draw_text(screen, "Prem P per reiniciar", font, BLACK, WIDTH // 2, 350, center=True)
    pygame.display.flip()

    pygame.mixer.music.stop()
    game_over_sound.play()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.mixer.music.play(-1)
                waiting = False

# ========================
# Bucle principal
# ========================
show_start_screen()  # ✅ Pantalla d'inici abans de començar el joc

while True:
    new_game()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                        show_pause_screen()  # ✅ Ara es mostra la pantalla de pausa
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_SPACE and not paused:
                    player.shoot()
            elif event.type == ADD_OBSTACLE and not paused:
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            elif event.type == ADD_POWERUP and not paused:
                powerup = PowerUp()
                all_sprites.add(powerup)
                powerups.add(powerup)

        if not paused:
            all_sprites.update()

            # Verificar col·lisions amb obstacles (perdre vides)
            if pygame.sprite.spritecollide(player, obstacles, True):
                crash_sound.play()
                lives -= 1
                if lives <= 0:
                    running = False  # Això fa sortir del bucle i mostrar Game Over

            # Verificar col·lisions amb power-ups (guanyar vides)
            for powerup in pygame.sprite.spritecollide(player, powerups, True):
                powerup_sound.play()
                lives += 1

            # Verificar col·lisions entre trets i obstacles (eliminar obstacles)
            pygame.sprite.groupcollide(obstacles, shots, True, True)

        screen.fill(SPACE_BLUE)  # Fons del joc corregit
        all_sprites.draw(screen)
        draw_text(screen, f"Puntuació: {score}", font, CYAN_GLOW, 10, 10)
        draw_lives(screen, 10, 40, lives)
        pygame.display.flip()

    show_game_over(score)  # ✅ Ara es mostra correctament