import multiprocessing as mp
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from typing import Any, Callable, Generator, Hashable


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

    def __contains__(self, key: Hashable) -> bool:
        return key in self._registry

    def __getitem__(self, key: Hashable) -> Any:
        return self._registry[key]


class FileObserver:

    def __init__(self, root: str = ".") -> None:
        self._root = Path(root)
        self._registry = HashRegistry()

    def scan(self) -> Generator[Path, None, None]:
        """
        Yield all existing files anywhere in the subtree of the root.

        Yields:
            Generator[Path, None, None]: The Path of the file.
        """
        for root, _, files in os.walk(self._root):
            for file in files:
                yield Path(os.path.join(root, file))

    def observe(self) -> list[Path]:
        """
        Observe the directory space for any file changes.

        Returns:
            list[Path]: List of Path to changed files.
        """
        changed_files = []
        for file in self.scan():
            last_changed = os.stat(file).st_mtime
            if file not in self._registry:
                self._registry.register(file, last_changed)
                changed_files.append(file)
            elif not self._registry.compare(file, last_changed):
                self._registry.update(file, last_changed)
                changed_files.append(file)

        return changed_files


class HummingbirdServer(HTTPServer):
    pass


class RequestHandler(SimpleHTTPRequestHandler):
    pass


class AutoreloadHTTPServer:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        root: str = ".",
        delay: float = 0.001,
        server_class: TCPServer = HummingbirdServer,
        request_class: BaseHTTPRequestHandler = RequestHandler
    ) -> None:
        self._delay = delay
        self._observer = FileObserver(Path(root))
        self._httpd = server_class((host, port), request_class)
        self._httpd_process = None

    def serve(self) -> None:
        """
        Starts the server
        """
        self._start_server_process()
        num_files = len(list(self._observer.scan()))
        print(f"Watching {num_files} files.")
        try:
            just_loaded = True
            while True:
                changed_files = self._observer.observe()
                if changed_files and not just_loaded:
                    num_files = len(changed_files)
                    verb = "has" if num_files == 1 else "have"
                    noun = "file" if num_files == 1 else "files"
                    print(f"{num_files} {noun} {verb} changed. Restarting server")
                    self._restart_server_process()
                if just_loaded:
                    just_loaded = False
                time.sleep(self._delay)
        except KeyboardInterrupt as e:
            self._stop_server_process()
            print(e)

    def _start_server_process(self) -> None:
        """
        Starts the server.
        """
        port = self._httpd.server_port
        host = self._httpd.server_name
        print(f"Starting server using host {host} on port {port}")
        self._httpd_process = self._new_server_process()
        self._httpd_process.start()

    def _stop_server_process(self) -> None:
        """
        Stops the server
        """
        self._server.shutdown()

    def _restart_server_process(self) -> None:
        """
        Restarts the server
        """
        self._httpd_process.terminate()
        self._start_server_process()

    def _serve(self) -> None:
        """
        Starts the server.
        """
        self._httpd.serve_forever()

    def _new_server_process(self) -> mp.Process:
        return mp.Process(target=self._serve, name="hummingbird_server")


if __name__ == "__main__":
    server = AutoreloadHTTPServer(port=5555)
    server.serve()
