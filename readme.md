# Whiteboard Collaboration App

The Whiteboard Collaboration App is a simple client-server application that allows multiple users to draw on a shared whiteboard canvas in real-time. The server runs on a specific IP address and port and listens for incoming connections from clients. Clients can connect to the server and draw on their local canvas, and their drawings will be broadcasted to all other connected clients.

## Requirements

- Python 3.x

## How to Use

### Running the Server

1. Open a terminal or command prompt.
2. Navigate to the directory containing the `server.py` file.
3. Run the following command to start the server:

```bash
python server.py
```

### Running the Client

1. Open a terminal or command prompt.
2. Navigate to the directory containing the `client.py` file.
3. Run the following command to start the client:

```bash
python client.py
```

### Using the Client

1. Upon running the client, a GUI window will open showing a white canvas and a toolbar at the bottom.
2. To draw on the canvas, select a pen color from the color buttons in the toolbar.
3. Adjust the pen width using the pen width slider in the toolbar.
4. Click and drag on the canvas to draw freely.
5. Release the mouse button to stop drawing.
6. To clear the canvas, click the "Clear" button in the toolbar.

## How it Works

### Server (`server.py`)

The server is implemented using the Python `socket` library. It listens for incoming client connections on a specified IP address (`HOST`) and port (`PORT`). For each client that connects, a separate thread is created (`handle_client`) to handle their communication. The server receives drawing data from clients and broadcasts it to all connected clients, enabling real-time collaboration.

### Client (`client.py`)

The client is implemented as a graphical application using the `tkinter` library for the GUI and the `socket` library for communication with the server. Upon starting the client, it establishes a connection with the server using the specified IP address (`HOST`) and port (`PORT`).

The GUI window of the client includes a white canvas where users can draw, a toolbar with color buttons and a pen width slider to customize their drawing experience. The client continuously sends drawing data to the server as the user draws on the canvas. It also receives drawing data from the server to update the canvas with the drawings of other connected users.

## Contribution

This project is a simple illustration of a collaborative whiteboard application. If you find any issues or have ideas for improvements, you are welcome to contribute by submitting a pull request or opening an issue on the GitHub repository.

Happy drawing and collaborating! 🎨✨