#This module pack is made for beginners to pygame who want to create a first simple project
#Before using make sure to have pygame installed
#For an example of how to use look in the 'example.py' file (or look at a whole example game in 'game.py')
#This code was all self written by me so if you're going to publish a project using this modules pack I would be happy if you mention it
#credit : https://github.com/Amr-007-coder/Python-Pygame-modules-for-Beginners

import pygame, random, math

pygame.init()

#show text message on the screen
def displayText(display: pygame.display, msg: str, pos: tuple, textColor: pygame.Color, font: pygame.font, show_msg: bool):

    obj = font.render(msg, show_msg, textColor)
    rect = obj.get_rect(center=pos)
    display.blit(obj, rect)

#show a coloured button on the screen and take actions if clicked/activated
buttonTimer = 0
def displayButton(display: pygame.display, msg_action: dir, current_msg: str, pos: tuple, size: tuple, buttonColor: pygame.Color,
                  active_buttonColor: pygame.Color, textColor: pygame.Color, font: pygame.font, show_buttonText: bool):
    global buttonTimer
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(pos[0] - size[0]/2, pos[1] - size[1]/2, size[0], size[1])
    pygame.draw.rect(display, buttonColor, (rect))

    if rect.collidepoint(mouse):
        pygame.draw.rect(display, active_buttonColor, (rect))

        if click[0]:
            buttonTimer += 1
            #check for messages and take action
            for msg in msg_action:
                if current_msg == msg and buttonTimer == 1:
                    msg_action[msg] = not msg_action[msg]
        
        else:
            buttonTimer = 0

    displayText(display, current_msg, pos, textColor, font, show_buttonText)

#show a image button (with image as fill) on the screen and take actions if clicked/activated
imagebuttonTimer = 0
def displayImageButton(display: pygame.display, msg_action: dir, current_msg: str, pos: tuple, size: tuple, buttonImage: pygame.image,
                  active_buttonImage: pygame.image, textColor: pygame.Color, font: pygame.font, show_buttonText: bool):
    global imagebuttonTimer

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    img = pygame.transform.scale(buttonImage, size)
    rect = pygame.Rect(pos[0] - img.get_width()/2, pos[1] - img.get_height()/2, img.get_width(), img.get_height())

    if rect.collidepoint(mouse):
        img = pygame.transform.scale(active_buttonImage, size)
        if click[0]:
            imagebuttonTimer += 1
            #check for messages and take action
            for msg in msg_action:
                if current_msg == msg and imagebuttonTimer == 1: #so button dosn't get pressed more than once
                    msg_action[msg] = not msg_action[msg]

        else:
            imagebuttonTimer = 0

    display.blit(img, rect)
    displayText(display, current_msg, pos, textColor, font, show_buttonText)

#get random position within a given area
def getRandomPosition(area: pygame.Rect):
    x = random.randint(area.left, area.right)
    y = random.randint(area.top, area.bottom)
    return x, y


#return value of an expression (not very neccessary funtcion but could help beginners)
def returnValue(expression):
    if expression:
        return True
    else:
        return False

#get single frames out of images
def get_image(sheet: pygame.image, frame: int, width: int, height: int, colour: pygame.Color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image.set_colorkey(colour)

    return image

#fade an image in or out
def fade(display: pygame.display, surface: pygame.image, alpha: int):
    fade_surface = surface.copy()
    fade_surface.set_alpha(alpha)
    display.blit(fade_surface, fade_surface.get_rect())
    
#draw a progress bar on the screen
def displayProgressBar(display: pygame.display, pos: tuple, size: tuple, progress: float, barColor: pygame.Color, borderColor: pygame.Color):
    inner_width = size[0] * min(max(progress, 0), 1)  # Progress is a value between 0 and 1
    pygame.draw.rect(display, barColor, (pos[0], pos[1], inner_width, size[1]))
    pygame.draw.rect(display, borderColor, (*pos, size[0], size[1]), 5)


#display FPS on the screen
def displayFPS(display: pygame.display, clock: pygame.time.Clock, pos: tuple, font: pygame.font, color: pygame.Color):
    fps = str(int(clock.get_fps()))
    fps_text = font.render("FPS: " + fps, True, color)
    display.blit(fps_text, pos)

#adjust camera position for scrolling levels
def cameraScroll(target_pos: tuple, screen_size: tuple, level_size: tuple):
    x = min(0, max(screen_size[0] - level_size[0], screen_size[0] // 2 - target_pos[0]))
    y = min(0, max(screen_size[1] - level_size[1], screen_size[1] // 2 - target_pos[1]))
    return x, y




#check if mouse is over a circular area
def isMouseOverCircle(center: tuple, radius: int):
    mouse = pygame.mouse.get_pos()
    distance = ((mouse[0] - center[0]) ** 2 + (mouse[1] - center[1]) ** 2) ** 0.5
    return distance <= radius

#draw circular button with collision check
def displayCircularButton(display: pygame.display, msg: str, center: tuple, radius: int, buttonColor: pygame.Color, active_buttonColor: pygame.Color, textColor: pygame.Color, font: pygame.font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = active_buttonColor if isMouseOverCircle(center, radius) else buttonColor
    pygame.draw.circle(display, color, center, radius)
    if isMouseOverCircle(center, radius) and click[0]:
        return True  # Button was clicked
    displayText(display, msg, center, textColor, font, True)
    return False

#create particles for effects
def createParticles(particles: list, position: tuple, color: pygame.Color, amount: int, speed: float):
    for _ in range(amount):
        angle = random.uniform(0, 2 * math.pi)
        velocity = (speed * math.cos(angle), speed * math.sin(angle))
        particles.append({'pos': list(position), 'vel': velocity, 'color': color, 'lifetime': 100})

#draw a health bar on the screen
def drawHealthBar(display: pygame.display, pos: tuple, size: tuple, health: int, max_health: int, bar_color: pygame.Color, border_color: pygame.Color):
    pygame.draw.rect(display, border_color, (*pos, *size), 2)
    inner_width = size[0] * max(0, health) // max_health
    pygame.draw.rect(display, bar_color, (pos[0], pos[1], inner_width, size[1]))

#handle text input from user
def handleTextInput(events, current_text: str, max_length: int = 10):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            elif event.key == pygame.K_RETURN:
                return current_text, True  # Return text and an "enter" signal
            elif len(current_text) < max_length:
                current_text += event.unicode
    return current_text, False

#simple countdown timer
def countdownTimer(start_time: int, duration: int):
    elapsed_time = pygame.time.get_ticks() - start_time
    return max(0, duration - elapsed_time // 1000)

#smoothly move a character to a target position
def smoothMove(current_pos: tuple, target_pos: tuple, speed: float):
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]
    distance = math.hypot(dx, dy)
    if distance > speed:
        return [current_pos[0] + dx / distance * speed, current_pos[1] + dy / distance * speed]  # Liste statt Tupel zurückgeben
    return list(target_pos)  # Auch hier eine Liste zurückgeben


#set a frame rate limiter
def limitFPS(clock: pygame.time.Clock, target_fps: int):
    clock.tick(target_fps)
