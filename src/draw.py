from PIL import Image, ImageDraw


def dots(x, y, number, vx, vy, dice_size):
    return [
        # one
        [
            [(x + dice_size // 2, y + dice_size // 2)],
        ],
        # two
        [
            # top left to bot right
            [(x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],

            # top right to bot left
            [(x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1)],
        ],
        # three
        [
            # top left to bot right
            [(x + dice_size // 2,     y + dice_size // 2),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],

            # top right to bot left
            [(x + dice_size // 2,     y + dice_size // 2),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1)],
        ],
        # four
        [
            [(x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],
        ],
        # five
        [
            [(x + dice_size // 2,     y + dice_size // 2),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],
        ],
        # six
        [
            # horizontal
            [(x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 2, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 2, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],

            # vertical
            [(x + dice_size // 4 * 1, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 3),
             (x + dice_size // 4 * 1, y + dice_size // 4 * 2),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 2),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 1),
             (x + dice_size // 4 * 3, y + dice_size // 4 * 3)],
        ],
    ][number - 1][version(number, vx, vy)]


def version(number, vx, vy):
    """Determine which version of the number to draw based on the vectors."""
    if number == 1 or number == 4 or number == 5:
        return 0
    if number == 6:
        return 0 if abs(vx) > abs(vy) else 1

    if (vx > 0 and vy > 0) or (vx < 0 and vy < 0):
        return 0
    return 1


def draw_dot(draw, x, y):
    """Draw one dot at the given location."""
    dot_size = 10
    draw.ellipse((x - dot_size, y - dot_size, x + dot_size, y + dot_size),
        fill = (0, 0, 0))


def draw_dice(draw, x, y, number, vx, vy, dice_size):
    """Draw the provided dice number at the given location and oriented
    according to the direction vectors."""

    x = dice_size * x
    y = dice_size * y

    draw.rectangle((x, y, x + dice_size, y + dice_size),
        fill = (255, 255, 255), outline = (0, 0, 0))

    for x, y in dots(x, y, number, vx, vy, dice_size):
        draw_dot(draw, x, y)


def draw_all(grid_dice, grid_vectors, dice_size):
    size = (dice_size * grid_dice.shape[1], dice_size * grid_dice.shape[0])
    img = Image.new('RGB', size, (125, 125, 125))
    draw = ImageDraw.Draw(img)

    for y in range(len(grid_dice)):
        for x in range(len(grid_dice[y])):
            draw_dice(draw, x, y, int(grid_dice[y][x]), *grid_vectors[y][x], dice_size)

    return img
