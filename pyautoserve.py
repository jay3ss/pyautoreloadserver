import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn
from threading import Event, Thread
from typing import Callable, Generator, Hashable


class HashRegistry:

    def __init__(self, hash_func: Callable = hash) -> None:
        self._registry = dict()
        self._hash = hash_func

    def register(self, key: Hashable, value: Hashable, force: bool = False) -> bool:
        """
        Registers a key-value pair to the register if it's not already present. If
        the pair already exists, then it will not be registered without passing
        `force=True`.

        Args:
            key (Hashable): The key
            value (Hashable): The value.
            force (bool, optional): Force the registering of the key-value pair if
            True. Defaults to False.

        Returns:
            bool: True if the key-value pair was successfully registered, False
            otherwise.
        """
        if key not in self._registry:
            self._registry[key] = self._hash(value)
        else:
            if not force:
                return False
            else:
                return self.update(key, value)

    def update(self, key: Hashable, value: Hashable) -> None:
        """
        Updates the key-value pair in the registry.

        Args:
            key (Hashable): They key.
            value (Hashable): The value.
        """
        self._registry[key] = self._hash(value)

    def compare(self, key: Hashable, value: Hashable) -> bool:
        """
        Compares the given key-value pair with the pair that's currently in the
        registry.

        Args:
            key (Hashable): The key.
            value (Hashable): The value.

        Returns:
            bool: True if the key-value pair matches what is in the registry,
            False otherwise.
        """
        if key not in self._registry:
            return False

        return self._hash(value) == self._registry[key]


class FileObserver:

    def __init__(self, root: str = ".") -> None:
        self._root = Path(root)
        self._registry = HashRegistry()

    def scan(self, pattern: str = "*") -> Generator[Path, None, None]:
        """
        Yield all existing files (of any kind, including directories) matching the
        given relative pattern, anywhere in this subtree.

        Args:
            root (Path): The root to start at.
            ext (str, optional): The file extension to yield. Defaults to "*".

        Yields:
            Generator[Path, None, None]: The Path of the file with the given file
            extension.
        """
        for p in self._root.rglob(pattern):
                if p.is_file():
                    yield p

    def observe(self, pattern: str = "*") -> Path:
        """
        Observe the directory space for any file changes.

        Args:
            pattern (str, optional): The file pattern to observe. Defaults to
            "*" which is all files.

        Returns:
            Path: If the file has changed, then (the Path to the file will be
            returned, otherwise None will be returned.
        """
        for file in self.scan(pattern):
            with open(file, "r") as f:
                data = f.read()

            if not file.name in self._registry:
                    self._registry.register(file, data)
            else:
                if not self._registry.compare(file, data):
                    self._registry.update(file, data)
                    return file

        return None

    def __contains__(self, key: Hashable) -> bool:
        return key in self._registry


class RequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Server(ThreadingMixIn, HTTPServer):
    pass


class AutoreloadHTTPServer:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        root: str = ".",
        delay: float = 0.001,
        *args,
        **kwargs
    ) -> None:
        self._delay = delay
        self._event = Event()
        self._observer = FileObserver(root)
        self._observer_thread = Thread(
            name="observer", target=None, daemon=True
        )
        self._server = Server((host, port), RequestHandler, *args, **kwargs)
        self._server_thread = Thread(
            name="server", target=self._start, daemon=True
        )

    def start(self) -> None:
        """
        Starts the server.
        """
        self._server_thread.start()

    def stop(self) -> None:
        """
        Stops the server
        """
        self._server.shutdown()

    def restart(self) -> None:
        """
        Restarts the server
        """
        self.stop()
        self.start()

    def run(self, pattern: str = "*") -> None:
        self.start()
        while True:
            changed_file = self._observer.observe(pattern)
            if changed_file:
                print(f"{changed_file} has changed. Restarting server")
                self.restart()

            time.sleep(self._delay)


if __name__ == "__main__":
    server = AutoreloadHTTPServer(port=5555)
    server.run()
