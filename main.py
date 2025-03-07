# Importació de llibreries necessàries
import pygame  # Llibreria per a la creació de jocs
import random  # Llibreria per a generar números aleatoris
import sys     # Llibreria per a gestionar la sortida del programa

# ========================
# Configuració inicial
# ========================
WIDTH = 800   # Amplada de la finestra del joc
HEIGHT = 600  # Alçada de la finestra del joc
FPS = 60      # Fotogrames per segon (velocitat del joc)

# Definició de colors
WHITE = (255, 255, 255)          # Blanc
BLACK = (0, 0, 0)                # Negre
SPACE_BLUE = (10, 10, 50)        # Blau espacial fosc
NEON_BLUE = (30, 144, 255)       # Blau neó vibrant
DEEP_PURPLE = (75, 0, 130)       # Porpra profund (Indigo)
LAVENDER = (150, 100, 255)       # Lavanda suau
CYAN_GLOW = (0, 255, 255)        # Blau cian lluminós
SOFT_LILAC = (200, 162, 200)     # Lila suau
DARK_PURPLE = (48, 25, 52)       # Porpra fosc
RED = (255, 0, 0)                # Vermell (per als projectils)
NEON_GREEN = (57, 255, 20)       # Verd neó
NEON_RED = (255, 0, 50)          # Vermell neó
MIDNIGHT_BLUE = (25, 25, 112)    # Blau mitjanit
ELECTRIC_PURPLE = (138, 43, 226) # Púrpura elèctric

# Inicialització de Pygame
pygame.init()  # Inicialitza tots els mòduls de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la finestra del joc
pygame.display.set_caption("🚀 Joc de l'Astronauta 🚀")  # Títol de la finestra
clock = pygame.time.Clock()  # Objecte per controlar el temps del joc

# Configuració de fonts
font = pygame.font.SysFont("Orbitron", 28) or pygame.font.SysFont("Arial", 28)  # Font per a textos normals
big_font = pygame.font.SysFont("Orbitron", 70) or pygame.font.SysFont("Arial", 70)  # Font per a textos grans

# Configuració de música i efectes de so
pygame.mixer.init()  # Inicialitza el mòdul de so
pygame.mixer.music.load("background.mp3")  # Carrega la música de fons
pygame.mixer.music.play(-1)  # Reprodueix la música en bucle infinit
powerup_sound = pygame.mixer.Sound("powerup.wav")  # So per als power-ups
game_over_sound = pygame.mixer.Sound("game_over.wav")  # So per al Game Over
crash_sound = pygame.mixer.Sound("crash.wav")  # So per a col·lisions amb asteroides
shoot_sound = pygame.mixer.Sound("shoot.wav")  # So per als trets

# Carregar imatges
astronauta_img = pygame.image.load("astronauta.png")  # Imatge de l'astronauta
astronauta_img = pygame.transform.scale(astronauta_img, (100, 100))  # Escala la imatge de l'astronauta
asteroide_img = pygame.image.load("asteroide.png").convert_alpha()  # Imatge dels asteroides
energia_img = pygame.image.load("energia.png")  # Imatge dels power-ups (energia)
energia_img = pygame.transform.scale(energia_img, (60, 60))  # Escala la imatge dels power-ups
vida_icon = pygame.transform.scale(energia_img, (30, 30))  # Icona per a les vides

# ========================
# Variables Globals
# ========================
score = 0  # Puntuació del jugador
difficulty_level = 1  # Nivell de dificultat (afecta la velocitat dels asteroides)
lives = 3  # Vides del jugador
paused = False  # Estat de pausa del joc
running = True  # Controla si el joc està en execució
ADD_OBSTACLE = pygame.USEREVENT + 1  # Event per afegir asteroides
ADD_POWERUP = pygame.USEREVENT + 2  # Event per afegir power-ups

# ========================
# Funcions Auxiliars
# ========================

def draw_text(surface, text, font, color, x, y, center=False):
    """Dibuixa text a la pantalla."""
    text_obj = font.render(text, True, color)  # Renderitza el text
    text_rect = text_obj.get_rect()  # Obté el rectangle del text
    if center:
        text_rect.center = (x, y)  # Centra el text
    else:
        text_rect.topleft = (x, y)  # Alinea el text a l'esquerra
    surface.blit(text_obj, text_rect)  # Dibuixa el text a la pantalla

def draw_lives(surface, x, y, lives):
    """Dibuixa les icones de vida a la pantalla."""
    for i in range(lives):
        surface.blit(vida_icon, (x + i * 35, y))  # Dibuixa una icona per cada vida

