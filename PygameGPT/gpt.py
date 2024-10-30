import pygame
from modules import *  # Importiere alle Funktionen aus modules.py
import random

# Initialisiere Pygame
pygame.init()

# Fenstergröße und Anzeige erstellen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Demo mit Modulen")

# Farben und Schriftarten
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
GRAY = pygame.Color(200, 200, 200)
BLUE = pygame.Color(0, 0, 255)
font = pygame.font.SysFont(None, 36)

# Spielfiguren und Variablen
clock = pygame.time.Clock()
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
player_health = 100
player_max_health = 100
particles = []
running = True

# Button- und Timer-Variablen
button_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
button_clicked = False
start_time = pygame.time.get_ticks()
fade_alpha = 0

# Hauptspiel-Schleife
while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    
    # Event-Handling
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    # Bewegung der Spielfigur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Spieler Kollision mit Bildschirmrand
    player_pos[0] = max(0, min(SCREEN_WIDTH, player_pos[0]))
    player_pos[1] = max(0, min(SCREEN_HEIGHT, player_pos[1]))

    # Button anzeigen und klicken überprüfen
    button_clicked = displayCircularButton(screen, "Klick mich", button_pos, 40, GRAY, BLUE, BLACK, font)
    if button_clicked:
        createParticles(particles, player_pos, RED, 15, 5)  # Erzeuge Partikel beim Klick

    # Partikel-Update und Anzeige
    for particle in particles[:]:
        particle['pos'][0] += particle['vel'][0]
        particle['pos'][1] += particle['vel'][1]
        particle['lifetime'] -= 1
        pygame.draw.circle(screen, particle['color'], (int(particle['pos'][0]), int(particle['pos'][1])), 3)
        if particle['lifetime'] <= 0:
            particles.remove(particle)

    # Gesundheitsanzeige des Spielers
    drawHealthBar(screen, (10, 10), (200, 20), player_health, player_max_health, GREEN, BLACK)
    
    # FPS-Anzeige
    displayFPS(screen, clock, (SCREEN_WIDTH - 60, 10), font, BLACK)

    # Text eingeben (drücke "T" um Text-Modus zu aktivieren)
    if keys[pygame.K_t]:
        text, enter_pressed = handleTextInput(events, "", 10)
        displayText(screen, f"Eingabe: {text}", (SCREEN_WIDTH // 2, 100), BLACK, font, True)

    # Timer für Countdown
    time_remaining = countdownTimer(start_time, 10)  # 10 Sekunden Countdown
    displayText(screen, f"Zeit: {time_remaining}", (SCREEN_WIDTH // 2, 150), BLACK, font, True)
    if time_remaining <= 0:
        displayText(screen, "Zeit ist abgelaufen!", (SCREEN_WIDTH // 2, 200), RED, font, True)

    # Glättungsbewegung (Beispiel für glatte Zielbewegung)
    target_pos = pygame.mouse.get_pos()
    player_pos = smoothMove(player_pos, target_pos, 0.1)

    # Aktualisiere Anzeige und begrenze FPS
    pygame.display.flip()
    limitFPS(clock, 60)

pygame.quit()
