import pygame
import schedule
from time import sleep
# pygame.init()

from random import randint


class gameState():
    def __init__(self):
        if True:
            self.agility = 1
            while self.agility > 10 or self.agility < 2:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Controls: arrow keys to move, space to shoot")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("What would you like your agility to be? The higher the number, the faster you move BUT you have smaller projectiles. 5 is normal speed.")
                self.agility = int(input("Enter a number between 2 and 10: "))
        else:
            self.agility = 5
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.windowX = 1000
        self.windowY = 700
        self.game = pygame.display.set_mode([self.windowX, self.windowY])
        self.verticalControls = True
        self.should_run = True
        # agility - more = faster moving but smaller projectiles. default = 5, max = 10, min = 2
        self.playerSpeed = self.agility * 2
        self.spawnDelay = 3
        self.alienType = "normal"
        self.died = False
        self.spawnIndex = 0
        # types: normal, ball
        self.theme = "normal"
        # themes: normal, contrast, light

        self.p1 = None
        self.balls = []
        self.gameElements = []

# gs = gameState()


class player():
    def __init__(self):
        self.hitbox = pygame.Rect(
            (gs.windowX/5, gs.windowY/1.2, gs.windowX/10, gs.windowY/10))
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.score = 0000

    def update(self, gs):
        x, y = self.hitbox.center
        if self.left_pressed:
            if x > 0:
                self.hitbox.move_ip(0 - gs.playerSpeed, 0)
        if self.right_pressed:
            if x < gs.windowX:
                self.hitbox.move_ip(gs.playerSpeed, 0)
        if self.up_pressed:
            if y > 0:
                self.hitbox.move_ip(0, 0 - gs.playerSpeed)
        if self.down_pressed:
            if y < gs.windowY:
                self.hitbox.move_ip(0, gs.playerSpeed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gs.should_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
            if gs.verticalControls:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.up_pressed = True
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.up_pressed = False
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = self.hitbox.center
                    proj = projectile(x, y)
                    gs.gameElements.append(proj)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for ball in gs.balls:
            if (ball.detectCollision(self.hitbox)):
                gs.died = True
                #gs.should_run = False

    def draw(self, gs):
        if gs.theme == "normal":
            pygame.draw.rect(gs.game, (113, 110, 155), self.hitbox)
        if gs.theme == "contrast":
            pygame.draw.rect(gs.game, (255, 255, 255), self.hitbox)
        if gs.theme == "light":
            pygame.draw.rect(gs.game, (113, 110, 155), self.hitbox)


gs = gameState()
gs.p1 = player()
gs.gameElements = [gs.p1]

# gs.p1 = player()

# gs.gameElements.append(player())


class ball():
    def setColor(self):
        if gs.theme == "normal":
            self.colorValue = self.maxHP * 5 + self.hp * 20
            self.color = (50, self.colorValue, 50)
        if gs.theme == "contrast":
            self.colorValue = self.maxHP * 5 + self.hp * 20
            self.color = (200, self.colorValue, 200)
        if gs.theme == "light":
            self.colorValue = self.maxHP * 5 + self.hp * 20
            self.color = (5, self.colorValue, 5)

    def detectCollision(self, rectangle):
        return rectangle.colliderect(self.hitbox)

    def __init__(self, color, size):
        self.maxHP = size
        self.hp = size
        self.size = size * 10 + 5
        # self.color = color
        self.x = 250
        self.y = 250
        self.xSpeed = randint(1, 10)
        self.ySpeed = randint(1, 10)
        self.xMove = self.xSpeed
        self.yMove = self.ySpeed
        self.colorValue = self.hp / self.maxHP * 20
        # self.colorValue = self.maxHP * 5 + self.hp * 20
        self.setColor()
        self.hitbox = pygame.Rect(
            self.x-(self.size/2), self.y-(self.size/2), self.size, self.size)

    def hit(self, projectile):
        self.hp = self.hp - 1
        gs.p1.score = gs.p1.score + 10 - self.size / 10
        self.setColor()
        if (self.hp < 0.01):
            if self in gs.gameElements:
                gs.gameElements.remove(self)
            if self in gs.balls:
                gs.balls.remove(self)
            gs.p1.score = gs.p1.score + 10 * self.size
        gs.p1.score = round(gs.p1.score)
        if projectile in gs.gameElements:
            gs.gameElements.remove(projectile)

    def update(self):
        if (self.x > gs.windowX - self.size):
            self.xMove = 0 - self.xSpeed
        if (self.x < 0 + self.size):
            self.xMove = self.xSpeed
        if (self.y > gs.windowY - self.size):
            self.yMove = 0 - self.ySpeed
        if (self.y < 0 + self.size):
            self.yMove = self.ySpeed
        self.x = self.x + self.xMove
        self.y = self.y + self.yMove
        self.hitbox = pygame.Rect(
            self.x-self.size, self.y-self.size, self.size*2, self.size*2)

    def draw(self, gs):
        pygame.draw.circle(gs.game, (self.color), (self.x, self.y), self.size)


class alien():
    def setColor(self):
        match gs.theme:
            case "normal":
                self.colorValue = self.maxHP * 5 + self.hp * 20
                self.color = (50, self.colorValue, 50)
            case "contrast":
                self.colorValue = self.maxHP * 5 + self.hp * 20
                self.color = (200, self.colorValue, 200)
            case "light":
                self.colorValue = self.maxHP * 5 + self.hp * 20
                self.color = (5, self.colorValue, 5)

    def detectCollision(self, rectangle):
        return rectangle.colliderect(self.hitbox)

    def __init__(self, color, size):
        self.difficulty = 10.5
        self.maxHP = size
        self.hp = size
        self.size = size * self.difficulty + 5
        # self.color = color
        self.x = 250
        self.y = 250
        self.xSpeed = 10.5 - size
        self.ySpeed = 0
        self.xMove = self.xSpeed
        self.yMove = self.ySpeed
        self.colorValue = self.hp / self.maxHP * 20
        # self.colorValue = self.maxHP * 5 + self.hp * 20
        self.setColor()
        self.hitbox = pygame.Rect(
            self.x-(self.size/2), self.y-(self.size/2), self.size, self.size)

    def hit(self, projectile):
        self.hp = self.hp - 1
        gs.p1.score = gs.p1.score + 5 + self.size / 100
        self.setColor()

        if (self.hp < 0.01):
            if self in gs.gameElements:
                gs.gameElements.remove(self)
            if self in gs.balls:
                gs.balls.remove(self)
            gs.p1.score = gs.p1.score + 10 * self.size
            # gameElements.remove(projectile)
        gs.p1.score = round(gs.p1.score)

    def update(self, gs):
        if self.y > gs.windowY:
            gs.p1.score -= 1000
            gs.gameElements.remove(self)
            gs.balls.remove(self)
            if gs.p1.score < 0:
                gs.died = True
        if (self.x > gs.windowX - self.size):
            self.xMove = 0 - self.xSpeed
            self.y = self.y + 60
        if (self.x < 0 + self.size):
            self.xMove = self.xSpeed
            self.y = self.y + 60
        self.x = self.x + self.xMove
        self.y = self.y + self.yMove
        self.hitbox = pygame.Rect(
            self.x-self.size, self.y-self.size, self.size*2, self.size*2)

    def draw(self, gs):
        pygame.draw.circle(gs.game, (self.color), (self.x, self.y), self.size)


class projectile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        projX = 20 - gs.agility
        projY = 20 - gs.agility
        self.hitbox = pygame.Rect(self.x-projX/2, self.y-projY/2, projX, projY)

    def draw(self, gs):
        if gs.theme == "normal":
            pygame.draw.rect(gs.game, (252, 90, 130), self.hitbox)
        if gs.theme == "contrast":
            pygame.draw.rect(gs.game, (210, 200, 255), self.hitbox)
        if gs.theme == "light":
            pygame.draw.rect(gs.game, (252, 90, 130), self.hitbox)

    def update(self, gs):
        self.x, self.y = self.hitbox.center
        self.hitbox.move_ip(0, -20)
        if self.y < 0:
            if self in gs.gameElements:
                gs.gameElements.remove(self)
        for ball in gs.balls[:]:
            if (ball.detectCollision(self.hitbox)):
                ball.hit(self)
                if self in gs.gameElements:
                    gs.gameElements.remove(self)


def spawn(gs):
    health = randint(1, 10)
    newAlien = alien((25, 234, 119), health)
    gs.balls.append(newAlien)
    gs.gameElements.append(newAlien)
    gs.p1.score = gs.p1.score + 1


schedule.every(1).to(3).seconds.do(spawn, gs)
# gs = gameState()


while gs.should_run:
    # spawn(gs)

    if not gs.died:
        schedule.run_pending()
        if gs.theme == "normal":
            gs.game.fill((8, 6, 30))
            text = gs.font.render(str(gs.p1.score), True, (176, 171, 234))
        if gs.theme == "contrast":
            gs.game.fill((0, 0, 0))
            text = gs.font.render(str(gs.p1.score), True, (255, 255, 255))
        if gs.theme == "light":
            gs.game.fill((195, 192, 226))
            text = gs.font.render(str(gs.p1.score), True, (20, 20, 20))
    else:
        text = gs.font.render("YOU DIED", True, (255, 255, 255))

        # sleep(0.5)
        s = pygame.Surface((1000, 750))  # the size of your rect
        s.set_alpha(128)                # alpha level
        s.fill((60, 0, 0))           # this fills the entire surface
        gs.game.blit(s, (0, 0))    # (0,0) are the top-left coordinates

        textRect = text.get_rect()
        textRect.center = (gs.windowX * 0.5, gs.windowY * 0.5)
        gs.game.blit(text, textRect)
        pygame.display.flip()
        sleep(1)
        gs.should_run = False
    for ge in gs.gameElements:
        if not gs.died:
            ge.update(gs)
        ge.draw(gs)
    textRect = text.get_rect()
    textRect.center = (gs.windowX * 0.9, gs.windowY * 0.1)
    gs.game.blit(text, textRect)
    pygame.display.flip()

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Your score was", gs.p1.score)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
