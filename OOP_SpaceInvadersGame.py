import pygame
import random
import time
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Space Invaders")

pygame.mixer.pre_init()
firingSFX = pygame.mixer.Sound("mixkit-short-laser-gun-shot-1670.wav")
losingSFX = pygame.mixer.Sound("mixkit-funny-system-break-down-2955.wav")
nextlevelSFX = pygame.mixer.Sound("next-level.wav")
winSFX = pygame.mixer.Sound("win_spaceinvaders.wav")

redAlien = pygame.image.load("redalien_spaceinvaders.png")
redAlien = pygame.transform.scale(redAlien, (30,30))

blueAlien = pygame.image.load("bluealien_spaceinvaders.png")
blueAlien = pygame.transform.scale(blueAlien, (30,30))

greenAlien = pygame.image.load("greenalien_spaceinvaders.png")
greenAlien = pygame.transform.scale(greenAlien, (30,30))

ship = pygame.image.load("ship_spaceinvaders.png")
ship = pygame.transform.scale(ship, (50,30))

bullet = pygame.image.load("bullet_spaceinvaders.png")
bullet = pygame.transform.rotate(bullet, 90)
bullet = pygame.transform.scale(bullet,(3, 10))

alienBullet = pygame.image.load("alienbullet_spaceinvaders.png")
alienBullet = pygame.transform.rotate(alienBullet, 90)
alienBullet = pygame.transform.scale(alienBullet,(3, 10))

background = pygame.image.load("bgart_spaceinvaders.jpg")
background = pygame.transform.scale(background, (800,800))

pygame.mixer.Sound.set_volume(firingSFX, 0.5)

class Character:

    def __init__(self,x):
        self.x = x
        self.image = blueAlien
        self.length = 30
        self.width = 30

    def draw(self): #drawing chara sprite
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, self.color, (self.x, self.y,self.width, self.length), 0)


class Ship (Character):
    def __init__(self,x,y):
        Character.__init__(self,x)
        self.image = ship
        Ship.width = 50
        self.health = 5
        self.y = y
        self.move = False
        self.fire = False

    def collision(self):
        if self.x <= 0:
            self.x = 1
        if self.x >= 800 - Ship.width:
            self.x = 801 - Ship.width   

    def move_ship(self,direction):
        if self.move:
            self.x += 5*direction
            self.collision() 
            

class Bullet(Character):
    def __init__(self,x,y):
        Character.__init__(self,x)
        self.image = bullet
        self.length = 10
        self.width = 3
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= 4
        

class Alien(Character):
    def __init__(self,x,y,direction):
        Character.__init__(self,x)
        self.image = blueAlien
        Alien.direction = direction
        Alien.bullets = 1
        self.changex = 2
        self.changey = 10
        self.y = 20 + y

    def shift_down(self):
        self.y += self.length + self.changey

    def change_direction(self):
        Alien.direction *= -1

    def move_alien(self):
        self.x += self.changex * Alien.direction


        

        
class SuperAlien (Alien):
    
    def __init__(self, x,y,direction):
        Alien.__init__(self,x,y,direction)
        self.direction = direction
        self.image = redAlien
        self.changex = 3
        SuperAlien.bullets = 3
        
    def change_super_direction(self):
        SuperAlien.direction *= -1

    def move_super_alien (self):
        self.x += self.changex* SuperAlien.direction
        

class AlienBullets(Bullet):

    def __init__(self, x, y):
        Bullet.__init__(self,x,y)
        self.image = alienBullet

    def move_down(self):
        self.y += 4
    
class ShooterAlien(Alien):

    def __init__(self,x,y,direction):
         SuperAlien.__init__(self,x,y,direction)
         self.image = greenAlien
         ShooterAlien.bullets = 5
         ShooterAlien.changex = 6
         ShooterAlien.changey = 15
         self.listOfBullets = []

    def change_shooter_direction(self):
        ShooterAlien.direction *= -1

    def move_shooter_alien(self):
        self.x += self.changex * ShooterAlien.direction

    def shift_shooter_down(self):
        self.y += self.length + self.changey

    def add_bullet(self,b):
        if len(self.listOfBullets) <= 5:
            self.listOfBullets.append(b)

    def alien_bullet_list(self):
        return self.listOfBullets

    def draw_bullets(self):
        for b in self.listOfBullets:
            b.draw()


