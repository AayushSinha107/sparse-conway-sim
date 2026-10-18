# Handling imports
import random
from collections import Counter
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
        self.alive_cells = set()

        # generating a random initial state
        for i in range(self.size):
            for j in range(self.size):
                r = random.randint(0, 100)
                if r <= 20:
                    self.alive_cells.add((i, j))
                else:
                    continue

    # function to count neighbours
    def neighbour_count(self):
        count = Counter()
        for x, y in self.alive_cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    count[((x + dx) % self.size, (y + dy) % self.size)] += 1

        return count

    # update the universe grid with next generation rules
    def update_matrix(self, n=1):
        for _ in range(n):
            next_gen = set()
            count = self.neighbour_count()
            for coord, neighbour in count.items():
                if neighbour == 3:
                    next_gen.add(coord)
                elif neighbour == 2 and coord in self.alive_cells:
                    next_gen.add(coord)
            self.alive_cells = next_gen


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
        for x, y in universe.alive_cells:
            x0 = y * CELL_SIZE
            y0 = x * CELL_SIZE
            draw.rectangle([x0, y0, x0 + CELL_SIZE, y0 + CELL_SIZE], fill="lime")

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