import pygame
import random
import csv 
import os
CSV_FILE = "player_scores.csv"


def save_to_csv(name, final_score):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player Name", "Score"])
        writer.writerow([name, final_score])


pygame.init()

# 1. Game window
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Car Racing Game")

clock = pygame.time.Clock()

# 2. Colours
GREEN = (35, 125, 55) 
GREY = (65, 65, 70)
WHITE = (255, 255, 255)
YELLOW = (245, 210, 40)
BLUE = (35, 130, 235)
BLACK = (20, 20, 20)
LIGHT_BLUE = (180, 220, 240)
DARK_BLUE = (35, 45, 55)
RED = (255, 0, 0)

# 3. Road settings
ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = 300

# 4. Car settings
CAR_WIDTH = 40
CAR_HEIGHT = 80

# 5. Player position player_x = horizontal position , player_y = vertical position ek aur baat
#  player_x and player_y car ke cenre ko represent nahi karte. ye car ke rectanglular body ke
#  top left corner position ko represent karta hai.
player_x = 180
player_y = 500
PLAYER_STEP = 10

# 6. Enemy position randomly x position to 50 se start hogi aur y position -80 se 
# matlab car ke top point 0 pe hogi aur starting se enter karegi aur screen pe enter karegi
enemy_x = random.randrange(50, 311, 10)
enemy_y = -80

# 7. Enemy speed
ENEMY_SPEED = 10

# 8. Score = 0 initial
score = 0
# pygame.font.sysfont() ke liye , none : default system font use karne ke liye , 40 : font size ke liye


# font score aur restart ke liye 
# big_font GAME OVER message ke liye
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# 9. Game state
game_over = False


# Function 1: Draw Road
def draw_road():

    screen.fill(GREEN)
    # pygame rectangle ke liye order hota hai (x , y , width , height) ROAD_LEFT=50 , ROAD_WIDTH=300
    pygame.draw.rect(
        screen, GREY,
        (ROAD_LEFT, 0, ROAD_WIDTH, 600)
    )

    # Road boundaries
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT, 0), (ROAD_LEFT, 600), 4
    )

    pygame.draw.line(
        screen, WHITE,
        (ROAD_RIGHT, 0), (ROAD_RIGHT, 600), 4
    )

    # Yellow dotted line , 0  se start  600 pe end 60 ke step se (x,y,widht,height)
    for y in range(0, 600, 60):
        pygame.draw.rect(
            screen, YELLOW,
            (198, y, 4, 30)
        )


# Function 2: Draw Car
def draw_car(x, y, color):

    # Car wheels (x-4 , y+12 , 7 , 18): x-4 = body se 4pixels left ,
    #  y+12 = top se 12 pixels neeche , 7 = wheel width , 18 = wheel height
    pygame.draw.rect(screen, BLACK,
                     (x - 4, y + 12, 7, 18))

    pygame.draw.rect(screen, BLACK,
                     (x + 37, y + 12, 7, 18))

    pygame.draw.rect(screen, BLACK,
                     (x - 4, y + 51, 7, 18))

    pygame.draw.rect(screen, BLACK,
                     (x + 37, y + 51, 7, 18))
    # color ek parameter hai jisko ham end mein call karenge
    # Main car body
    pygame.draw.rect(
        screen, color,
        (x, y, CAR_WIDTH, CAR_HEIGHT),
        border_radius=8
    )

    # Front window
    pygame.draw.rect(
        screen, LIGHT_BLUE,
        (x + 7, y + 13, 26, 18),
        border_radius=4
    )

    # Back window
    pygame.draw.rect(
        screen, DARK_BLUE,
        (x + 7, y + 43, 26, 19),
        border_radius=4
    )

    # Headlights
    pygame.draw.rect(screen, YELLOW,
                     (x + 5, y + 3, 8, 5))

    pygame.draw.rect(screen, YELLOW,
                     (x + 27, y + 3, 8, 5))

data_saved = False


def get_player_name():
    name = ""
    entering = True
    while entering:
        screen.fill(DARK_BLUE)
        title = font.render("Enter Player Name", True, YELLOW)
        name_box = font.render(name + "_", True, WHITE)
        hint = font.render("Press ENTER to Start", True, LIGHT_BLUE)

        screen.blit(title, (75, 200))
        screen.blit(name_box, (75, 260))
        screen.blit(hint, (75, 320))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() if name.strip() != "" else "Unknown Player"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode
        clock.tick(30)


player_name = get_player_name()


# 10. Main Game Loop
# game hamesa run karne ke bad chalta rahega jab tak true rahega ye window close karne ke bad ye false hoga aur loop bhi band
running = True

