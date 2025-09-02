import numpy as np
from physics.motion import acceleration, velocity
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# loop for animation
def simulate_orbit(r0, T, dt):
    r = np.array(r0)
    v = velocity(r)
    positions = []

    for _ in range(int(T / dt)):
        positions.append(r.copy())
        a = acceleration(r)
        r = r + v * dt
        v = v + a * dt

    return np.array(positions)


def plot_orbit(positions):
    plt.figure(figsize=(6, 6))
    plt.plot(positions[:, 0], positions[:, 1])
    plt.plot(0, 0, "ro", label="Planet")
    plt.axis("equal")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Orbit Path")
    plt.grid(True)
    plt.legend()
    plt.show()


def animate_orbit(positions, interval=20):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Orbit Animation")

    (line,) = ax.plot([], [], lw=1)
    (point,) = ax.plot([], [], "bo")
    (planet,) = ax.plot(0, 0, "ro", markersize=8)

    def init():
        ax.set_xlim(min(positions[:, 0]), max(positions[:, 0]))
        ax.set_ylim(min(positions[:, 1]), max(positions[:, 1]))
        line.set_data([], [])
        point.set_data([], [])
        return line, point

    def update(frame):
        line.set_data(positions[:frame, 0], positions[:frame, 1])
        point.set_data(positions[frame, 0], positions[frame, 1])
        return line, point

    ani = animation.FuncAnimation(
        fig, update, frames=len(positions), init_func=init, blit=True, interval=interval
    )
    plt.show()
