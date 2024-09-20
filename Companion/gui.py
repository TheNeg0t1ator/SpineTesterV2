import tkinter as tk
import math

class userInterface():
    def __init__(self):
        self.root = tk.Tk()
        self.createWindow()
    
    def createWindow(self):
        self.root.title("Spine Tester")
        self.root.geometry("400x400")  # Increase the window size to fit the circle
        self.root.iconbitmap("favicon.ico")
        self.measurement_frame = MeasurementCircle(self.root)  # Create the MeasurementCircle frame
    
    def showWindow(self):
        self.root.mainloop()

class MeasurementCircle(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Create a canvas to draw the circle and arrows
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.circle_radius = 100  # Radius of the circle
        self.center_x = 200  # X-coordinate of the center
        self.center_y = 200  # Y-coordinate of the center

        self.num_arrows = 6  # Default number of arrows
        self.angle_offset = 0  # Starting angle offset

        self.draw_circle()
        self.draw_arrows()

    def draw_circle(self):
        # Draw a circle
        self.canvas.create_oval(self.center_x - self.circle_radius, self.center_y - self.circle_radius,
                                self.center_x + self.circle_radius, self.center_y + self.circle_radius, outline="black", width=2)

    def draw_arrows(self):
        # Clear the canvas before drawing
        self.canvas.delete("arrow")  # Tag for arrows and labels

        angle_step = 360 / self.num_arrows  # Calculate the angle between each arrow

        for i in range(self.num_arrows):
            angle = math.radians(i * angle_step + self.angle_offset)  # Convert angle to radians

            # Start point outside the circle
            x_arrow_start = self.center_x + (self.circle_radius + 30) * math.cos(angle)
            y_arrow_start = self.center_y + (self.circle_radius + 30) * math.sin(angle)

            # End point at the edge of the circle
            x_arrow_end = self.center_x + self.circle_radius * math.cos(angle)
            y_arrow_end = self.center_y + self.circle_radius * math.sin(angle)

            # Draw arrow from outside the circle pointing towards the circle's edge
            self.canvas.create_line(x_arrow_start, y_arrow_start, x_arrow_end, y_arrow_end, arrow=tk.LAST, width=2, tags="arrow")

            # Draw label at the arrow's starting point (outside the circle)
            label_distance = self.circle_radius + 60  # Adjust the distance for the label further out

            # Adjust label position more based on the angle to prevent overlap
            if 85 < math.degrees(angle) < 95:  # Right side
                label_distance += 20
            elif 265 < math.degrees(angle) < 275:  # Left side
                label_distance += 20

            label_x = self.center_x + label_distance * math.cos(angle)
            label_y = self.center_y + label_distance * math.sin(angle)
            self.canvas.create_text(label_x, label_y, text=f"Measurement {i+1}", tags="arrow")

    def update_arrows(self, num_arrows=None, angle_offset=None):
        if num_arrows:
            self.num_arrows = num_arrows
        if angle_offset:
            self.angle_offset = angle_offset

        self.draw_arrows()  # Redraw arrows with the updated values


if __name__ == "__main__":
    app = userInterface()
    app.showWindow()
