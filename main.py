import pygame as pg
import random

WINSIZE = [1280, 1280]
CELL_WIDTH = WINSIZE [0]/10
CELL_LENGTH = WINSIZE [1]/10

def find_mimes(grid, coordinate):
    # getting index
    row = coordinate[0]
    col = coordinate[1]

    # checking col
    mime_count = 0

    for (row, col) in find_neighbor_mimes(coordinate):
        if grid[row][col]['bomb']:
            mime_count += 1

    return mime_count

def find_neighbor_mimes(coordinates):
    row = coordinates[0]
    col = coordinates[1]

    # check top row
    if row != 0:
        # checking top middle
        yield (row - 1, col)
        # checking top left
        if col != 0:
            yield (row - 1, col - 1)
        # checking top right
        if col != 9:
            yield (row - 1, col + 1)

    # check bottom row
    if row != 9:
        # checking bottom middle
        yield (row + 1, col)
        # checking bottom left
        if col != 0:
            yield (row + 1, col - 1)
        # checking bottom right
        if col != 9:
            yield (row + 1, col + 1)

    # checking left/right
    if col != 0:
        yield (row, col - 1)
    if col != 9:
        yield (row, col + 1)

def place_mines(difficulty):
    # difficulty assignment
    dif_map = {'easy': 0.10,
               'medium': 0.20,
               'hard': 0.30}
    game_dif = dif_map[difficulty]

    # building probability
    population = [True, False]
    weights = [game_dif, 1 - game_dif]

    # building grid
    mine_list = []
    for row in range(10):
        row_list = []
        for col in range(10):
            choice = random.choices(population, weights)
            row_list.append({
                'bomb': choice [0], 
                'cover': True 
            })

        mine_list.append(row_list)

    return mine_list

def clear_zero_mimes(field, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    if find_mimes(field, coordinates) == 0:
        for reveal in find_neighbor_mimes(coordinates):
            if not field[reveal[0]][reveal[1]]['cover']:
                continue
            field[reveal[0]][reveal[1]]['cover'] = False
            clear_zero_mimes(field, reveal)

def reveal_all(field):
    for row in field:
        for col in row:
            col['cover'] = False

def mine(surface,field, font, game_over, bomb_img):
    for (row, lims) in enumerate(field):
        for (col, cell) in enumerate(lims):
            x = col*CELL_WIDTH
            y= row*CELL_LENGTH
            padding = 5
            if cell['bomb'] and not cell['cover']:
                color = 255, 0, 0
            else:
                color = 255, 255, 255
            rect = pg.Rect((x + padding, y + padding), (CELL_WIDTH - 2*padding, CELL_LENGTH - 2*padding ))
            pg.draw.rect(surface, (color), rect)
            
            if not cell['cover'] and not cell['bomb']:
                mimes = find_mimes(field, (row, col))
                text = font.render (str(mimes), False, (0, 0, 0))
                text_rect = text.get_rect(center=(x + CELL_WIDTH / 2, y + CELL_LENGTH / 2))
                surface.blit (text, text_rect)
            if not cell['cover'] and cell['bomb']:
                img = pg.transform.scale(bomb_img, (rect.width, rect.height))
                surface.blit(img, rect)

def main():
    pg.init()
    pg.font.init()
    font = pg.font.SysFont ('Comic Sans MS', 150)
    screen = pg.display.set_mode(WINSIZE)

    pg.display.set_caption("Minesweeper")
    black = 20, 20, 40
    screen.fill(black)

    bomb_img = pg.image.load('bomb.png')

    clock = pg.time.Clock()
    field = place_mines ("easy")
    # main game loop
    done = 0
    game_over = False
    while not done:
        mine(screen,field, font, game_over, bomb_img)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            if e.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                x = int(pos[0] / CELL_WIDTH)
                y = int(pos[1] / CELL_LENGTH)
                if not game_over:
                    field[y][x]["cover"] = False
                    clear_zero_mimes(field, (y, x))
                    if field[y][x]["bomb"]:
                        reveal_all(field)
                        game_over = True
        clock.tick(50)
    pg.quit()

if __name__ == '__main__':
    main()