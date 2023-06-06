# PyAutoReloadServer

PyAutoServe is a Python package that provides an auto-reloading HTTP server for serving files from a specified directory. It is designed to simplify the process of serving and monitoring files during development or local testing.

## Features

- Automatic file change detection: PyAutoServe monitors the specified directory for any changes to the files and automatically reloads the server whenever a change is detected.
- Flexible customization: You can easily customize the server's behavior by specifying the host, port, root directory, delay between checks, and the request handler class.
- Simple command-line interface: PyAutoServe provides a convenient command-line interface for running the server, allowing you to quickly start serving files with minimal configuration.

## Installation

You can install PyAutoServe using pip:

```
pip install pyautoserve
```

## Usage

To use PyAutoServe, follow these steps:

1. Import the necessary classes and functions from the `pyautoserve` module:

   ```python
   from pyautoreloadserver import AutoreloadHTTPServer
   ```

2. Create an instance of the `AutoreloadHTTPServer` class:

   ```python
   server = AutoreloadHTTPServer(
       host="localhost",
       port=8000,
       root="/path/to/root",
       delay=0.001,
       RequestClass=RequestHandlerClass,
   )
   ```

   Customize the server's configuration according to your needs. The `host` and `port` parameters specify the server's listening address, while the `root` parameter determines the directory from which files will be served. The `delay` parameter controls the delay between file change checks.

5. Start the server:

   ```python
   server.serve()
   ```

   This method will start the server and monitor the specified directory for file changes. The server will automatically restart whenever a change is detected.

6. Stop the server (optional):

   ```python
   server.stop()
   ```

   If you want to stop the server programmatically, you can call the `stop` method.

Alternatively, you can run the server directly from the command line:

```shell
python my_server.py -r /path/to/root -p 8000 -n localhost
```

This will start the server with the specified configuration.

## License

PyAutoServe is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
