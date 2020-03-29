# made by Artur Dorovskikh 2020-03-26
# v0.3 2020-03-29

# reference article for input lag: https://forums.blurbusters.com/viewtopic.php?t=3780

# TODO test on crt min input, set as 0ms, test other monitors
# TODO add calculation to arduino serial latency, subtract it, use pressure version to calculate
# TODO check crashes after a few seconds on xps

# TODO USE PROFILER to optimize pygame fps from 300 to 1000
# TODO save ms latency data to a csv file for analysis

import sys
import pygame
import ctypes
import serial # for getting data from arduino
# to fix not importing serial use: pip install --upgrade --force-reinstall pyserial

ser = serial.Serial('COM3', 9600) # Establish the connection on a specific port

pygame.init()
ctypes.windll.user32.SetProcessDPIAware() # disables windows scaling for this app

hz = 144 # TODO get monitor refresh rate

pygame.display.set_caption('Input Lag Test')
font = pygame.font.Font('freesansbold.ttf', 64)

c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_red = (255, 0, 0)
c_green = (0, 255, 0)
c_blue = (0, 0, 255)

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

width_half, height_half = width // 2, height // 2
scale = 150 # square scale
clock = pygame.time.Clock()
fps = 1000 #TODO fps matching screen or 1000, 144 not drawing squares sometimes

def draw_squares(color):
    # draw 3 squares, one top left, one middle left, one bottom left for the various lag measurements
    pygame.draw.rect(screen, color, (0, 0, scale, scale)) # left top
    pygame.draw.rect(screen, color, (0, height/2 - scale/2, scale, scale)) # left middle
    pygame.draw.rect(screen, color, (0, height - scale, scale, scale)) # left bottom
    # pygame.display.flip()

def draw_text(text, color, color_back, x, y):
    text = font.render(text, True, color, color_back)
    textRect = text.get_rect()
    textRect.midleft = (x, y)
    screen.blit(text, textRect)
    # pygame.display.flip()

def main():
    wait_reading_squares = 0
    screen.fill(c_black)
    # pygame.display.flip()
    # draw_squares(c_white)

    # TODO USE DICTIONARY TO STORE ALL LATENCY data and to calculate min max
    array = {} # to keep track of the ms
    # array.setdefault(0)
    array_index = 0
    draw_tick = False # to keep track of each frame, shows white square every other frame
    show_counter = 0
    counter_hz = 1 # to keep track of the hz

    ms_max = 0
    ms_min = 1000
    flash_signal_recieved = False

    ser.flushInput()
    while True:
        if wait_reading_squares > 1:
            wait_reading_squares -= 1
        else:
            draw_squares(c_black)
            wait_reading_squares = 0

        # if wait_reading_squares == True:
        #     draw_squares(c_black)
        #     wait_reading_squares = False

        try:
            ser.write(str.encode())
        except:
            pass

        # TODO USE FLUSH TO REMOVE LATENCY, but doing so breaks serial reading
        # ser.flushInput() # to disable buffer to improve latency
        sensor = str(ser.readline())[2:-5]

        if sensor == "w":
            pass
        elif sensor == "f":
            if flash_signal_recieved == False:
                # print(str(array_index) + ": " + str(array.get(array_index-1)))
                # TODO CHAGNE TO REFRESH SCREEN ONLY ON BLACK/WHITE
                # TODO show several text lines upon refresh
                draw_squares(c_white)
                wait_reading_squares = round(fps/hz) # TODO: change number to only show one image for a refresh, not several
                # print(round(fps/hz))
                flash_signal_recieved = True
        else:
            # print("recieved ms " + sensor) #TODO prints 3 at a time, but in between array index
            flash_signal_recieved = False
            array[array_index] = int(sensor) # add value to recent
            # print(array.get(array_index))
            # print(array)
            array_index += 1
            # print(str(array_index)) #TODO why is arrayindex being added 3 times at a time????
            # array(None) = 0

            if array_index > 30: # get last 10 values only if past 10 iterations
                ms_max = 0
                ms_min = 1000
                for i in range(30): #TODO array not being counted properly
                    # print(" array - i " + str(array_index - i), end = '')
                    key = array.get(array_index - i - 1)
                    # print("i:"+str(i))
                    # print(key)
                    if key is not None:
                        if key > ms_max:
                            ms_max = key
                        if key < ms_min:
                            ms_min = key
                # print("max = " + str(ms_max) + " min = " + str(ms_min))
                # print(array)
            print("ms: " + str(array.get(array_index-1)) + " min: " + str(ms_min) + " max: " + str(ms_max) + " | fps: " + str(round(clock.get_fps())))

        #TODO add alternating left right rectangle to see better
        if draw_tick == True and show_counter == round(fps/hz): #TODO stuttering, fix so that every other
            pygame.draw.rect(screen, c_red, (width/3, height/3, scale/4, scale/4))
            draw_tick = False
            show_counter = 0
        else:
            pygame.draw.rect(screen, c_blue, (width/3, height/3, scale/4, scale/4))

            draw_tick = True
            show_counter += 1

        draw_text(str(counter_hz) + " / " + str(hz) + "  ", c_white, c_black, width_half-100, height_half-100)

        # TODO change to monospaced font= https://www.reddit.com/r/pygame/comments/278sfa/load_font_which_is_not_a_standard_font/
        # TODO: also show screen resolution and refresh rate, display lag (crt zero calibrated),  and total measured ms lag
        draw_text("ms: " + str(array.get(array_index-1)) + " min: " + str(ms_min) + " max: " + str(ms_max) + " | fps: " + str(round(clock.get_fps())) + "    ", c_white, c_black, width_half/2, height_half) # + " tick: " + str(pygame.time.get_ticks())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_squares(c_white)
                wait_reading_squares = round(fps/hz) # TODO: change number to only show one image for a refresh, not several
                # print(round(fps/hz))
                flash_signal_recieved = True
            if event.type == pygame.MOUSEBUTTONUP:
                draw_squares(c_black)
        clock.tick(fps)
        counter_hz = (counter_hz + 1) % hz
        pygame.display.flip()
main()