# ========================
# Pantalla de pausa
# ========================
def show_pause_screen():
    """Mostra un missatge de pausa en pantalla."""
    screen.fill(DARK_PURPLE)  # Fons porpra fosc
    draw_text(screen, "PAUSA", big_font, NEON_BLUE, WIDTH // 2, HEIGHT // 2 - 50, center=True)  # Text de pausa
    draw_text(screen, "Prem P per continuar", font, WHITE, WIDTH // 2, HEIGHT // 2 + 20, center=True)  # Instrucció
    pygame.display.flip()  # Actualitza la pantalla

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
    draw_text(screen, " JOC DE L'ASTRONAUTA ", big_font, NEON_BLUE, WIDTH // 2, 100, center=True)  # Títol
    draw_text(screen, "OBJECTIU: Sobreviu i evita els asteroides!", font, CYAN_GLOW, WIDTH // 2, 180, center=True)  # Objectiu
    draw_text(screen, "CONTROLS:", font, ELECTRIC_PURPLE, WIDTH // 2, 250, center=True)  # Controls
    draw_text(screen, " FLETXES : Moure", font, LAVENDER, WIDTH // 2, 280, center=True)  # Moviment
    draw_text(screen, " ESPAI : Disparar", font, LAVENDER, WIDTH // 2, 310, center=True)  # Disparar
    draw_text(screen, " P : Pausa", font, LAVENDER, WIDTH // 2, 340, center=True)  # Pausa
    draw_text(screen, " Recull energia per guanyar vides!", font, SOFT_LILAC, WIDTH // 2, 380, center=True)  # Power-ups
    draw_text(screen, " PREM QUALSSEVOL TECLA PER COMENÇAR ", font, ELECTRIC_PURPLE, WIDTH // 2, 450, center=True)  # Instrucció
    pygame.display.flip()  # Actualitza la pantalla

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Comença el joc

# ========================
# Classes del Joc
# ========================

class Player(pygame.sprite.Sprite):
    """Classe que representa l'astronauta (jugador)."""
    def __init__(self):
        super().__init__()
        self.image = astronauta_img  # Imatge de l'astronauta
        self.rect = self.image.get_rect()  # Rectangle de la imatge
        self.rect.center = (100, HEIGHT // 2)  # Posició inicial
        self.speed = 5  # Velocitat de moviment

    def update(self):
        """Actualitza la posició de l'astronauta."""
        keys = pygame.key.get_pressed()  # Obté les tecles premudes
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed  # Mou cap amunt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed  # Mou cap avall
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  # Mou cap a l'esquerra
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed  # Mou cap a la dreta
        self.rect.clamp_ip(screen.get_rect())  # Limita el moviment dins de la pantalla

    def shoot(self):
        """Dispara un projectil."""
        shoot_sound.play()  # Reprodueix el so de disparar
        shot = Shot(self.rect.right, self.rect.centery)  # Crea un nou projectil
        all_sprites.add(shot)  # Afegeix el projectil al grup d'sprites
        shots.add(shot)  # Afegeix el projectil al grup de trets

class Obstacle(pygame.sprite.Sprite):
    """Classe que representa els asteroides."""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(asteroide_img, (random.randint(40, 80), random.randint(40, 80)))  # Escala l'asteroide
        self.rect = self.image.get_rect()  # Rectangle de la imatge
        self.rect.x = WIDTH + random.randint(10, 100)  # Posició inicial (fora de la pantalla)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Posició vertical aleatòria
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)  # Velocitat aleatòria

    def update(self):
        """Actualitza la posició de l'asteroide."""
        global score
        if not paused:
            self.rect.x -= self.speed  # Mou l'asteroide cap a l'esquerra
            if self.rect.right < 0:  # Si surt de la pantalla
                score += 1  # Incrementa la puntuació
                self.kill()  # Elimina l'asteroide

class PowerUp(pygame.sprite.Sprite):
    """Classe que representa els power-ups (energia)."""
    def __init__(self):
        super().__init__()
        self.image = energia_img  # Imatge del power-up
        self.rect = self.image.get_rect()  # Rectangle de la imatge
        self.rect.x = WIDTH + random.randint(10, 100)  # Posició inicial (fora de la pantalla)
        self.rect.y = random.randint(50, HEIGHT - 50)  # Posició vertical aleatòria
        self.speed = 4  # Velocitat del power-up

    def update(self):
        """Actualitza la posició del power-up."""
        if not paused:
            self.rect.x -= self.speed  # Mou el power-up cap a l'esquerra
            if self.rect.right < 0:  # Si surt de la pantalla
                self.kill()  # Elimina el power-up

class Shot(pygame.sprite.Sprite):
    """Classe que representa els projectils."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # Superfície del projectil
        self.image.fill(RED)  # Color del projectil
        self.rect = self.image.get_rect()  # Rectangle del projectil
        self.rect.center = (x, y)  # Posició inicial
        self.speed = 10  # Velocitat del projectil

    def update(self):
        """Actualitza la posició del projectil."""
        self.rect.x += self.speed  # Mou el projectil cap a la dreta
        if self.rect.left > WIDTH:  # Si surt de la pantalla
            self.kill()  # Elimina el projectil

# ========================
# Funció per reiniciar el Joc
# ========================
def new_game():
    """Reinicia el joc amb valors inicials."""
    global score, difficulty_level, lives, paused
    score = 0  # Reinicia la puntuació
    difficulty_level = 1  # Reinicia el nivell de dificultat
    lives = 3  # Reinicia les vides
    paused = False  # Desactiva la pausa
    pygame.time.set_timer(ADD_OBSTACLE, 1500)  # Configura l'event per afegir asteroides
    pygame.time.set_timer(ADD_POWERUP, 5000)  # Configura l'event per afegir power-ups
    global all_sprites, obstacles, powerups, player, shots
    all_sprites = pygame.sprite.Group()  # Grup que conté tots els sprites
    obstacles = pygame.sprite.Group()  # Grup per als asteroides
    powerups = pygame.sprite.Group()  # Grup per als power-ups
    shots = pygame.sprite.Group()  # Grup per als projectils
    player = Player()  # Crea un nou jugador
    all_sprites.add(player)  # Afegeix el jugador al grup d'sprites

# ========================
# Pantalla de Game Over
# ========================
def show_game_over(final_score):
    """Mostra una pantalla de Game Over millorada."""
    screen.fill(NEON_RED)  # Fons vermell neó
    draw_text(screen, "GAME OVER", big_font, WHITE, WIDTH // 2, 200, center=True)  # Text de Game Over
    draw_text(screen, f"Puntuació Final: {final_score}", font, WHITE, WIDTH // 2, 300, center=True)  # Puntuació final
    draw_text(screen, "Prem P per reiniciar", font, BLACK, WIDTH // 2, 350, center=True)  # Instrucció
    pygame.display.flip()  # Actualitza la pantalla

    pygame.mixer.music.stop()  # Atura la música de fons
    game_over_sound.play()  # Reprodueix el so de Game Over

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.mixer.music.play(-1)  # Reprèn la música de fons
                waiting = False  # Reinicia el joc

# ========================
# Bucle principal
# ========================
show_start_screen()  # Mostra la pantalla d'inici

while True:
    new_game()  # Reinicia el joc
    running = True
    while running:
        clock.tick(FPS)  # Controla la velocitat del joc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # Activa/desactiva la pausa
                    if paused:
                        pygame.mixer.music.pause()  # Pausa la música
                        show_pause_screen()  # Mostra la pantalla de pausa
                    else:
                        pygame.mixer.music.unpause()  # Reprèn la música
                elif event.key == pygame.K_SPACE and not paused:
                    player.shoot()  # Dispara un projectil
            elif event.type == ADD_OBSTACLE and not paused:
                obstacle = Obstacle()  # Crea un nou asteroide
                all_sprites.add(obstacle)  # Afegeix l'asteroide al grup d'sprites
                obstacles.add(obstacle)  # Afegeix l'asteroide al grup d'obstacles
            elif event.type == ADD_POWERUP and not paused:
                powerup = PowerUp()  # Crea un nou power-up
                all_sprites.add(powerup)  # Afegeix el power-up al grup d'sprites
                powerups.add(powerup)  # Afegeix el power-up al grup de power-ups

        if not paused:
            all_sprites.update()  # Actualitza tots els sprites

            # Verificar col·lisions amb obstacles (perdre vides)
            if pygame.sprite.spritecollide(player, obstacles, True):
                crash_sound.play()  # Reprodueix el so de col·lisió
                lives -= 1  # Redueix les vides
                if lives <= 0:
                    running = False  # Finalitza el joc

            # Verificar col·lisions amb power-ups (guanyar vides)
            for powerup in pygame.sprite.spritecollide(player, powerups, True):
                powerup_sound.play()  # Reprodueix el so de power-up
                lives += 1  # Incrementa les vides

            # Verificar col·lisions entre trets i obstacles (eliminar obstacles)
            pygame.sprite.groupcollide(obstacles, shots, True, True)

        screen.fill(SPACE_BLUE)  # Dibuixa el fons del joc
        all_sprites.draw(screen)  # Dibuixa tots els sprites
        draw_text(screen, f"Puntuació: {score}", font, CYAN_GLOW, 10, 10)  # Dibuixa la puntuació
        draw_lives(screen, 10, 40, lives)  # Dibuixa les vides
        pygame.display.flip()  # Actualitza la pantalla

    show_game_over(score)  # Mostra la pantalla de Game Over