while running:

    # loop ke speed ko define karta hai yani 60 times per second ke hisab se chalta hai
    #  varna computere apne hisab se loop ko kitni bhi speed se chalata 
    clock.tick(60)

    # Events and keyboard controls
    # pygame se pendingg events recieve karo
    for event in pygame.event.get():

        # check karta hai ki user ne game ka window close to nahi kiya.
        # running = false : agar close window mila, to running variable ki value false ho gayegi aur loop vhi rook jayeggi
        if event.type == pygame.QUIT:
            running = False

        # pygame.keyboard ka matlab hai user ne keyboard press ki hai.
        elif event.type == pygame.KEYDOWN:

            # Restart game
            if game_over and event.key == pygame.K_r:
            # kya user ne R key press to nahi ki hai dono fullfill honi chahiye game_over honi chahiye aur R key press honi chahiye

                player_x = 180
                player_y = 500

                enemy_x = random.randrange(50, 311, 10)
                enemy_y = -80
            # game start hone se pehle score ki value 0 hogi
                score = 0
                game_over = False
                data_saved = False
            # Player movement
            elif not game_over:


                # left aur right lest right move karne ke liye 
                if event.key == pygame.K_LEFT:
                    # har game frame mein player ki x position 10 pixels si left move karegi kunki PLAYER_STEP=10 hai
                    # aur max ensure karega ki x position 50 se niche na jaaye 
                    player_x = max(50, player_x - PLAYER_STEP)
                    # har game frame mein player ki y position 10 pixels si right move karegi kunki PLAYER_STEP=10 hai
                    # aur min ensure karega ki x position 310 se niche na jaaye 
                elif event.key == pygame.K_RIGHT:
                    player_x = min(310, player_x + PLAYER_STEP)

    # Enemy movement
    if not game_over:
        #  har game frame mein enemy ki y position 5 pixels se increase hogi kyunki ENEMY_SPEED=5 hai
        enemy_y += ENEMY_SPEED

        # Enemy reset and score update
        # check karega ki car ki y position 600 se jyada ho gya hai ki nii  ,
        #  for example enemy_y = 601 hui aur ye condition true ho gayi aur 
        # score 1 se increase karta hai aur aur hir enemy car scren ki upar 
        # se enter karti hai kyunki enemy_y = -80 aa gya nad repeat
        if enemy_y > 600:

            score += 1
            enemy_y = -80

            enemy_x = random.randrange(50, 311, 10)

        # Player collision rectangle : matlab computer ek invisible rectangular
        #  boundary create karta hai taki collision detect karna aasan ho
        player_rect = pygame.Rect(
            player_x, player_y,
            CAR_WIDTH, CAR_HEIGHT
        )

        # Enemy collision rectangle : same for enemy
        enemy_rect = pygame.Rect(
            enemy_x, enemy_y,
            CAR_WIDTH, CAR_HEIGHT
        )

        # .colliderect() -isska full meaning collision between rectangles - actual Collision detection 
        # agar game mein rectangular cars overlap karta hai to to game_over = true hogayega aur game end aur while loop bhi end
        if player_rect.colliderect(enemy_rect):
            game_over = True
            if not data_saved:
                save_to_csv(player_name, score)
                data_saved = True

    # Draw road
    draw_road()

    # Draw player car
    draw_car(player_x, player_y, BLUE)

    # Draw enemy car
    draw_car(enemy_x, enemy_y, RED)

    # Display score
    # font.render() text ko image mein convert karta hai
    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    # screen.blit() : text ko image meien convert kiya tha na usko screen par show karta hai
    # screen ; hamari game window
    # score_text : font.render se create text surface   
    # (10 , 10) : screen par text ki position
    screen.blit(score_text, (10, 10))

    # Game Over screen
    # if game_over: ka matlab hai ki agar game_over ki value True hai, tabhi andar ka code execute hoga
    if game_over:
        # game_over karke red color mein display karta hai
        game_over_text = big_font.render(
            "GAME OVER", True, RED
        )
    # ye player ko instructions deta hai ki R key press karne par game restart hoga
        restart_text = font.render(
            "Press R to Restart", True, WHITE
        )
    # GAME OVER message ko x = 65 aur y = 250 par display karta hai.
        screen.blit(game_over_text, (65, 250))
        screen.blit(restart_text, (65, 320))

    # Update display , iska kam hai screen par banayi gayi changes ko display karna.
    pygame.display.flip()

# jab loop stop ho gata hai yani window jab cloase ho gata hai
#  tab ye function initialized modulus ko properly shutdown kara dete hai.
pygame.quit() 