class Game:

    
    def __init__(self, enemyList, ship):#constructor
        self.enemyList = enemyList
        self.superAlienList = []
        self.shooterAlienList = []
        self.ship = ship
        self.bullet_list = []
        self.level = 1
        self.lives = 3
        self.super_number = 0
        self.nostartlvl3 = False


    def show_text(self,msg,x,y,color):#used to show text on display
        fontobj = pygame.font.SysFont("freesans", 32)
        msgobj = fontobj.render(msg, False, color)
        screen.blit(msgobj, (x,y))

    def hud(self):
        fontobj = pygame.font.SysFont("freesans", 20)
        pygame.draw.rect(screen, (255,255,255), (690, 750, 110, 25), 0)
        msgobj = fontobj.render("health: "+str(self.ship.health*20), False, (48,213,200))
        screen.blit(msgobj, (700, 750))

        if (self.ship.health == 1):
            pygame.draw.rect(screen, (255,255,255), (0, 750, 135, 25), 0)
            msgobj2 = fontobj.render("HEALTH LOW!", False, (255,87,51))
            screen.blit(msgobj2, (0, 750))

    def regen_aliens(self):#makes aliens again after dying

        self.enemyList = []
        self.bullet_list = []
        self.super_num = 0
        self.ship.x = 400
        

    def enemy_level_list(self):#returns the current enemy list
        if self.level == 1:
            return self.enemyList
        elif self.level == 2:
            return self.superAlienList
        elif self.level == 3:
            return self.shooterAlienList


    def create_superAlien(self,direction,one_x):

        j = 0
        k = 0
        supAlien = False
        x_val = 0
        y_val = 0
        supAlien1 = 0

        special_aliens = []
        
        for i in self.superAlienList:  
            if (type(i) == SuperAlien):
                supAlien = True
                j = i
                special_aliens.append(j)

            else:
                if k == 0:
                    k = i      

        if supAlien:
            y_val = j.y + j.length + 40

        elif len(self.superAlienList) == 0:
            y_val = 10

        else:
            y_val = k.y + k.length
            
        x_val = one_x
       
        superA = SuperAlien(x_val, y_val, direction)
        self.superAlienList.append(superA)

    def create_shooterAlien(self):

        current_x = 30
        
        for a in range(5):
            shooter = ShooterAlien(current_x, 10, 1)
            self.shooterAlienList.append(shooter)
            current_x = current_x + (shooter.width + 10)
        print(len(self.shooterAlienList))
        pygame.display.update()
            
            
  
    def game_over(self):#losing condition triggered

        time.sleep(2)
        screen.blit(background, (0,0))
        self.show_text("you lose!", 350, 350, (48,213,200))
        losingSFX.play(0)                    
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        exit()            

    def check_win(self):#checks if won, and if so, moves to next level OR player beat game

        list_of_enemies = self.enemy_level_list()
        
        if len(list_of_enemies) == 0:#if no aliens left
            if (self.level == 2):
                if self.super_number >= 5: 
                    time.sleep(2)
                    screen.blit(background, (0,0))
                    self.level += 1
            else:
                time.sleep(2)
                screen.blit(background, (0,0))
                self.level += 1

            if self.level >= 4:#if player beat final level
                self.show_text("you win!", 350, 350, (48,213,200))
                winSFX.play(0)
                pygame.display.update()
                time.sleep(3)
                pygame.quit()
                exit()
                
            else:
                
                self.show_text("round "+str(self.level), 350, 350, (48,213,200))
                nextlevelSFX.play(0)
                self.regen_aliens()
                pygame.display.update()
                time.sleep(3)
                

    def detect_alien_collision(self, l):# when the aliens hit the edge

        collision = False
        
        for a in l:
            if a.x <= 0 or a.x >= 800-a.width:#if hits edge
                collision = True

        if collision and len(l)>0:
            for a in l:
                a.shift_down()
                #changes direction for all aliens
                if l[0] == a:
                    if self.level == 1:
                        a.change_direction()
                    if self.level == 2:
                        a.change_super_direction()
                #checks to see if aliens have gone too far down
                if l[len(l)-1] == a:
                    if a.y + 3*(a.length) > self.ship.y+self.ship.length+10:
                        self.game_over()

    def detect_shooterAlien_collision(self):
        collision = False
        for sa in self.shooterAlienList:
            if sa.x <= 0 or sa.x >=800-sa.width:
                collision = True


        if collision and len(self.shooterAlienList) > 0:
            for a in self.shooterAlienList:
                a.shift_shooter_down()
                
                if a == self.shooterAlienList[0]:
                    a.change_shooter_direction()

                if self.shooterAlienList[len(self.shooterAlienList)-1] == a:
                    if a.y + 3*a.length > self.ship.y + self.ship.length + 10:
                        self.game_over()
                


    def alien_bullets_collision(self,a): # a is each indv shooter alien

        healthLost = 0

        for b in a.alien_bullet_list():
            if self.ship.x -1 < b.x < self.ship.x + 1 + self.ship.width and self.ship.y <= b.y <= self.ship.y +self.ship.length:
                a.listOfBullets.remove(b)
                healthLost += 1

            if (b.y <= 0):
                a.listOfBullets.remove(b)

        if (healthLost > 0):
            print(healthLost)

        return healthLost


    def create_new_bullet(self):#creates a new bullet once SPACE is pressed
        s = Bullet(self.ship.x + self.ship.width/2, self.ship.y)
        self.bullet_list.append(s)

    def detect_alien_bullet(self,b):#checks to see if any of the bullets have hit the aliens
        #called in bullet_move

        l = self.enemy_level_list()
        
        for a in l:
            if a.y<= b.y <= a.y+a.length and a.x-1<= b.x <=a.x+1+a.width:
                a.bullets -= 1
                
                if a.bullets <= 0:
                    l.remove(a)
                        
                self.bullet_list.remove(b)

    

    
    def bullet_move(self):#controlls movement of bullets as a group
        for b in self.bullet_list:
            b.move_up()
            if (b.y <= 0):#removes bullets once gone off screen
                self.bullet_list.remove(b)

            self.detect_alien_bullet(b)

        
        
    def play(self):#runs the game
        
        ship_direction = 1
        start = time.time()
        lives = self.lives
        y_of_end = 0

        self.level = 1 #TESTING
        
        while True:
           
            screen.blit(background, (0,0))
            
            if (lives > self.lives):
                lives -= 1
                print(lives)
                start = time.time()

            duration = time.time() - start


            #FIRST GAME ROUND

            if self.level == 1:

                list_of_enemies = self.enemy_level_list()

                for a in list_of_enemies:
                    a.draw()
                    a.move_alien()
                    
                self.detect_alien_collision(list_of_enemies)

                self.ship.move_ship(ship_direction)
                ship.draw()

                self.bullet_move()
                
                for s in self.bullet_list:
                    s.draw()

                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    #input check
                    if event.type == pygame.KEYDOWN:
                        #spaceship controls
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.ship.move = True
                            ship_direction = -1
                            
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.ship.move = True
                            ship_direction = 1

                        if event.key == pygame.K_SPACE:#makes bullets
                            if len(self.bullet_list) <= 5:
                                self.create_new_bullet()
                                firingSFX.play(0)
                                               

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.ship.move = False

                self.check_win()#check for win condition


            #SECOND GAME ROUND

            elif self.level == 2:

                one_x = 10
                
                list_of_enemies = self.enemy_level_list()

                for a in list_of_enemies:
                    a.draw()
                    a.move_super_alien()
                    
                    if list_of_enemies[0] == a:
                        d = a.direction
                        one_x = a.x

                if duration > 4 and self.super_number < 5: #makes a super alien
                    if len(self.superAlienList) == 0:
                        d = 1
                    
                    start = time.time()                 
                    self.create_superAlien(d,one_x)
                    self.super_number += 1

                self.detect_alien_collision(list_of_enemies)

                self.ship.move_ship(ship_direction)
                ship.draw()

                self.bullet_move()
                
                for s in self.bullet_list:
                    s.draw()

                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    #input check
                    if event.type == pygame.KEYDOWN:
                        #spaceship controls
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.ship.move = True
                            ship_direction = -1
                            
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.ship.move = True
                            ship_direction = 1

                        if event.key == pygame.K_SPACE:#makes bullets
                            if len(self.bullet_list) <= 5:
                                self.create_new_bullet()
                                firingSFX.play(0)

                                                        

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.ship.move = False

                self.check_win()#check for win condition

            #THIRD GAME ROUND

            elif self.level == 3:

                healthLost = 0

                list_of_enemies = self.enemy_level_list()

                if len(list_of_enemies) == 0 and self.nostartlvl3 == False:
                    self.create_shooterAlien()
                    self.nostartlvl3 = True

                if duration > 3: 
                    start = time.time()

                    for a in list_of_enemies:
                        b = AlienBullets(a.x + a.width/2, a.y + a.width)
                        a.add_bullet(b)

                for a in list_of_enemies:
                    a.draw()
                    a.move_shooter_alien()

                    for b in a.listOfBullets:
                        b.move_down()
                    
                    a.draw_bullets()
                    healthLost += self.alien_bullets_collision(a)

                self.detect_shooterAlien_collision()

                self.ship.health -= healthLost

                if (ship.health <= 0):
                    self.game_over()
                    

                self.ship.move_ship(ship_direction)
                ship.draw()

                self.bullet_move()
                
                for s in self.bullet_list:
                    s.draw()

                self.hud()

                for event in pygame.event.get():
                    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                        7
     
                    #input check
                    if event.type == pygame.KEYDOWN:
                        #spaceship controls
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.ship.move = True
                            ship_direction = -1
                            
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.ship.move = True
                            ship_direction = 1

                        if event.key == pygame.K_SPACE:#makes bullets
                            if len(self.bullet_list) <= 5:
                                self.create_new_bullet()
                                firingSFX.play(0)

                                               
                                               

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.ship.move = False

                self.check_win()#check for win condition

                
            clock.tick(60)
            pygame.display.update()  


#alien creation:

alienList = []
distance = 10

for l in range (5):
    distance = 10
    for i in range (10):
        a = Alien(distance, l*40,1)
        alienList.append(a)
        distance += a.width + 10

#ship creation:
ship = Ship(400, 700)
        
spaceInvaders = Game(alienList, ship)
spaceInvaders.play()
