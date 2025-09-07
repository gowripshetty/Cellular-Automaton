import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio
import os

# ===============================
# Setup project directories
# ===============================
os.makedirs('docs', exist_ok=True)
os.makedirs('results', exist_ok=True)

# ===============================
# Parameters
# ===============================
GRID_SIZE = 50          # Grid is GRID_SIZE x GRID_SIZE
ALIVE_PROB = 0.2        # Probability a cell starts alive
GENERATIONS = 100       # Number of iterations
INTERVAL = 200          # Time between frames (ms)

# Initialize grid randomly
grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[1-ALIVE_PROB, ALIVE_PROB])

# ===============================
# Update function for animation
# ===============================
def update(frameNum, img, grid, frames_list):
    newGrid = grid.copy()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Count alive neighbors
            total = int((
                grid[i, (j-1)%GRID_SIZE] + grid[i, (j+1)%GRID_SIZE] +
                grid[(i-1)%GRID_SIZE, j] + grid[(i+1)%GRID_SIZE, j] +
                grid[(i-1)%GRID_SIZE, (j-1)%GRID_SIZE] + grid[(i-1)%GRID_SIZE, (j+1)%GRID_SIZE] +
                grid[(i+1)%GRID_SIZE, (j-1)%GRID_SIZE] + grid[(i+1)%GRID_SIZE, (j+1)%GRID_SIZE]
            ))

            # Apply Conway's rules
            if grid[i, j] == 1:
                if total < 2 or total > 3:
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 1

    img.set_data(newGrid)
    grid[:] = newGrid[:]

    # Save frames for GIF
    if frameNum % 5 == 0:  # Save every 5th frame
        frames_list.append(newGrid.copy())

    return img,

# ===============================
# Visualization & Animation
# ===============================
frames_list = []

fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='binary')
ax.set_title("Conway's Game of Life")

ani = animation.FuncAnimation(fig, update, fargs=(img, grid, frames_list),
                              frames=GENERATIONS, interval=INTERVAL, save_count=50)


# Save final snapshot
final_snapshot = 'docs/sample_simulation.png'
plt.imsave(final_snapshot, grid, cmap='binary')

# Save GIF
gif_path = 'docs/simulation.gif'
with imageio.get_writer(gif_path, mode='I', duration=INTERVAL/1000) as writer:
    for f in frames_list:
        writer.append_data((f * 255).astype(np.uint8))

print(f"Simulation snapshot saved at: {final_snapshot}")
print(f"GIF animation saved at: {gif_path}")

# Show animation
plt.show()
