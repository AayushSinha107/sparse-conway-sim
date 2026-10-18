# Handling imports
import random
from PIL import Image, ImageDraw


# Defining Universe Grid Class
class UniverseGrid:

    # a lookup list to know how to reach the neighbour
    neighbour_loc = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, -1),
        (-1, 1),
    ]

    # initialize the class with default 32x32 size or user entered value
    def __init__(self, size=32):
        self.size = size
        self.universe_matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

        # generating a random initial state
        for row in self.universe_matrix:
            for i in range(self.size):
                r = random.random()
                if r <= 0.2:
                    row[i] = 1
                else:
                    continue

    # function to count neighbours
    def neighbour_count(self, i, j):
        count = 0
        for neighbour in self.neighbour_loc:
            new_x = (i + neighbour[0]) % self.size
            new_y = (j + neighbour[1]) % self.size
            if self.universe_matrix[new_x][new_y] == 1:
                count += 1
        return count

    # update the universe grid with next generation rules
    def update_matrix(self, n=1):
        for _ in range(n):
            next_gen = [[0 for _ in range(self.size)] for _ in range(self.size)]
            for i in range(self.size):
                for j in range(self.size):
                    if self.universe_matrix[i][j] == 1 and self.neighbour_count(
                        i, j
                    ) in [2, 3]:
                        next_gen[i][j] = 1
                    elif (
                        self.universe_matrix[i][j] == 0
                        and self.neighbour_count(i, j) == 3
                    ):
                        next_gen[i][j] = 1
            self.universe_matrix = next_gen


if __name__ == "__main__":
    print("Creating the universe...")
    universe = UniverseGrid(size=128)

    frames = []
    CELL_SIZE = 10  # Each grid cell becomes a 10x10 pixel square
    GENERATIONS = 1000  # How many frames to simulate

    print(f"Simulating {GENERATIONS} generations...")
    for _ in range(GENERATIONS):
        # Create a blank black canvas (320x320 pixels)
        img = Image.new(
            "RGB", (universe.size * CELL_SIZE, universe.size * CELL_SIZE), "black"
        )
        draw = ImageDraw.Draw(img)

        # Draw the alive cells
        for i in range(universe.size):
            for j in range(universe.size):
                if universe.universe_matrix[i][j] == 1:
                    # Calculate the pixel corners for this cell
                    x0 = j * CELL_SIZE
                    y0 = i * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE

                    # Draw a lime green square
                    draw.rectangle([x0, y0, x1, y1], fill="lime")

        # Save this frame to our history list
        frames.append(img)

        # Advance the simulation by 1 generation
        universe.update_matrix(1)

    print("Stitching frames and saving GIF...")
    # Save the list of images as an animated GIF
    frames[0].save(
        "simulation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Speed: 100 milliseconds per frame
        loop=0,  # 0 means loop forever
    )
    print("Done! Check your folder for simulation.gif.")
