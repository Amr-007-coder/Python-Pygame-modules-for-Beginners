#This code uses classes, complex logic and collisions (complex for beginners)
#still I tried to write the code easier. Thats why it is very long
#If it is too hard to understand check out the 'example.py' file


import pygame, random
from modules import *

pygame.init()

#import images/sounds
bg = pygame.image.load("images/bg.jpg")
corner = pygame.image.load("images/corner.png")
game_sound = pygame.mixer.Sound("sounds/game.wav")
walk_sound = pygame.mixer.Sound("sounds/walk.wav")
jump_sound = pygame.mixer.Sound("sounds/jump.wav")
attack_sound = pygame.mixer.Sound("sounds/attack.wav")
lose_sound = pygame.mixer.Sound("sounds/lose.wav") #first create lose screen then add sound

#set screen
width = bg.get_width()
height = bg.get_height()
screen = pygame.display.set_mode((width, height))

#set fps
fps = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont("Comic Sans MS", 40)
bigfont = pygame.font.SysFont("Comic Sans MS", 60)

button_actions = {
    "Start": True,
    "Quit": False,
}

def menu():
    displayText(screen, "Welcome", (screen.get_width()//2, 50), "black", font, True) #or to set the, True text in the center of the screen
    displayButton(screen, button_actions, "Start", (screen.get_width()//2, 150), (200, 100), (0, 240, 0), (0, 150, 0), ("black"), font, True) #rgb colour
    displayButton(screen, button_actions, "Quit", (screen.get_width()//2, 300), (200, 100), (150, 150, 150), (100, 100, 100), ("black"), font, True)

class Player:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = 4
        self.rect = pygame.Rect(self.x+45, self.y+40, self.width-100, self.height-50)
        self.fheart = pygame.image.load("images/voll.png")
        self.hheart = pygame.image.load("images/halb.png")
        self.run_sheet = pygame.image.load("images/player/run.png")
        self.idle_sheet = pygame.image.load("images/player/idle.png")
        self.die_sheet = pygame.image.load("images/player/die.png")
        self.attack_sheet = pygame.image.load("images/player/_Attack.png")
        self.jump_sheet = pygame.image.load("images/player/jump.png")
        self.crouch_idle = pygame.image.load("images/player/_Crouch.png")
        self.crouch_sheet = pygame.image.load("images/player/_CrouchWalk.png")
        self.run_frame = [get_image(self.run_sheet, n, self.width, self.height, ("black")) for n in range(0, 11)]
        self.idle_frame = [get_image(self.idle_sheet, n, self.width, self.height, ("black")) for n in range(0, 11)]
        self.die_frame = [get_image(self.die_sheet, n, self.width, self.height, ("black")) for n in range(0, 11)]
        self.attack_frame = [get_image(self.attack_sheet, n, self.width, self.height, ("black")) for n in range(0, 5)]
        self.jump_frame = [get_image(self.jump_sheet, n, self.width, self.height, ("black")) for n in range(0, 3)]
        self.crouch_frame = [get_image(self.crouch_sheet, n, self.width, self.height, ("black")) for n in range(0, 9)]
        self.standing = 0
        self.rightsteps = 0
        self.leftsteps = 0
        self.attack_time = 0
        self.reset_timer = 252
        self.die_time = 0
        self.gravity = -16
        self.direction = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[idle, crouch, crouch-walk-left, crouch-walk-left, left, right, jump-left, jump-right, fall-left, fall-right, attack, die]
        self.heart_pos = [(screen.get_width()/2 - 60, 15), (screen.get_width()/2, 15), (screen.get_width()/2 + 60, 15)]
        self.life = 6
        self.score = 0
        self.attacking = False
        self.resetting = False
        self.jumping = False
        self.crouched = False
        #for lose screen
        self.scorex = 80
        self.scorey = 30
        self.trans = 0
        self.corner_pos = [[-corner.get_width(), -corner.get_height()], [screen.get_width(), -corner.get_height()],
                           [-corner.get_width(), screen.get_height()], [screen.get_width(), screen.get_height()]]

    def move_player(self):
        pressed = pygame.key.get_pressed()

        self.speed = 4
        if pressed[pygame.K_DOWN] and not self.jumping:
            self.crouched = True
        if pressed[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            self.direction = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
            self.leftsteps += 1
            self.standing = 0
            if pressed[pygame.K_w] and self.gravity == -16:
                pygame.mixer.Sound.play(jump_sound)
                self.gravity = 15
            if not pressed[pygame.K_w] and self.gravity == -16:
                self.jumping = False
        
            if self.gravity >= -15:
                self.jumping = True
                n = 1
                if self.gravity < 0:
                    self.direction = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
                    n = -1
                else:
                    self.direction = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
                self.y -= (self.gravity**2)*0.091*n
                self.gravity -= 1

        elif pressed[pygame.K_d] and self.x < 510:
            self.x += self.speed
            self.rightsteps += 1
            self.direction = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            if pressed[pygame.K_w] and self.gravity == -16:
                pygame.mixer.Sound.play(jump_sound)
                self.gravity = 15
            if not pressed[pygame.K_w] and self.gravity == -16:
                self.jumping = False
        
            if self.gravity >= -15:
                self.jumping = True
                n = 1
                if self.gravity < 0:
                    self.direction = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
                    n = -1
                else:
                    self.direction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                self.y -= (self.gravity**2)*0.091*n
                self.gravity -= 1


        else:
            self.standing += 1
            self.direction = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            if pressed[pygame.K_w] and self.gravity == -16:
                pygame.mixer.Sound.play(jump_sound)
                self.gravity = 15
            if not pressed[pygame.K_w] and self.gravity == -16:
                self.jumping = False
        
            if self.gravity >= -15:
                self.jumping = True
                n = 1
                if self.gravity < 0:
                    self.direction = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
                    n = -1
                else:
                    self.direction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
                self.y -= (self.gravity**2)*0.091*n
                self.gravity -= 1

        if (self.rightsteps == 20 or self.rightsteps == 44 or self.leftsteps == 20 or self.leftsteps == 44) and not self.jumping:
            pygame.mixer.Sound.play(walk_sound)

        #reset steps at 50
        self.leftsteps %= 50
        self.rightsteps %= 50
        self.standing %= 50

        self.rect = pygame.Rect(self.x+45, self.y, self.width-100, self.height)
    
    def crouch(self):
        pressed = pygame.key.get_pressed()
        self.direction = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rect = pygame.Rect(self.x+45, self.y+55, self.width-100, self.height-50)
        self.speed = 2
        if pressed[pygame.K_UP]:
            self.crouched = False
        if pressed[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            self.direction = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.leftsteps += 1
        if pressed[pygame.K_d] and self.x < 510:
            self.x += self.speed
            self.direction = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            self.rightsteps += 1

        self.rightsteps %= 40
        self.leftsteps %= 40

    def attack(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_f] or pressed[pygame.K_RIGHT]: #two options to attack
            self.attacking = True

        if self.attacking:
            self.direction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
            self.attack_time += 1
            if self.attack_time == 1:
                pygame.mixer.Sound.play(attack_sound)
            if self.attack_time == 20:
                self.attacking = False
                self.attack_time = 0

        if self.rect.colliderect(chest.rect) and self.attacking:
            chest.hide()
            self.resetting = True
            self.life += 1

        if self.resetting:
            self.reset_timer -= 1
            if self.reset_timer <= 0:
                self.resetting = False
                self.reset_timer = 252
                chest.reset()

    def draw_lifes(self):
        if self.life == 6:
            [screen.blit(self.fheart, (self.heart_pos[n])) for n in range(0, 3)]
        elif self.life == 5:
            screen.blit(self.hheart, self.heart_pos[2])
            [screen.blit(self.fheart, (self.heart_pos[n])) for n in range(0, 2)]
        elif self.life == 4:
            [screen.blit(self.fheart, (self.heart_pos[n])) for n in range(0, 2)]
        elif self.life == 3:
            screen.blit(self.hheart, self.heart_pos[1])
            [screen.blit(self.fheart, (self.heart_pos[n])) for n in range(0, 1)]
        elif self.life == 2:
            screen.blit(self.fheart, (self.heart_pos[0]))
        elif self.life == 1:
            screen.blit(self.hheart, self.heart_pos[0])
        else:
            [screen.blit(self.fheart, (self.heart_pos[n])) for n in range(0, 3)]
            displayText(screen, "+", (self.heart_pos[2][0]+73, self.heart_pos[2][1]+16), ("red"), bigfont, True)

    def lose(self):
        blur_surface = pygame.Surface(screen.get_size())
        blur_surface.set_alpha(self.trans)
        blur_surface.fill((164, 87, 41))
        blur_surface = pygame.transform.scale(blur_surface, (screen.get_width()//10, screen.get_height()//10))
        blur_surface = pygame.transform.scale(blur_surface, (screen.get_width(), screen.get_height()))
        screen.blit(blur_surface, (0, 0))

        if self.life > 0:
            pass
        else:
            self.scorex = screen.get_width()/2
            displayText(screen, "Game Over", (screen.get_width()//2, self.scorey/4), ("red"), font, True)
            if self.trans < 200:
                self.trans += 5
            if self.corner_pos[0][0] < 20:
                self.corner_pos[0][0] +=3
                self.corner_pos[0][1] +=3
                self.corner_pos[1][0] -=3
                self.corner_pos[1][1] +=3
                self.corner_pos[2][0] +=3
                self.corner_pos[2][1] -=3
                self.corner_pos[3][0] -=3
                self.corner_pos[3][1] -=3
                self.scorey += 3
            if self.corner_pos[0][0] == 0:
                pygame.mixer.Sound.play(lose_sound)

        screen.blit(corner, (self.corner_pos[0][0], self.corner_pos[0][1]))
        screen.blit(pygame.transform.flip(corner, True, False), (self.corner_pos[1][0], self.corner_pos[1][1]))
        screen.blit(pygame.transform.flip(corner, False, True), (self.corner_pos[2][0], self.corner_pos[2][1]))
        screen.blit(pygame.transform.flip(corner, True, True), (self.corner_pos[3][0], self.corner_pos[3][1]))

    def draw(self):
        #text("Life: " + str(self.life), 80, 30, ("black"), font)
        chest.spawn()
        if self.direction[0]:
            screen.blit(self.idle_frame[self.standing//5], (self.x, self.y))
        if self.direction[1]:
            screen.blit(self.crouch_idle, (self.x, self.y))
        if self.direction[2]:
            screen.blit(pygame.transform.flip(self.crouch_frame[self.leftsteps//5], True, False).convert_alpha(), (self.x, self.y))
        if self.direction[3]:
            screen.blit(self.crouch_frame[self.rightsteps//5], (self.x, self.y))
        if self.direction[4]:
            screen.blit(pygame.transform.flip(self.run_frame[self.leftsteps//5], True, False).convert_alpha(), (self.x, self.y)) #50:5 = 10 (num of frames)
        if self.direction[5]:
            screen.blit(self.run_frame[self.rightsteps//5], (self.x, self.y))
        if self.direction[6]:
            screen.blit(pygame.transform.flip(self.jump_frame[0], True, False).convert_alpha(), (self.x, self.y))
        if self.direction[7]:
            screen.blit(self.jump_frame[0], (self.x, self.y))
        if self.direction[8]:
            screen.blit(pygame.transform.flip(self.jump_frame[1], True, False).convert_alpha(), (self.x, self.y))
        if self.direction[9]:
            screen.blit(self.jump_frame[1], (self.x, self.y))
        if self.direction[10]:
            screen.blit(self.attack_frame[self.attack_time//5], (self.x, self.y))
        if self.direction[11]:
            screen.blit(self.die_frame[self.die_time//5], (self.x, self.y))
        
        if self.life <= 0 and self.die_time < 40:
            self.die_time += 1

        if self.life > 0:
            self.draw_lifes()
            if not self.crouched:
                self.move_player()
                self.attack()
            else:
                self.crouch()
        else:
            self.lose()
            self.direction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

        displayText(screen, "Score: " + str(self.score), (self.scorex, self.scorey), ("black"), font, True)


class Enemy:
    def __init__(self):
        self.size = 128
        self.x = screen.get_width() + 100 #so the enemy will come towards us
        self.y = 238
        self.speed = 5
        self.steps = 0
        self.rect = pygame.Rect(self.x+40, self.y+40, self.size-105, self.size-100) #using pygame.Rect cuz we´ll check if player and enemy collide
        self.run_sheet = pygame.image.load("images/enemy/run.png")
        self.run_frame = [get_image(self.run_sheet, n, self.size, self.size, ("black")) for n in range(0, 9)]
        self.enemy_num = 1

    def respawn(self):
        self.x = screen.get_width() + 100
        self.enemy_num = random.randint(1, 2)

    def movement(self):
        if self.x > 0 - self.size: #so if the enemy has not completed the 'run' till left side of screen
            self.x -= self.speed
            self.steps += 1
        
        if self.x <= 0 - self.size: #if reached left end of screen
            self.speed += 0.3
            player.score += 1
            self.respawn()

        if player.rect.colliderect(self.rect):
            self.respawn()
            player.life -= 1

        self.steps %= 48
        self.rect = pygame.Rect(self.x+40, self.y+40, self.size-105, self.size-100)


    def draw(self):
        screen.blit(pygame.transform.scale(pygame.transform.flip(self.run_frame[self.steps//6], True, False).convert_alpha(), (80, 80)), (self.x, self.y))
        if player.life > 0:
            self.movement()


class Enemy2:
    def __init__(self):
        self.size = 16
        self.changed_size = 30
        self.x = screen.get_width() + 100
        self.y = 260
        self.speed = 5
        self.steps = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.run_sheet = pygame.image.load("images/enemy/bird.png")
        self.run_frame = [get_image(self.run_sheet, n, self.size, self.size, ("black")) for n in range(0, 9)]


    def respawn(self):
        self.x = screen.get_width() + 100
        enemy.enemy_num = random.randint(1, 2)

    def movement(self):
        if self.x > 0 - self.size: #so if the enemy has not completed the 'run' till left side of screen
            self.x -= self.speed
            self.steps += 1
        
        if self.x <= 0 - self.size: #if reached left end of screen
            self.speed += 0.3
            player.score += 1
            self.respawn()

        if player.rect.colliderect(self.rect):
            self.respawn()
            player.life -= 1

        self.steps %= 48
        self.rect = pygame.Rect(self.x+5, self.y+5, self.size+10, self.size)

    def draw(self):
        screen.blit(pygame.transform.scale(self.run_frame[self.steps//6], (self.changed_size, self.changed_size)).convert_alpha(), (self.x, self.y))
        if player.life > 0:
            self.movement()


class Chest:
    def __init__(self):
        self.size = (55, 55)
        self.img = pygame.transform.scale(pygame.image.load("images/chest.png"), self.size)
        self.pos = (random.randint(20, 400), 275) #so chest/box spawms at random pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def reset(self):
        self.pos = (random.randint(20, 400), 275)
        self.rect = pygame.Rect(0, 0, 0, 0) #so the box rect doesnt 'exist' during cool down

    def hide(self):
        self.pos = (-1000, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)

    def spawn(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        screen.blit(self.img, (self.pos))

player = Player(200, 238, 120, 80)
enemy = Enemy()
enemy2 = Enemy2()
chest = Chest()

pygame.mixer.Sound.play(game_sound, 5)

while not button_actions["Quit"]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            button_actions["Quit"] = True

    screen.blit(bg, (0, 0))
    if button_actions["Start"]:
        menu()
    else:
        displayText(screen, "Score: " + str(player.score), (80, 30), ("black"), font, True)
        player.draw()
        if enemy.enemy_num == 1:
            enemy.draw()
        else:
            enemy2.draw()
    pygame.display.update()
    clock.tick(fps)

#- add sounds