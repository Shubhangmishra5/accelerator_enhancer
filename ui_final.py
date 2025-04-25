import pygame
import math
import serial
import time

# Initialize pygamep
pygame.init()
ser = serial.Serial('COM13', 115200, timeout=1)
# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame UI")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (30, 30, 30)
LIGHT_BLUE = (173, 216, 230)

font = pygame.font.Font(None, 28)

# System state array
systemSTATE = [0] * 12  # 0: Manual, 1-3: Modes, 4-9: Motors, 10: Current, 11: RPM  
def send_data(data_array):
    """Send a list of integers as a comma-separated string."""
    data_str = ','.join(map(str, data_array)) + '\n'  # Convert array to string and add newline
    ser.write(data_str.encode('utf-8'))  # Send data
    print(f"Sent: {data_str.strip()}")
    time.sleep(0.1)
    receive_data()

def receive_data():
    """Receive data from STM32 and print it."""
    global systemSTATE
    if(ser.in_waiting > 0):
        received = ser.readline().decode('utf-8').strip()  # Read the incoming data
        print(f"Received: {received}")
        new_state = list(map(int, received.split(',')))
        systemSTATE = new_state
        return received
    return None

# Function to draw meters
def draw_meter(x, y, value, label, max_value=100):
    pygame.draw.circle(screen, BLACK, (x, y), 50, 5)
    angle = (value / max_value) * 360  # Convert value to angle (0 to 360 degrees)
    end_x = x + 45 * math.cos(math.radians(angle))
    end_y = y - 45 * math.sin(math.radians(angle))
    pygame.draw.line(screen, RED, (x, y), (end_x, end_y), 3)
    text = font.render(label, True, BLACK)
    screen.blit(text, (x - 25, y + 60))
    value_text = font.render(f"{value:.1f}", True, BLACK)
    screen.blit(value_text, (x - 15, y + 80))

# Main loop
send_data(systemSTATE)
running = True
while running:
    screen.fill(DARK_BLUE)
    
    # Event handling
    # time.sleep(0.1)
    receive_data()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # send_data(systemSTATE)

            # Toggle manual mode
            if 225 <= x <= 375 and 10 <= y <= 50:
                systemSTATE[0] = 1 - systemSTATE[0]
                if systemSTATE[0] == 1:  
                    systemSTATE[1:4] = [0, 0, 0]
                
            
            # Mode selection (only if manual mode is OFF)
            if systemSTATE[0] == 0 and 130 <= x <= 470 and 160 <= y <= 210:
                for i in range(3):
                    if 130 + i * 140 <= x <= 250 + i * 140:
                        systemSTATE[1:4] = [0, 0, 0]
                        systemSTATE[i + 1] = 1-systemSTATE[i+1]
                        
                        
            
            # Toggle motor buttons (only if manual mode is ON)
            if systemSTATE[0] == 1:
                for i in range(6):
                    if 50 + i * 90 <= x <= 130 + i * 90 and 100 <= y <= 140:
                        systemSTATE[4 + i] = 1 - systemSTATE[4 + i]
                        
            print(systemSTATE)
            # send_data(systemSTATE)
            send_data(systemSTATE)
     
            
    
    # Draw manual mode button
    pygame.draw.rect(screen, GREEN if systemSTATE[0] else RED, pygame.Rect(225, 10, 150, 40), border_radius=10)
    screen.blit(font.render("Manual", True, WHITE), (260, 20))
    
    # Draw motor buttons
    for i in range(6):
        color = GREEN if systemSTATE[4 + i] else RED
        pygame.draw.rect(screen, color, pygame.Rect(50 + i * 90, 100, 80, 40), border_radius=10)
        text = font.render(f"M{i+1}", True, WHITE)
        screen.blit(text, (75 + i * 90, 115))
    
    # Draw mode selection buttons
    mode_labels = ["Sports", "Normal", "Eco"]
    for i in range(3):
        color = BLUE if systemSTATE[i + 1] else GRAY
        pygame.draw.rect(screen, color, pygame.Rect(130 + i * 140, 160, 120, 50), border_radius=15)
        text = font.render(mode_labels[i], True, WHITE if systemSTATE[i + 1] else BLACK)
        screen.blit(text, (150 + i * 140, 175))
    
    # Draw meters for Current and RPM
    draw_meter(200, 300, systemSTATE[10], "Current", max_value=50)
    draw_meter(400, 300, systemSTATE[11], "RPM", max_value=100)
    
    pygame.display.flip()

pygame.quit()