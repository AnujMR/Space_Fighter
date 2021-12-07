import pygame,sys

pygame.init()
pygame.mixer.init()

# Create a display
screen = pygame.display.set_mode((600,300))
pygame.display.set_caption('Space Fighters')
width = screen.get_width()
height = screen.get_height()

# Create a border in the middle of the display
border_width = 10
border = pygame.Rect(295, 0, border_width, height)

# Set the frame rate (FPS) for the game
clock = pygame.time.Clock()
fps = 60

# Load images and scale them as per the requirement
F1 = pygame.image.load('F:\SpaceFighter\Fighter1.png')
F2 = pygame.image.load('F:\SpaceFighter\Fighter2.png')
Space = pygame.image.load('F:\SpaceFighter\Space.png')
Button = pygame.image.load('F:\SpaceFighter\Button.png')
button_width = 150
button_height = 70
Button_start = pygame.transform.scale(Button,(button_width,button_height))
Button_controls = pygame.transform.scale(Button,(button_width+50,button_height))
Button_credits = pygame.transform.scale(Button,(button_width-20,button_height-20))
Space_Background = pygame.transform.scale(Space,(600,300))
Fighter1 = pygame.transform.scale(F1, (50,50))
Fighter2 = pygame.transform.rotate(pygame.transform.scale(F2, (50,50)), 180)
F_2 = pygame.transform.scale(F2, (50,50))
Fighter_width = Fighter1.get_width()
Fighter_height = Fighter1.get_height()

# Load sound effects
Fire_sound = pygame.mixer.Sound('F:\SpaceFighter\Fire_sound.mp3')
Winner_sound = pygame.mixer.Sound('F:\SpaceFighter\Winning.mp3')

# Create lists for bullets
Fighter1_bullets = []
Fighter2_bullets = []

# Create new events for players getting hit
Fighter1_Hit = pygame.USEREVENT + 1
Fighter2_Hit = pygame.USEREVENT + 2

# Set the health of the players
Fighter1_Health = 10
Fighter2_Health = 10

# Create Rectangles for the Spaceships
Fighter1_rect = pygame.Rect(120, height//2-30, Fighter_width, Fighter_height)
Fighter2_rect = pygame.Rect(420, height//2-30, Fighter_width, Fighter_height)

# Set the font style and font size
Health_Font = pygame.font.SysFont('comicsans', 30)
Winner_Font = pygame.font.SysFont('comicsans', 100)
Button_Font = pygame.font.SysFont('comicsans', 40)
Controls_Font = pygame.font.SysFont('comicsans', 30)
Credits_Font = pygame.font.SysFont('comicsans',25)

# Create Rectangles for the Spaceships
Fighter1_rect = pygame.Rect(120, height//2-30, Fighter_width, Fighter_height)
Fighter2_rect = pygame.Rect(420, height//2-30, Fighter_width, Fighter_height)

# Set the health of the players
Fighter1_Health = 10
Fighter2_Health = 10

# Create lists for bullets
Fighter1_bullets = []
Fighter2_bullets = []
Max_bullets = 3

# Set the Velocity
vel = 5
bullet_vel = 7

Up = False
Down = False

def draw_game(Fighter1_rect, Fighter2_rect, Fighter1_bullets, Fighter2_bullets, Fighter1_Health, Fighter2_Health):
    screen.blit(Space_Background,(0,0))
    pygame.draw.rect(screen, (255,255,255), border)

    Fighter1_Health_text = Health_Font.render("Health :" + str(Fighter1_Health), 1, (255,255,255)) 
    Fighter2_Health_text = Health_Font.render("Health :" + str(Fighter2_Health), 1, (255,255,255)) 
    screen.blit(Fighter1_Health_text, (10, 10))
    screen.blit(Fighter2_Health_text, (width - Fighter2_Health_text.get_width() - 10, 10))

    for bullet in Fighter1_bullets:
        pygame.draw.rect(screen,(255,0,0),bullet)
    
    for bullet in Fighter2_bullets:
        pygame.draw.rect(screen,(0,0,255),bullet)
        
    screen.blit(Fighter1, Fighter1_rect)  
    screen.blit(Fighter2, Fighter2_rect)
    pygame.display.update()

def bullets_movement(Fighter1_bullets, Fighter2_bullets, Fighter1_rect, Fighter2_rect):
    for bullet in Fighter1_bullets:
        bullet.x += bullet_vel
        if Fighter2_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Fighter2_Hit)) # It will just trigger the event written inside the brackets
            Fighter1_bullets.remove(bullet)
        elif bullet.x >= width:
            Fighter1_bullets.remove(bullet)
    
    for bullet in Fighter2_bullets:
        bullet.x -= bullet_vel
        if Fighter1_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Fighter1_Hit))
            Fighter2_bullets.remove(bullet)
        elif bullet.x <= 0:
            Fighter2_bullets.remove(bullet)

