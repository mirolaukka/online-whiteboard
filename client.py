import socket
import threading
import tkinter as tk
import json
from tkinter import Canvas, messagebox, Scale, Button

HOST = "127.0.0.1"
PORT = 8080

class WhiteboardApp:
    def __init__(self, root, server_socket):
        self.root = root
        self.server_socket = server_socket
        self.canvas = Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.pen_color = "black"
        self.pen_width = 5

        self.points = []
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.create_toolbar()

        self.batch_size = 10  # Number of points to send in each batch
        self.drawing = False
        self.points_buffer_preview = []  # Separate buffer for pen preview
        self.points_buffer_draw = []     # Separate buffer for actual drawing
        self.after_id = None  # Store the ID returned by after method

        self.preview_pen_color = "black"
        self.preview_pen_width = 5

        self.canvas.bind("<Motion>", self.on_preview)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(fill=tk.X)

        colors = ["black", "red", "blue", "green", "orange", "yellow", "purple", "pink"]
        for color in colors:
            color_btn = Button(toolbar, bg=color, width=3, command=lambda c=color: self.change_pen_color(c))
            color_btn.pack(side=tk.LEFT)

        pen_width_slider = Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL, label="Pen Width",
                                 command=self.change_pen_width)
        pen_width_slider.set(self.pen_width)
        pen_width_slider.pack(side=tk.LEFT, padx=5)

        clear_btn = Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=10)

    def on_preview(self, event):
        # Clear the previous preview oval on the main canvas
        self.canvas.delete("preview_pen")

        # Draw the new preview of the pen position directly on the main canvas
        x, y = event.x, event.y
        self.canvas.create_oval(
            x - self.preview_pen_width, y - self.preview_pen_width,
            x + self.preview_pen_width, y + self.preview_pen_width,
            fill=self.preview_pen_color, width=0, tags="preview_pen"
        )
        self.points_buffer_preview.append((x, y, self.preview_pen_width, self.preview_pen_color))


    def change_pen_color(self, color):
        self.pen_color = color
        self.preview_pen_color = color

    def change_pen_width(self, width):
        self.pen_width = int(width)
        self.preview_pen_width = int(width)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.server_socket.sendall("clear".encode())

    def start_drawing(self, event):
        self.drawing = True
        self.points_buffer_draw.append((event.x, event.y, self.pen_width, self.pen_color))
        self.after_id = self.root.after(100, self.send_batch_points)

    def stop_drawing(self, event):
        self.drawing = False
        if self.after_id:
            self.root.after_cancel(self.after_id)  # Cancel the scheduled after call
            self.after_id = None

        if self.points_buffer_draw:
            self.points_buffer_draw.clear()

    def send_batch_points(self):
        if self.points_buffer_draw:
            message = json.dumps(self.points_buffer_draw).encode()
            self.server_socket.sendall(message)
            self.points_buffer_draw.clear()
        self.after_id = self.root.after(100, self.send_batch_points)

    def on_drag(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_oval(x, y, x + self.pen_width, y + self.pen_width, fill=self.pen_color, width=0)
            self.points_buffer_draw.append((x, y, self.pen_width, self.pen_color))

def receive_points(canvas, server_socket):
    buffer = b""
    while True:
        data = server_socket.recv(4096)  # Use a reasonable buffer size
        if not data:
            break

        buffer += data
        try:
            while buffer:
                # Try to decode JSON data from the buffer
                points, buffer = json.loads(buffer.decode()), b""
                for x, y, width, color in points:
                    canvas.create_oval(x, y, x + width, y + width, fill=color, width=0)
        except json.JSONDecodeError:
            # Incomplete JSON data received, continue receiving
            pass

def main():
    root = tk.Tk()
    root.title("Whiteboard Client")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Could not connect to the server.")
        return

    app = WhiteboardApp(root, server_socket)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

    receiver_thread = threading.Thread(target=receive_points, args=(app.canvas, server_socket))
    receiver_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
