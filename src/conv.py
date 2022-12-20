from PIL import Image
import numpy as np
import sys
import math


kernel_edge_horizontal = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1],
])

kernel_edge_vertical = np.array([
    [-1,  0,  1],
    [-2,  0,  2],
    [-1,  0,  1],
])


def convolute(grid, kernel, scalar = 1):
    """Execute the kernel over the given grid."""
    kernel_height, kernel_width = kernel.shape
    grid_height, grid_width = grid.shape

    assert kernel_height == kernel_width
    assert kernel_height % 2 == 1

    newgrid = np.empty(shape = grid.shape)
    kernel_offset = -(kernel_height - 1) // 2

    for grid_y in range(grid_height):
        for grid_x in range(grid_width):
            accumulator = 0

            for kernel_y in range(kernel_height):
                for kernel_x in range(kernel_width):
                    pixel_y = grid_y + kernel_y + kernel_offset
                    pixel_x = grid_x + kernel_x + kernel_offset

                    if 0 <= pixel_y < grid_height and 0 <= pixel_x < grid_width:
                        accumulator += grid[pixel_y][pixel_x] * kernel[kernel_y][kernel_x]

            newgrid[grid_y][grid_x] = accumulator * scalar

    return np.array(newgrid)


def vectors(grid):
    """Create a grid with all the direction vectors."""
    grid = blur(grid, 5)

    grid_horizontal = convolute(grid, kernel_edge_horizontal)
    grid_vertical = convolute(grid, kernel_edge_vertical)

    grid = [[None] * grid.shape[1] for _ in range(grid.shape[0])]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = (grid_horizontal[y][x], grid_vertical[y][x])

    return np.array(grid)


def edges(grid):
    """Create a grid with all the edges."""
    grid = blur(grid, 5)

    grid_horizontal = convolute(grid, kernel_edge_horizontal)
    grid_vertical = convolute(grid, kernel_edge_vertical)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            grid[y][x] = math.sqrt(grid_horizontal[y][x] ** 2 + grid_vertical[y][x] ** 2)

    return grid


def blur(grid, size):
    """Blur a grid using a kernel of the given size filled with ones."""
    assert size % 2 == 1

    kernel = np.array([[1] * size for _ in range(size)])
    return convolute(grid, kernel, scalar = 1 / (size ** 2))


def image(grid):
    """Convert a given grid to a gray scale image."""
    grid = np.asarray(dtype = np.dtype('uint8'), a = grid)
    img = Image.frombuffer(mode = 'L', size = grid.shape[::-1], data = grid)
    return img


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} <img.png>')
        sys.exit()

    filename = sys.argv[1]

    img = Image.open(filename)
    img = img.convert('L')  # grey scale

    scale = 0.5
    size = (int(img.size[0] * scale), int(img.size[1] * scale))
    img = img.resize(size)

    grid = np.array(img)
    grid = edges(grid)

    img = image(grid)
    img.show()
    img.save('edges.png')
