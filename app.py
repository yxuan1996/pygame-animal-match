import pygame
import game_config as gc

from pygame import display, event, image
from time import sleep
from animal import Animal

def find_index_from_xy(x, y):
    row = y // gc.IMAGE_SIZE
    col = x // gc.IMAGE_SIZE
    index = row * gc.NUM_TILES_SIDE + col
    return row, col, index

pygame.init()
display.set_caption('My Game')

#create game window
screen = display.set_mode((gc.SCREEN_SIZE, gc.SCREEN_SIZE))

#Load the matched image
matched = image.load('other_assets/matched.png')

running = True

#Instantiate all animal tiles
tiles = [Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]
current_images_displayed = []

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
            row, col, index = find_index_from_xy(mouse_x, mouse_y)
            if index not in current_images_displayed:
                #2 pictures displayed
                #we refresh the screen to display the clicked tile and the previously clicked tile
                if len(current_images_displayed) > 1:
                    current_images_displayed = current_images_displayed[1:] + [index]
                else:
                    current_images_displayed.append(index)

    screen.fill((255, 255, 255))

    total_skipped = 0

    for i, tile in enumerate(tiles):
        #selected imgaes are soted in current_images_displayed
        #we only display 2 images at one time and hide the other images using tile.box
        current_image = tile.image if i in current_images_displayed else tile.box

        #screen.blit() overlays images on SCREEN
        #Images that have already been matched will be skipped
        if not tile.skip:
            screen.blit(current_image, (tile.col * gc.IMAGE_SIZE + gc.MARGIN, tile.row * gc.IMAGE_SIZE + gc.MARGIN))
        else:
            total_skipped += 1

    display.flip()

    # Remove images if they match
    if len(current_images_displayed) == 2:
        idx1, idx2 = current_images_displayed
        if tiles[idx1].name == tiles[idx2].name:
            tiles[idx1].skip = True
            tiles[idx2].skip = True
            # display matched message
            sleep(0.2)
            screen.blit(matched, (0, 0))
            display.flip()
            sleep(0.5)
            #Reset current_images
            current_images_displayed = []

    #If all tiles are skipped, then game is complete
    if total_skipped == len(tiles):
        running = False

print('Goodbye!')
