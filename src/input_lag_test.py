# Made by Artur Dorovskikh
# This app changes the screen to white from black on mouse click, then back to black after mouse release
# v0.2 2020-03-13

# reference article for input lag: https://forums.blurbusters.com/viewtopic.php?t=3780

import sys
import pygame
import ctypes
# from time import sleep
import serial # for getting data from arduino, # to fix not importing serial use: pip install --upgrade --force-reinstall pyserial

ser = serial.Serial('COM3', 9600) # Establish the connection on a specific port

pygame.init()
ctypes.windll.user32.SetProcessDPIAware() # disables windows scaling for this app
# TODO: make borderless fulscreen so leaving app does not minimize it for more than one monitor systems, for when running windas and connecting the crt on the same computer 

hz = 60 # TODO get monitor refresh rate

pygame.display.set_caption('Input Lag Test') 
font = pygame.font.Font('freesansbold.ttf', 32) 

c_white = (255, 255, 255)
c_black = (0, 0, 0)

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

width_half, height_half = width // 2, height // 2
scale = 150 # square scale
clock = pygame.time.Clock()
fps = 1000

stack = [] # to keep track of the ms

# TODO pull ms latency data from arduino
# TODO draw last 10 average measured ms latency data on screen bottom right
# TODO save ms latency data to a csv file for analysis

def draw_squares(color):
    # draw 3 squares, one top left, one middle left, one bottom left for the various lag measurements
    pygame.draw.rect(screen, color, (0, 0, scale, scale)) # left top
    pygame.draw.rect(screen, color, (0, height/2 - scale/2, scale, scale)) # left middle
    pygame.draw.rect(screen, color, (0, height - scale, scale, scale)) # left bottom
    pygame.display.flip()
    
def draw_text(text, color, color_back, x, y):
    text = font.render(text, True, color, color_back) 
    textRect = text.get_rect()
    textRect.midleft = (x, y)
    screen.blit(text, textRect)
    pygame.display.flip()

def main():
    wait_reading_squares = 0
    screen.fill(c_black)
    pygame.display.flip()
    # draw_squares(c_white)

    ser.flushInput()
    while True:
        if wait_reading_squares > 1:
            wait_reading_squares -= 1
        else:
            draw_squares(c_black)
            wait_reading_squares = 0

        # TODO USE FLUSH TO REMOVE LATENCY, but doing so breaks serial reading
        # ser.flushInput() # to disable buffer to improve latency
        
        try:
            # ser.write(str.encode('allon')) # ?crashes app after a few seconds
            ser.write(str.encode())
        except:
            pass
        
        sensor = str(ser.readline())[2:-5]

        if sensor == "w":
            # TODO CHAGNE TO REFRESH SCREEN ONLY ON BLACK/WHITE
            # TODO show several text lines upon refresh
            draw_squares(c_white)
            wait_reading_squares = 10 # TODO: change number to only show one image for a refresh, not several

        # TODO change to monospaced font= https://www.reddit.com/r/pygame/comments/278sfa/load_font_which_is_not_a_standard_font/
        draw_text("latency: " + sensor + "ms | fps: " + str(round(clock.get_fps())) + " ", c_white, c_black, width_half, height_half) # + " tick: " + str(pygame.time.get_ticks())
        # TODO: also show screen resolution and refresh rate, display lag (crt zero calibrated),  and total measured ms lag

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_LSHIFT:
                    draw_squares(c_white)
                    # print(ser)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    draw_squares(c_black)

main()
