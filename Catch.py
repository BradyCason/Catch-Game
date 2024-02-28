import sys
import pygame
from random import randint

class Square():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.centerx = self.screen_rect.centerx
        self.rect = pygame.Rect(self.centerx,700, 50, 50)
        self.moving_right = False
        self.moving_left = False
        self.lives = 3
        
    def draw_square(self):
        pygame.draw.rect(self.screen, (255,0,0), self.rect)
        
    def update_square(self):
        if self.moving_right and self.rect.right < 1200:
            self.centerx += 2
        if self.moving_left and self.rect.left > 0:
            self.centerx -= 2
        
        self.rect = pygame.Rect(self.centerx, 700, 50, 50)
        
    def check_lives(self, circle1, circle2, circle3, circle4, new_name):
        if self.lives <= 0:
            print("\nFinal score: " + str(circle1.score + circle2.score + circle3.score + circle4.score))
            with open("Catch_high_score.txt", "r") as document:
                contents = document.read()
                high = contents[0:2]
                name = contents[3:]
                if int(circle1.score + circle2.score + circle3.score + circle4.score) > int(high):
                    with open("Catch_high_score.txt", "w") as document:
                        print(str(circle1.score + circle2.score + circle3.score + circle4.score) + " is the new high score! It is held by " + new_name + ".")
                        if len(str(circle1.score + circle2.score + circle3.score + circle4.score)) == 3:
                            document.write(str(circle1.score + circle2.score + circle3.score + circle4.score) + new_name)
                        elif len(str(circle1.score + circle2.score + circle3.score + circle4.score)) == 2:
                            document.write(str(circle1.score + circle2.score + circle3.score + circle4.score) + " " + new_name)
                        elif len(str(circle1.score + circle2.score + circle3.score + circle4.score)) == 1:
                            document.write(str(circle1.score + circle2.score + circle3.score + circle4.score) + "  " + new_name)
                else:
                    print("\n")
                    print("High score: " + str(high.rstrip()))
                    print("Held by: " + name)
            sys.exit()
        
class Circle():
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.centerx = randint(25, 1175)
        self.centery = randint(-1200,-50)
        self.y = self.centery
        self.rect = pygame.Rect(self.centerx, self.centery, 50, 50)
        self.score = 0
        self.speed = 0.5
        
    def draw_circle(self):
        pygame.draw.circle(self.screen, (200,200,0), (self.centerx, self.centery),25)
        
    def update_circle(self, square, circle_speed, circle1, circle2, circle3, circle4):
        if self.centery >= 825:
            self.centerx = randint(25, 1175)
            self.y = randint(-1200,-50)
            self.centery = self.y
            square.lives -= 1
        else:
            self.y = float(self.y + circle_speed)
            self.centery = self.y
    
    def check_for_collision(self, square, circle1, circle2, circle3, circle4):
        if square.rect.top <= self.centery + 25 and square.rect.bottom >= self.centery -25:
            if square.rect.left <= self.centerx +25 and square.rect.right >= self.centerx -25:
                self.centerx = randint(25, 1175)
                self.y = randint(-1200,-50)
                self.centery = self.y
                self.score += 1

def run_game():
    while True:
        print("\nRules:")
        print("\tUse the arrow keys to move the red square.")
        print("\tTry to catch as many yellow circles as you can.")
        print("\tIf you miss a circle, you lose a life.")
        print("\tYou have 3 lives.")
        print("\tYou will have to click on the game window when it pops up.")
        new_name = input("What is your name: ")
        if input("\nType 'ok' and hit enter to begin: ") == "ok":
            break
        else:
            print("That's not how you spell 'ok' stupid...")
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Catch")
    square = Square(screen)
    circle1 = Circle(screen)
    circle2 = Circle(screen)
    circle3 = Circle(screen)
    circle4 = Circle(screen)
    circle_speed = 0.4
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Final score: " + str(circle1.score + circle2.score + circle3.score + circle4.score))
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    square.moving_right = True
                if event.key == pygame.K_LEFT:
                    square.moving_left = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    square.moving_right = False
                if event.key == pygame.K_LEFT:
                    square.moving_left = False
        
        circle_speed = float(circle_speed + 0.00005)
        screen.fill((20,60,200))
        square.update_square()
        circle1.check_for_collision(square, circle1, circle2, circle3, circle4)
        circle2.check_for_collision(square, circle1, circle2, circle3, circle4)
        circle3.check_for_collision(square, circle1, circle2, circle3, circle4)
        circle4.check_for_collision(square, circle1, circle2, circle3, circle4)
        circle1.update_circle(square, circle_speed, circle1, circle2, circle3, circle4)
        circle2.update_circle(square, circle_speed, circle1, circle2, circle3, circle4)
        circle3.update_circle(square, circle_speed, circle1, circle2, circle3, circle4)
        circle4.update_circle(square, circle_speed, circle1, circle2, circle3, circle4)
        square.draw_square()
        circle1.draw_circle()
        circle2.draw_circle()
        circle3.draw_circle()
        circle4.draw_circle()
        square.check_lives(circle1, circle2, circle3, circle4, new_name)
        pygame.display.flip()
        
run_game()