def draw_winner(text):
    winner_text = Winner_Font.render(text,1,(0,0,0))
    Rect = pygame.Rect(width//2 - winner_text.get_width()//2, height//2 - winner_text.get_height()//2,winner_text.get_width(),winner_text.get_height())
    pygame.draw.rect(screen,(100,100,100), Rect)
    screen.blit(winner_text,(width//2 - winner_text.get_width()//2, height//2 - winner_text.get_height()//2))
    Winner_sound.play()
    pygame.display.update()
    pygame.time.delay(3000)
    main()

def movements(Fighter1_rect, Fighter2_rect, key_pressed): 
    # For Fighter - 1
    if key_pressed[pygame.K_d] and Fighter1_rect.x + Fighter_width < border.x:
        Fighter1_rect.x += vel
    if key_pressed[pygame.K_a] and Fighter1_rect.x > 0:
        Fighter1_rect.x -= vel
    if key_pressed[pygame.K_w] and Fighter1_rect.y > 0:
        Fighter1_rect.y -= vel
        Up = True
        Down = False
    elif key_pressed[pygame.K_s] and Fighter1_rect.y + Fighter_height < height:
        Fighter1_rect.y += vel
        Up = False
        Down = True
    else:
        Up = False
        Down = False
    

    # For Fighter - 2
    if key_pressed[pygame.K_RIGHT] and Fighter2_rect.x + Fighter_width < width:
        Fighter2_rect.x += vel
    if key_pressed[pygame.K_LEFT] and Fighter2_rect.x > border.x + border_width:
        Fighter2_rect.x -= vel
    if key_pressed[pygame.K_UP] and Fighter2_rect.y > 0:
        Fighter2_rect.y -= vel
    if key_pressed[pygame.K_DOWN] and Fighter2_rect.y + Fighter_height < height:
        Fighter2_rect.y += vel

def main_menu():
    Click = False
    while True:
        screen.blit(Space_Background,(0,0))

        screen.blit(Button_start,(width//2 - button_width//2, height//2 - button_height//2))
        Start_button = pygame.Rect(width//2 - button_width//2, height//2 - button_height//2, button_width, button_height)
        Start_text = Button_Font.render('START',1,(0,0,0))
        screen.blit(Start_text, (width//2 - Start_text.get_width()//2, height//2 - Start_text.get_height()//2))
        
        screen.blit(Button_controls,(width//2 - button_width//2 - 25, height//2 - button_height//2 + 70))
        Controls_button = pygame.Rect(width//2 - button_width//2 - 25, height//2 - button_height//2 + 70, button_width + 50, button_height)
        Controls_text = Button_Font.render('CONTROLS',1,(0,0,0))
        screen.blit(Controls_text,(width//2 - button_width//2 - 2, height//2 - button_height//2 + 95))

        screen.blit(Button_credits,(width//2 - button_width//2 - 200, height//2 - button_height//2 + 120))
        Credits_button = pygame.Rect(width//2 - button_width//2 - 200, height//2 - button_height//2 + 120, button_width, button_height)
        Credits_text = Controls_Font.render('CREDITS',1,(0,0,0))
        screen.blit(Credits_text,(width//2 - button_width//2 - 180, height//2 - button_height//2 + 138))

        mx, my = pygame.mouse.get_pos()
        if Start_button.collidepoint((mx, my)):
            if Click == True:
                main()
        if Controls_button.collidepoint((mx, my)):
            if Click == True:
                controls()
        if Credits_button.collidepoint((mx, my)):
            if Click == True:
                credits()

        Click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    Click = True

        pygame.display.update()

def controls():
    while True:
        screen.blit(Space_Background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        Fighter1_controls = Controls_Font.render('Player 1 -',1,(255,255,255))
        Fighter2_controls = Controls_Font.render('Player 2 -',1,(255,255,255))
        Fighter1_controls_2 = Controls_Font.render('Movements : W,A,S,D        Fire : Left CTRL',1,(255,255,255))
        Fighter2_controls_2 = Controls_Font.render('Movements : Arrow Keys     Fire : Right CTRL',1,(255,255,255))
        screen.blit(Fighter1_controls, (10,20))
        screen.blit(Fighter1, (150,5)) 
        screen.blit(Fighter1_controls_2,(10,70))
        screen.blit(Fighter2_controls, (10, 130))
        screen.blit(F_2, (150,115)) 
        screen.blit(Fighter2_controls_2,(10, 180))
        pygame.display.update()

def credits():
    while True:
        screen.blit(Space_Background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        Credits = Button_Font.render('Credits :',1,(255,255,255))
        Anuj = Credits_Font.render('Anuj Ramane (Developer)',1,(255,255,255))
        screen.blit(Credits, (10,20))
        screen.blit(Anuj, (10,70))
        pygame.display.update()

def main():
    # Create Rectangles for the Spaceships
    Fighter1_rect = pygame.Rect(120, height//2-30, Fighter_width, Fighter_height)
    Fighter2_rect = pygame.Rect(420, height//2-30, Fighter_width, Fighter_height)

    # Set the health of the players
    Fighter1_Health = 10
    Fighter2_Health = 10

    # Create lists for bullets
    Fighter1_bullets = []
    Fighter2_bullets = []

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(Fighter1_bullets)<Max_bullets:
                    bullet = pygame.Rect(Fighter1_rect.x + Fighter_width, Fighter1_rect.y + Fighter_height//2, 10, 5)
                    Fighter1_bullets.append(bullet)
                    Fire_sound.play()
                
                if event.key == pygame.K_RCTRL and len(Fighter2_bullets)<Max_bullets:
                    bullet = pygame.Rect(Fighter2_rect.x, Fighter2_rect.y + Fighter_height//2 - 4, 10, 5)
                    Fighter2_bullets.append(bullet)
                    Fire_sound.play()
                
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == Fighter1_Hit:
                Fighter1_Health -= 1

            if event.type == Fighter2_Hit:
                Fighter2_Health -= 1
                

        bullets_movement(Fighter1_bullets, Fighter2_bullets, Fighter1_rect, Fighter2_rect)
        draw_game(Fighter1_rect, Fighter2_rect, Fighter1_bullets, Fighter2_bullets, Fighter1_Health, Fighter2_Health)
        key = pygame.key.get_pressed()
        movements(Fighter1_rect, Fighter2_rect, key)

        winner_text = ""
        if Fighter1_Health <= 0:
            winner_text = "Player 2 Won!"
        if Fighter2_Health <= 0:
            winner_text = "Player 1 Won!"
        if winner_text != "":
            draw_winner(winner_text)
            
        pygame.display.update()
            
main_menu()