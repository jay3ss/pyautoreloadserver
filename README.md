Sure! Here's an updated README.md file based on the new code base:

# PyAutoReloadHTTPServer

PyAutoReloadHTTPServer is a simple Python package that provides an HTTP server with automatic reloading functionality. It allows you to serve static files and dynamically reload them whenever they are modified, created, or destroyed. You no longer have to restart your local server to load changed files, this will serve files as they're added and changed. Give it a shot!

## Installation

You can install PyAutoReloadServer using pip:

```bash
pip install pyautoreloadserver
```

## Usage

The easiest way to run it, is to use it from the command line

```shell
pyautoreloadserver -n localhost -p 5555 -r .
```

The flags above can be summarized as follows

- `n`: the hostname
- `p`: the port
- `r`: the root directory to monitor

To use PyAutoReloadHTTPServer, create an instance of the `AutoReloadHTTPServer` class and call the `serve` method to start the server. By default, the server listens on `localhost` and port `8000`, and serves files from the current directory.

```python
from pyautoreloadserver import AutoReloadHTTPServer

# Create an instance of AutoReloadHTTPServer
server = AutoReloadHTTPServer()

# Start the server
server.serve()
```

You can customize the server behavior by providing optional arguments to the `AutoReloadHTTPServer` initializer:

- `host` (str): The hostname or IP address to bind the server to (default: "localhost").
- `port` (int): The port number to listen on (default: 8000).
- `root` (str): The root directory to serve files from (default: ".").
- `delay` (float): The delay between serving requests (default: 0.001 seconds).
- `ServerClass` (TCPServer): The server class to use (default: HTTPServer).
- `RequestHandlerClass` (BaseHTTPRequestHandler): The request handler class to use (default: SimpleHTTPRequestHandler).

```python
from pyautoreloadserver import AutoReloadHTTPServer

# Create an instance of AutoReloadHTTPServer with custom options
server = AutoReloadHTTPServer(host="0.0.0.0", port=8080, root="/path/to/files")

# Start the server
server.serve()
```

Once the server is running, you can visit the specified host and port in your web browser to access the served files.

To stop the server, call the `stop` method:

```python
server.stop()
```

Although you'll probably want to start this in a separate thread/process because the server is running a loop that may block.

## Logging

PyAutoReloadHTTPServer logs informational messages using the `logging` module. By default, the log level is set to `logging.INFO`, but you can configure it according to your needs.

```python
import logging

# Set the log level to DEBUG for more detailed logs
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions to PyAutoReloadHTTPServer are welcome! If you find a bug, have a feature request, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/jay3ss/pyautoreloadserver).

## License

This project is licensed under the [MIT License](LICENSE).
