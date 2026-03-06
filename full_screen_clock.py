import pygame
import time
from datetime import datetime
import subprocess
import threading
from Display_Capture import capture_images


# Initialize pygame
pygame.init()


# Set up the screen (full screen mode)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
image_size = ((screen.get_width() // 2) - 2.5, (screen.get_height() // 2) - 2.5)
pygame.display.set_caption("Current Time")

# Load images
#image1 = pygame.image.load("Bed_Display.jpg")  # Replace with actual image paths
#image2 = pygame.image.load("Closet_Display.jpg")

# Set image sizes (adjust as needed)
#image1 = pygame.transform.scale(image1, image_size)
#image2 = pygame.transform.scale(image2, image_size)

# Set font and color
font = pygame.font.Font(None, 400)
text_color = (255, 255, 255)
line_color = (255, 255, 255)




# Password
PASSWORD = "1234"  # Change this to your desired password
MAX_ATTEMPTS = 5
WAIT_TIME = 60  # Wait time in seconds

# Function to load images dynamically
def load_images():
    image1 = pygame.image.load("Live_Stream/Bed_Display.jpg")
    image2 = pygame.image.load("Live_Stream/Closet_Display.jpg")
    #image_size = ((screen.get_width() // 2) - 2.5, (screen.get_height() // 2) - 2.5)
    image1 = pygame.transform.scale(image1, image_size)
    image2 = pygame.transform.scale(image2, image_size)
    return image1, image2

# Function to draw number pad like iPhone layout
def draw_number_pad():
    font_pad = pygame.font.Font(None, 100)
    button_size = 100
    padding = 20
    buttons = []
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (1, 3)]
    enter_pos = (2, 3)
    delete_pos = (0, 3)

    for i, num in enumerate(numbers):
        col, row = positions[i]
        rect = pygame.Rect(screen.get_width() // 2 + col * (button_size + padding) - 200,
                           screen.get_height() // 2 + row * (button_size + padding) + 100,
                           button_size, button_size)
        buttons.append((num, rect))
        pygame.draw.rect(screen, (100, 100, 100), rect)
        text = font_pad.render(num, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))

    enter_rect = pygame.Rect(screen.get_width() // 2 + enter_pos[0] * (button_size + padding) - 200,
                             screen.get_height() // 2 + enter_pos[1] * (button_size + padding) + 100,
                             button_size, button_size)
    delete_rect = pygame.Rect(screen.get_width() // 2 + delete_pos[0] * (button_size + padding) - 200,
                              screen.get_height() // 2 + delete_pos[1] * (button_size + padding) + 100,
                              button_size, button_size)
    buttons.append(("ENTER", enter_rect))
    buttons.append(("DELETE", delete_rect))
    
    pygame.draw.rect(screen, (0, 200, 0), enter_rect)
    pygame.draw.rect(screen, (200, 0, 0), delete_rect)

    return buttons

# Function to display password input
def password_input():
    user_input = ""
    font_small = pygame.font.Font(None, 100)
    input_active = True
    attempts = 0

    while input_active:
        screen.fill((0, 0, 0))
        prompt = font_small.render("Enter Password:", True, text_color)
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
        screen.blit(prompt, prompt_rect)
        input_text = font_small.render(user_input, True, text_color)
        input_rect = input_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(input_text, input_rect)
        buttons = draw_number_pad()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for num, rect in buttons:
                    if rect.collidepoint(event.pos):
                        if num == "ENTER":
                            if user_input == PASSWORD:
                                return True
                            else:
                                attempts += 1
                                user_input = ""
                                if attempts >= MAX_ATTEMPTS:
                                    message = font_small.render("Too many attempts. Wait 1 minute.", True, text_color)
                                    screen.blit(message, (screen.get_width() // 2 - message.get_width() // 2, screen.get_height() // 2 + 100))
                                    pygame.display.flip()
                                    time.sleep(WAIT_TIME)
                                    attempts = 0
                        elif num == "DELETE":
                            user_input = user_input[:-1]
                        else:
                            user_input += num



def ALARM():

    file_path = "mixkit-sound-alert-in-hall-1006.wav"
    with open("alarm_check.txt", "r") as f:
        alarm = f.read()

    if alarm == "ALARM":
        process = subprocess.Popen(["afplay", file_path])
        time.sleep(5)
        process.terminate()





position = "center"
running = True
# Create the thread
thread = threading.Thread(target=capture_images())

# Start the thread
thread.start()


while running:


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if position == "center":
                if password_input():
                    font = pygame.font.Font(None, 200)
                    position = "lower_left"
                    
            elif position == "lower_left":
                font = pygame.font.Font(None, 400)
                position = "center"
    
    
    with open("cleanroom.txt", "r") as f:
        clean = f.read()
    
    current_time = datetime.now().strftime('%H:%M:%S')
    text = font.render(current_time, True, text_color)
    text_rect = text.get_rect()
    screen.fill((0, 0, 0))

    if position == "center":
        text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
#    elif position == "lower_left":
 #       text_rect.center = (screen.get_width() // 4, screen.get_height() * 3 // 4)
  #      pygame.draw.line(screen, line_color, (screen.get_width() // 2, 0), (screen.get_width() // 2, screen.get_height()), 5)
   #     pygame.draw.line(screen, line_color, (0, screen.get_height() // 2), (screen.get_width(), screen.get_height() // 2), 5)
    #    screen.blit(image1, (0, 0))
     #   screen.blit(image2, (screen.get_width() - image_size[0], 0))
    # Customize this variable for the text you want to display in the bottom-right corner

    # In the position == "lower_left" section:
    elif position == "lower_left":

        image1, image2 = load_images()
        # Display time in the bottom-left corner
        text_rect.center = (screen.get_width() // 4, screen.get_height() * 3 // 4)  # 10 is the padding from the screen edge
        screen.blit(image1, (0, 0))
        screen.blit(image2, (screen.get_width() - image_size[0], 0))
        pygame.draw.line(screen, line_color, (screen.get_width() // 2, 0), (screen.get_width() // 2, screen.get_height()), 5)
        pygame.draw.line(screen, line_color, (0, screen.get_height() // 2), (screen.get_width(), screen.get_height() // 2), 5)
    
        # Display customizable text in the bottom-right corner
        custom_font = pygame.font.Font(None, 100)  # You can change the font size
        custom_text_surface = custom_font.render(clean, True, text_color)
        custom_text_rect = custom_text_surface.get_rect(center=(screen.get_width() * 3 // 4, screen.get_height() * 3 // 4))
        screen.blit(custom_text_surface, custom_text_rect)



    ALARM()
    #Display_Capture
    
    screen.blit(text, text_rect)
    pygame.display.flip()
    #time.sleep(0.5)
    
    
    
pygame.quit()


