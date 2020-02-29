import tkinter as tk
import random
import math as m

# Parameters
G = 9.81


class Pendulum():
    def __init__(self, theta: float, theta_dot: float,
                 mass: float, length: float,
                 width: int = 3):
        """Creates a Pendulum with a given position, velocity, length and mass.
        width represent the width of the rope of the pendulum.
        The size of the pendulum is proportional to its mass."""

        self.theta = theta
        self.theta_dot = theta_dot
        self.mass = mass
        self.length = length
        self.width = width


class App(tk.Tk):
    def __init__(self,
                 pendulum_1: Pendulum, pendulum_2: Pendulum,
                 width: int = 600, height: int = 600,
                 offset_width: int = 300, offset_height: int = 120,
                 dt: float = 0.05):
        """Initialize the widget for the double pendulum animation.

        offset_width and offset_height represent the x and y offsets from the
        top left corner of the canvas to place the first pendulum."""

        # Setting attributes
        self.width = width
        self.height = height
        self.offset_width = offset_width
        self.offset_height = offset_height
        self.dt = dt
        self.pendulum_1 = pendulum_1
        self.pendulum_2 = pendulum_2
        self.trace_coords = []

        # Setting canvas widget
        tk.Tk.__init__(self)
        self.title("Double Pendulum")
        self.canvas = tk.Canvas(self,
                                width=self.width, height=self.height)
        self.canvas.pack(side="top")

        # Action
        self.after(1, self.draw_frame)

    def update_pendulums_positions(self):
        """Update the angle positions and velocities of the two pendulums"""

        # Dealing with the first pendulum equation of motion
        num_1 = -G * (2 * self.pendulum_1.mass + self.pendulum_2.mass)
        num_1 *= m.sin(self.pendulum_1.theta)

        num_2 = -self.pendulum_2.mass * G
        num_2 *= m.sin(
            self.pendulum_1.theta -
            2 * self.pendulum_2.theta
        )

        num_3 = -2 * m.sin(self.pendulum_1.theta-self.pendulum_2.theta)
        num_3 *= self.pendulum_2.mass
        num_3 *= (
            self.pendulum_2.theta_dot**2 * self.pendulum_2.length +
            self.pendulum_1.theta_dot**2 * self.pendulum_1.length *
            m.cos(
                self.pendulum_1.theta -
                self.pendulum_2.theta
            )
        )

        denom_1 = self.pendulum_1.length * (
            2 * self.pendulum_1.mass +
            self.pendulum_2.mass -
            self.pendulum_2.mass *
            m.cos(
                2 * self.pendulum_1.theta -
                2 * self.pendulum_2.theta
            )
        )

        # Dealing with the second pendulum equation of motion

        num_4 = 2 * m.sin(self.pendulum_1.theta - self.pendulum_2.theta)

        num_5 = (
            self.pendulum_1.theta_dot**2 *
            self.pendulum_1.length *
            (self.pendulum_1.mass + self.pendulum_2.mass)
        )

        num_6 = G * (self.pendulum_1.mass + self.pendulum_2.mass)
        num_6 *= m.cos(self.pendulum_1.theta)

        num_7 = self.pendulum_2.theta_dot**2 * self.pendulum_2.length
        num_7 *= self.pendulum_2.mass * m.cos(
            self.pendulum_1.theta -
            self.pendulum_2.theta
        )

        denom_2 = self.pendulum_2.length * (
            2 * self.pendulum_1.mass +
            self.pendulum_2.mass -
            self.pendulum_2.mass *
            m.cos(
                2 * self.pendulum_1.theta -
                2 * self.pendulum_2.theta
            )
        )

        # Compute the accelerations
        theta1_dotdot = (num_1 + num_2 + num_3) / denom_1
        theta2_dotdot = (num_4*(num_5+num_6+num_7)) / denom_2

        # Update the velocities and positions
        self.pendulum_1.theta_dot += theta1_dotdot * self.dt
        self.pendulum_1.theta += self.pendulum_1.theta_dot * self.dt
        self.pendulum_2.theta_dot += theta2_dotdot * self.dt
        self.pendulum_2.theta += self.pendulum_2.theta_dot * self.dt

    def draw_pendulums(self):
        """Draw the two pendulums and the trace"""

        # Cartesian coordinates
        x1 = self.pendulum_1.length * m.sin(self.pendulum_1.theta)
        y1 = self.pendulum_1.length * m.cos(self.pendulum_1.theta)

        x2 = x1 + self.pendulum_2.length * m.sin(self.pendulum_2.theta)
        y2 = y1 + self.pendulum_2.length * m.cos(self.pendulum_2.theta)

        # Update the trace of the second pendulum
        self.trace_coords.append(
            (
                self.offset_width + x2,
                self.offset_height + y2,
                self.offset_width + x2,
                self.offset_height + y2
            )
        )

        # Draw the trace
        self.canvas.create_line(self.trace_coords, fill='black', tag='trace')

        # Draw the first pendulum
        self.canvas.create_line(
            self.offset_width, self.offset_height,
            self.offset_width + x1, self.offset_height + y1,
            width=self.pendulum_1.width, fill='pink', tags='pendulum'
        )
        self.canvas.create_oval(
            self.offset_width - self.pendulum_1.mass + x1,
            self.offset_height - self.pendulum_1.mass + y1,
            self.offset_width + self.pendulum_1.mass + x1,
            self.offset_height + self.pendulum_1.mass + y1,
            fill='pink', outline='pink', tags='pendulum'
        )

        # Draw the second pendulum
        self.canvas.create_line(
            self.offset_width + x1, self.offset_height + y1,
            self.offset_width + x2, self.offset_height + y2,
            width=self.pendulum_2.width, fill='pink', tags='pendulum'
        )
        self.canvas.create_oval(
            self.offset_width - self.pendulum_2.mass + x2,
            self.offset_height - self.pendulum_2.mass + y2,
            self.offset_width + self.pendulum_2.mass + x2,
            self.offset_height + self.pendulum_2.mass + y2,
            fill='pink', outline='pink', tags='pendulum'
        )

    def draw_frame(self):
        """Draw the current frame"""

        # Delete objects on the canvas to redraw
        self.canvas.delete('trace')
        self.canvas.delete('pendulum')

        # Update the positions and draw the frame
        self.update_pendulums_positions()
        self.draw_pendulums()

        # Repeat
        self.after(1, self.draw_frame)


if __name__ == '__main__':

    # Initialization of the two pendulums
    theta1 = random.random() * 2 * m.pi
    theta2 = random.random() * 2 * m.pi

    pendulum_1_parameters = {
        "theta": theta1,
        "theta_dot": 0,
        "mass": 10,
        "length": 100,
        "width": 3
    }
    pendulum_2_parameters = {
        "theta": theta2,
        "theta_dot": 0,
        "mass": 10,
        "length": 100,
        "width": 3
    }

    pendulum_1 = Pendulum(**pendulum_1_parameters)
    pendulum_2 = Pendulum(**pendulum_2_parameters)

    # Run the animation
    animation_parameters = {
        "pendulum_1": pendulum_1,
        "pendulum_2": pendulum_2,
        "width": 600,
        "height": 600,
        "offset_width": 300,
        "offset_height": 150,
        "dt": 0.05
    }
    app = App(**animation_parameters)
    app.mainloop()
