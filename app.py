import pygame
import game_config as gc

from pygame import display, event, image
from animal import Animal
from time import sleep

def find_index(x,y):
    row = y//gc.IMAGE_SIZE
    col = x // gc.IMAGE_SIZE
    index = row * gc.NUM_TILES_SIDE + col
    return index

pygame.init()

display.set_caption('My Game')

#create game window
screen = display.set_mode((512,512))

#Load the matched image
matched = image.load('other_assets/matched.png')
#overlays the image on the screen
#screen.blit(matched,(0,0))
#update the display
#display.flip()

running = True

#Instatiate all animal tiles
tiles = [Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]
current_images = []

#Main game loop
while running:
    # list of all keyboard and mouse events
    current_events = event.get()

    for e in current_events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #find the index of the tile that was clicked
            index = find_index(mouse_x, mouse_y)
            #Do not match image to itself
            if index not in current_images:
                current_images.append(index)
            current_images.append(index)
            if len(current_images) > 2:
                current_images = current_images[1:]
            

    screen.fill((255,255,255))

    total_skipped = 0

    for i, tile in enumerate(tiles):
        #selected images are stored in current images
        #we only display 2 images at one time and hide the other images using tile.box
        image_i = tile.image if i in current_images else tile.box

        #Overlays the image on the screen
        #only display images that are not skipped
        if not tile.skip:
            screen.blit(image_i, (tile.col*gc.IMAGE_SIZE +gc.MARGIN, tile.row*gc.IMAGE_SIZE + gc.MARGIN))
        else: 
            total_skipped += 1


    #Remove images if they match
    if len(current_images) == 2:
        idx1,idx2 = current_images
        if tiles[idx1].name == tiles[idx2].name:
            tiles[idx1].skip = True
            tiles[idx2].skip = True
            #Display "Matched"
            sleep(0.4)
            screen.blit(matched,(0,0))
            display.flip()
            sleep(0.4)
            #Reset current images
            current_images = []

    #If all tiles are skipped, then game is complete
    if total_skipped == len(tiles):
        running = False

    display.flip()

print("GoodBye!")