import pygame
import random
import os

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de la Nave")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imágenes
ship_img = pygame.image.load('img/ship.png').convert_alpha()
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
meteor_small_img = pygame.image.load('img/meteor_small.png').convert_alpha()
meteor_medium_img = pygame.image.load('img/meteor_medium.png').convert_alpha()
meteor_large_img = pygame.image.load('img/meteor_large.png').convert_alpha()

# Cargar música y efectos de sonido (sacar # cuando tenga el archivo)
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.set_volume(0.5)
#shoot_sound = pygame.mixer.Sound('shoot.wav')  # Sonido para disparos
#explosion_sound = pygame.mixer.Sound('explosion.wav')  # Sonido para explosiones

# Clase para la nave
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ship_img, (50, 40))  # Imagen de la nave
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.life = 100
        self.points = 0
        self.last_shot = pygame.time.get_ticks()  # Para controlar el tiempo entre disparos
        self.shoot_delay = 250  # Retardo entre disparos (milisegundos)

    def move(self, dx):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:  # Controla la frecuencia de disparos
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)  # Agregar la bala al grupo all_sprites para que se dibuje
            #shoot_sound.play()  # Reproducir el sonido de disparo

# Clase para las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (10, 20))  # Imagen de la bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Clase para los meteoritos
class Meteor(pygame.sprite.Sprite):
    def __init__(self, meteor_type):
        super().__init__()
        if meteor_type == "small":
            self.image = pygame.transform.scale(meteor_small_img, (30, 30))  # Meteorito pequeño
            self.health = 1
            self.damage = 5
            self.points = 1
        elif meteor_type == "medium":
            self.image = pygame.transform.scale(meteor_medium_img, (50, 50))  # Meteorito mediano
            self.health = 3
            self.damage = 25
            self.points = 10
        elif meteor_type == "large":
            self.image = pygame.transform.scale(meteor_large_img, (70, 70))  # Meteorito grande
            self.health = 4
            self.damage = 50
            self.points = 25

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Función para mostrar el menú principal
def show_menu():
    font = pygame.font.SysFont(None, 55)
    screen.fill(BLACK)

    title_text = font.render("Juego de la Nave", True, WHITE)
    start_text = font.render("Iniciar partida", True, WHITE)
    score_text = font.render("Ver puntuaciones", True, WHITE)
    music_text = font.render("Activar/Desactivar música", True, WHITE)
    quit_text = font.render("Salir del juego", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    start_rect = screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 200))
    score_rect = screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))
    music_rect = screen.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, 400))
    quit_rect = screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 500))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verificar si se hizo clic con el botón izquierdo
                    if start_rect.collidepoint(event.pos):
                        return 'start'
                    elif score_rect.collidepoint(event.pos):
                        return 'scores'
                    elif music_rect.collidepoint(event.pos):
                        return 'toggle_music'
                    elif quit_rect.collidepoint(event.pos):
                        return 'quit'

# Función para leer puntuaciones anteriores
def show_scores():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 40)
    
    try:
        with open('highscores.txt', 'r') as f:
            scores = f.readlines()
    except FileNotFoundError:
        scores = []

    title_text = font.render("Puntuaciones Anteriores", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    for i, score in enumerate(scores):
        score_text = font.render(f"{i+1}. {score.strip()}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 200 + i * 40))
        

    pygame.display.flip()
    pygame.time.wait(2000)  # Espera para que el jugador pueda leer


# Función principal del juego
def game():
    clock = pygame.time.Clock()
    ship = Ship()
    
    # Inicializar grupos de sprites
    global all_sprites, bullets, meteors
    all_sprites = pygame.sprite.Group()  # Grupo que contiene todos los sprites
    bullets = pygame.sprite.Group()  # Grupo para las balas
    meteors = pygame.sprite.Group()  # Grupo para los meteoritos

    all_sprites.add(ship)
    
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento de la nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.move(-1)
        if keys[pygame.K_RIGHT]:
            ship.move(1)
        if keys[pygame.K_SPACE]:  # Revisar si se presiona la tecla de espacio
            ship.shoot()

        # Crear meteoritos aleatorios
        if random.random() < 0.02:  # Probabilidad de aparición
            meteor_type = random.choice(["small", "medium", "large"])
            meteor = Meteor(meteor_type)
            meteors.add(meteor)
            all_sprites.add(meteor)

        # Actualizar sprites
        all_sprites.update()

        # Colisiones entre balas y meteoritos
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, meteors, False)
            for hit in hits:
                hit.health -= 1
                if hit.health <= 0:
                    ship.points += hit.points
                    hit.kill()
                    #explosion_sound.play()  # Reproducir sonido de explosión
                bullet.kill()

        # Colisiones entre nave y meteoritos
        hits = pygame.sprite.spritecollide(ship, meteors, True)
        for hit in hits:
            ship.life -= hit.damage
            if ship.life <= 0:
                main_menu()  # Termina el juego

        # Dibujar todo
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Mostrar puntuación y vida
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Puntos: {ship.points}", True, WHITE)
        life_text = font.render(f"Vida: {ship.life}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (10, 50))

        pygame.display.flip()

    # Guardar puntuación al terminar el juego
    with open('highscores.txt', 'a') as f:
        f.write(f"{ship.points}\n")

# Alternar la música
def toggle_music(is_music_on):
    if is_music_on:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play(-1)  # Repetir la música indefinidamente
    return not is_music_on

# Lógica del menú principal
def main_menu():
    is_music_on = False
    while True:
        choice = show_menu()
        if choice == 'start':
            game()
        elif choice == 'scores':
            show_scores()
        elif choice == 'toggle_music':
            is_music_on = toggle_music(is_music_on)
        elif choice == 'quit':
            pygame.quit()
            quit()

# Ejecutar el menú principal
main_menu()
