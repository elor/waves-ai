import pygame
import numpy as np
import matplotlib.cm

# Define the size of the square pond
size = (400, 400)
pond = np.zeros(size)

# Define the wave speed
c = 200.0

# Define the frames per second and calculate the time step
fps = 120
dt = 1 / (fps * 10)  # Perform 10 time steps per frame

# Define the spatial step and the square of the spatial step
dx = 1.0
dx2 = dx * dx

# Initialize the new pond configuration
new_pond = np.zeros(size)

# Initialize Pygame
pygame.init()

# Set the size of the window
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Wave Simulation")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Pre-calculate the constant term
constant_term = (c * dt / dx) ** 2

floating_minmax = 0.0


def lerp(a, b, t):
    return a + (b - a) * t


# -------- Main Program Loop -----------
while True:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = int(x)
            y = int(y)
            pond[x, y] = 1.0

    # Perform multiple time steps per frame
    for _ in range(10):
        # --- Game logic should go here
        new_pond[1:-1, 1:-1] = (
            2 * pond[1:-1, 1:-1]
            - new_pond[1:-1, 1:-1]
            + constant_term
            * (
                pond[2:, 1:-1]
                + pond[:-2, 1:-1]
                + pond[1:-1, 2:]
                + pond[1:-1, :-2]
                - 4 * pond[1:-1, 1:-1]
            )
        )

        # Swap new pond and old pond
        pond, new_pond = new_pond, pond

    # --- Drawing code should go here
    # Apply the red-black-blue colormap
    pond_min = pond.min()
    pond_max = pond.max()
    pond_minmax = max(1e-1, max(abs(pond_min), abs(pond_max)))

    floating_minmax = lerp(floating_minmax, pond_minmax, 0.01)

    colored_pond = (
        matplotlib.cm.bwr((pond + floating_minmax) / 2 / floating_minmax)[:, :, :3]
        * 255
    )
    colored_pond = colored_pond.astype(np.uint8)

    # print(f"Minimum: {pond.min()}, Maximum: {pond.max()}")

    # Update the pixels of the screen
    pygame.surfarray.blit_array(screen, colored_pond)

    # --- Go ahead and update the screen with what we've drawn
    pygame.display.flip()

    # --- Limit to the desired frames per second
    clock.tick(fps)
