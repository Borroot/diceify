from PIL import Image
import numpy as np
import math
import sys

from draw import draw_all
from conv import vectors


def preprocess(file, number_dice):
    """Convert to gray scale and appropriate size."""
    img = Image.open(file)
    img = img.convert('L')  # grey scale

    scale = math.sqrt(number_dice / (img.size[0] * img.size[1]))
    width  = int(img.size[0] * scale)
    height = int(img.size[1] * scale)
    img = img.resize((width, height))

    # img.show()
    return np.array(img)  # 2d grid


def diceify_grid(grid):
    """Convert the grid to dice numbers."""
    domain = grid.max() - grid.min()
    step = domain / 6

    tonumber = lambda value: min(i for i in range(1, 7) if value <= grid.min() + i * step)
    newgrid = np.empty(shape = grid.shape)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            newgrid[y][x] = tonumber(grid[y][x])

    return newgrid


def diceify(filename, number_dice, dice_size = 100):
    # create the gray scale grid, the dice grid and the vectors grid
    grid = preprocess(filename, number_dice)
    grid_dice = diceify_grid(grid)
    grid_vectors = vectors(grid)

    # create an image to draw the dice on
    img = draw_all(grid_dice, grid_vectors, dice_size)
    img.show()
    img.save("dice.png")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'usage: python {sys.argv[0]} <img.png> <num_dice>')
        sys.exit()

    filename = sys.argv[1]
    number_dice = int(sys.argv[2])

    diceify(filename, number_dice)
