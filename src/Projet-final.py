#On importe les differents modules de pygame et random.
import pygame
import random
pygame.init()
pygame.mixer.init()


#On crée notre fenêtre et on crée un nom pour cette dernière. # Toute l'equipe
win = pygame.display.set_mode((1000,650))
pygame.display.set_caption("Pong Game - 1 VERSUS 1")
#On introduit une musique dans le programme # Ashfaq
music = pygame.mixer.Sound('../ressources/sound/music.wav')
music.play(-1)


#On importe les images. # Antoine Ashfaq Dimitrii
scoreboard = pygame.image.load('../ressources/img/scoreboard.png')
menu_bg = pygame.image.load('../ressources/img/menu.png')
aide = pygame.image.load('../ressources/img/aides.png')
mute_button = pygame.image.load('../ressources/img/muted.png')
unmute_button = pygame.image.load('../ressources/img/unmuted.png')


# On crée des variables pour les couleurs que nous allons utiliser # Dimitrii
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# On crée une liste pour pouvoir apres determiner le signe de l'abscice
sens = [-1, 1]

# On crée une fonction pour afficher les textes sur notre fenêtre # Ashfaq + Antoine
def displaytext(text,fontsize,x,y,color):
    font = pygame.font.SysFont('', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    win.blit(text, textpos)

# On crée une fonction pour réinitialiser la balle à chaque point # Dimitrii
def reset_ball(index):
    index.y = 325
    index.x = 250
    index.xx = random.choice(sens)
    index.yy = random.choice(sens)
    index.vel = 2

#On crée une classe pour la balle du jeu. # Dimitrii
class Ball:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.xx = 1
        self.yy = 1
        self.vel = 4
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size, 0)

        if self.y >= 650 - self.size:
            reset_ball(self)
            plat1.score += 1

        if self.y <= self.size:
            reset_ball(self)
            plat2.score += 1

        if self.x == 500 - self.size:
            self.xx = -1
        if self.x == self.size:
            self.xx = 1
        if self.x >= plat2.x - 10 and self.x <= plat2.x + plat2.width + 10 and self.y == plat2.y - 10:
            self.yy = -1
        if self.x >= plat1.x - 10 and self.x <= plat1.x + plat1.width + 10 and self.y == plat1.y + plat1.height + 10:
            self.yy = 1
        self.x += self.vel * self.xx
        self.y += self.vel * self.yy

#On définit la classe pour les differentes plateformes(raquettes qu'on utilisera) # Dimitrii
class platform(object):
    def __init__ (self, x, y, width, height, color):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.color = color
                self.vel = 5
                self.score = 0

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y,self.width, self.height))

#On définit les platformes et la balle avec les differentes variables necessaires. #Toute l'equipe.
plat1 = platform(190, 25, 120, 10, WHITE)
plat2 = platform(190, 615, 120, 10, WHITE)
PongBall = Ball(250, 325, 10, RED)

#Cette fonction permettra la mise a jour des images de notre jeu # ---------->Toute l'equipe <--------
def redrawGameWindow():
    win.fill((0,0,0))
    win.blit(scoreboard, (500,0))

    plat1.draw(win)
    plat2.draw(win)
    PongBall.draw(win)

    # Affiche le score dans le tableau de score
    displaytext(str(plat1.score),100,927,223, GREEN)
    displaytext(str(plat2.score),100,927,378, GREEN)

    # Arrête le jeu quand le score d'un des joueurs arrive a 12, affichant un texte "Gagner"
    if plat1.score == 12:
        displaytext("Joueur 1 GAGNE BRAVO!",40,254,300, RED)
        displaytext("Appuyer ENTRER pour rejouer",40,254,353, GREEN)
        PongBall.vel = 0

    if plat2.score == 12:
        displaytext("Joueur 2 GAGNE BRAVO!",40,254,300, BLUE)
        displaytext("Appuyer ENTRER pour rejouer",40,254,353, GREEN)
        PongBall.vel = 0

    pygame.display.update()

#Fonction qui nous permettra de sélectionner les variables permettant de bouger les platformes # Ashfaq et Antoine
def movement(plat, left_key, right_key):
    keys = pygame.key.get_pressed()
    if keys[left_key] and plat.x > plat.vel:
        plat.x -= plat.vel
    elif keys[right_key] and plat.x < 500 - plat.vel - plat.width:
        plat.x += plat.vel

# Boucle pour le jeu en lui même # Ashfaq
def Game():
    run = True
    while run:
        pygame.time.delay(1)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get ():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_KP_ENTER]:
                plat1.score = 0
                plat2.score = 0
                reset_ball(PongBall)


        movement(plat1, pygame.K_a, pygame.K_d)
        movement(plat2, pygame.K_LEFT, pygame.K_RIGHT)

        redrawGameWindow()
# Fonction pour la page aide #Antoine
def page_aide():
    page = True
    while page:
        mouseclick = pygame.mouse.get_pressed()
        mousep = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get ():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] or mouseclick[0] == 1 and 607 <= mousep[0] <= 956 and 540 <= mousep[1] <= 603:
                page = False
        win.blit(aide, (0,0))
        pygame.display.update()

#Fonction permettant l'arrêt du son dans le jeu #Ashfaq
check_mute = True
def mute_check():
    if check_mute:
        win.blit(unmute_button, (10, 583))
    else:
        win.blit(mute_button, (10, 583))
#Boucle principale\main loop permettant le fonctionnement de notre menu et du jeu en lui même #Antoine
menuRun = True
while menuRun:
    win.blit(menu_bg, (0,0))
    mute_check()
    mouseclick = pygame.mouse.get_pressed()
    mousep = pygame.mouse.get_pos()
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            menuRun = False
        #bouton mute
        if mouseclick[0] == 1 and 10 <= mousep[0] <= 50 and 583 <= mousep[1] <= 642:
            if check_mute:
                pygame.mixer.pause()
                check_mute = False
            else:
                pygame.mixer.unpause()
                check_mute = True
        #bouton jouer
        if mouseclick[0] == 1 and 354 <= mousep[0] <= 657 and 224 <= mousep[1] <=288:
            Game()
        #bouton aide
        if mouseclick[0] == 1 and 377 <= mousep[0] <= 625 and 344 <= mousep[1] <= 415:
            page_aide()
        #bouton quitter
        if mouseclick[0] == 1 and 309 <= mousep[0] <= 692 and 467 <= mousep[1] <= 548:
            menuRun = False
    pygame.display.update()
pygame.quit()
