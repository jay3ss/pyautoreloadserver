import contextlib
import logging
import socket
import time
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    SimpleHTTPRequestHandler,
    ThreadingHTTPServer,
)
from socketserver import TCPServer


logging.basicConfig(level=logging.INFO)


BaseServerClass = ThreadingHTTPServer | HTTPServer


class RequestHandler(SimpleHTTPRequestHandler):
    pass


class AutoReloadHTTPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        root: str = ".",
        delay: float = 0.001,
        ServerClass: BaseServerClass = None,
        RequestHandlerClass: BaseHTTPRequestHandler = RequestHandler,
    ) -> None:
        # adapted from:
        # https://github.com/python/cpython/blob/
        # c2df09fb4d152fd0748790af38668841e4faca93/Lib/http/server.py#L1300
        if not ServerClass:

            class DualStackServer(ThreadingHTTPServer):
                def server_bind(self):
                    # suppress exception when protocol is IPv4
                    with contextlib.suppress(Exception):
                        self.socket.setsockopt(
                            socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0
                        )
                    return super().server_bind()

                def finish_request(self, request, client_address):  # pragma: no cover
                    self.RequestHandlerClass(
                        request, client_address, self, directory=root
                    )

            ServerClass = DualStackServer

        self._delay = delay
        self._root = root
        self._httpd = ServerClass((host, port), RequestHandlerClass)
        self._stop_flag = False

    def serve(self) -> None:
        """
        Starts the server
        """
        try:
            root = self._root
            host, port = self._httpd.server_address
            log_msg = f"Serving {root}. Visit http://{host}:{port}"
            logging.info(log_msg)
            while not self._stop_flag:
                self._httpd.handle_request()
                time.sleep(self._delay)
        except KeyboardInterrupt as e:
            logging.info("Quitting server...")
            logging.error(e)

    def stop(self) -> None:
        """
        Stops serving
        """
        self._stop_flag = True
