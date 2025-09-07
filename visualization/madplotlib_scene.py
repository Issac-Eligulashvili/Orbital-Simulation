import numpy as np
from physics.motion import acceleration
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from data.constants import v0


# loop for animation
def simulate_orbit(r0, T, dt):
    # Get inital values for the radius and velocity
    r = np.array(r0)
    v = np.array([0, v0])
    positions = []

    for _ in range(int(T / dt)):
        positions.append(
            r.copy()
        )  # append the currnet radius vector to positions for later animaion
        a = acceleration(r)  # old acceleration
        r_new = (
            r + v * dt + 0.5 * a * dt**2
        )  # update the new postion with the guess from the old acceleration
        a_new = acceleration(
            r_new
        )  # get new acceleration with the new guessed position
        v_new = v + 0.5 * (a + a_new) * dt  # calculate new velocity
        # Update the radius and velocity variables
        r = r_new
        v = v_new
    return np.array(positions)


def plot_orbit(positions):
    plt.figure(figsize=(6, 6))
    plt.plot(positions[:, 0], positions[:, 1])
    plt.plot(0, 0, "bo", label="Earth")
    plt.axis("equal")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Orbit Path")
    plt.legend()
    plt.tight_layout(pad=10)
    plt.show()


def animate_orbit(positions, interval=20):
    # Initialize the grid
    fig, ax = plt.subplots(figsize=(6, 6))
    # Set colors
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    # Make it a square
    ax.set_aspect("equal")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Orbit Animation")
    # Initialize the trail of orbit
    (line,) = ax.plot([], [], lw=1, color="white", alpha=0.3)
    # Initialize satellite
    (point,) = ax.plot(
        [],
        [],
        "wo",
    )
    # Initialize satellite label
    satellite_label = ax.text(
        positions[0, 0],
        positions[0, 1],
        " Satellite",
        color="white",
        fontsize=10,
        ha="left",
        va="bottom",
    )
    # Plot earth and its label
    ax.plot(0, 0, "bo", markersize=10, label="Earth")  # blue Earth
    ax.text(0, 0, " Earth", color="white", fontsize=10, ha="left", va="bottom")

    def init():
        # Determine max-range to see how big to make graph
        max_range = np.max(np.abs(positions)) * 1.1
        # Set limits so picture fits within graph
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        # Make aspect ratio 1 so it doesnt stretch
        ax.set_aspect("equal", adjustable="box")
        # Put line and point to empty and put label in 0,0
        line.set_data([], [])
        point.set_data([], [])
        satellite_label.set_position((positions[0, 0], positions[0, 1]))
        return line, point, satellite_label

    def update(frame):
        # Draw line that leads upto point
        line.set_data(positions[:frame, 0], positions[:frame, 1])
        # Move point and label one frame ahead
        point.set_data([positions[frame, 0]], [positions[frame, 1]])
        satellite_label.set_position((positions[frame, 0], positions[frame, 1]))
        return line, point, satellite_label

    # Run animation
    ani = animation.FuncAnimation(
        fig, update, frames=len(positions), init_func=init, blit=True, interval=interval
    )
    plt.show()
