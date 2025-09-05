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
    plt.plot(0, 0, "ro", label="Planet")
    plt.axis("equal")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Orbit Path")
    plt.legend()
    plt.show()


def animate_orbit(positions, interval=20):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("Orbit Animation")

    (line,) = ax.plot([], [], lw=1)
    (point,) = ax.plot(
        [],
        [],
        "ro",
    )
    satellite_label = ax.text(
        positions[0, 0],
        positions[0, 1],
        " Satellite",
        color="white",
        fontsize=10,
        ha="left",
        va="bottom",
    )
    ax.plot(0, 0, "bo", markersize=10, label="Earth")  # blue Earth
    ax.text(0, 0, " Earth", color="white", fontsize=10, ha="left", va="bottom")

    def init():
        max_range = np.max(np.abs(positions))
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect("equal", adjustable="box")
        line.set_data([], [])
        point.set_data([], [])
        satellite_label.set_position((positions[0, 0], positions[0, 1]))
        return line, point, satellite_label

    def update(frame):
        line.set_data(positions[:frame, 0], positions[:frame, 1])
        point.set_data([positions[frame, 0]], [positions[frame, 1]])
        satellite_label.set_position((positions[frame, 0], positions[frame, 1]))
        return line, point, satellite_label

    ani = animation.FuncAnimation(
        fig, update, frames=len(positions), init_func=init, blit=True, interval=interval
    )
    plt.show()
