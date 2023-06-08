import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Process
from pathlib import Path

from pyautoreloadserver import AutoReloadHTTPServer
from tests.client import HttpClient


class AutoReloadHTTPServerTests(unittest.TestCase):
    def setUp(self):
        self.port = 5555
        self.host = "localhost"
        self.client = HttpClient(host=self.host, port=self.port)
        self.server_process: Process = None

    def tearDown(self) -> None:
        if self.server_process is not None:
            self.server_process.terminate()  # Terminate the server process
            self.server_process.join()  # Wait for the process to finish

    def test_serve(self):
        server = AutoReloadHTTPServer(port=self.port)
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        # Send GET request to the server and verify the response
        response = self.client.open("/")
        server.stop()

        self.assertEqual(response.status, 200)

    def test_stop(self):
        server = AutoReloadHTTPServer(port=self.port)
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        # Send GET request to the server and verify the response
        response = self.client.open("/")
        self.assertEqual(response.status, 200)

        # Terminate the server process and send another request to
        # verify it's not serving anymore
        server.stop()
        self.server_process.terminate()
        self.server_process.join()

        with self.assertRaises(TimeoutError):
            self.client.open("/")

    def test_custom_request_handler(self):
        class CustomRequestHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Custom Request Handler")

        server = AutoReloadHTTPServer(
            RequestHandlerClass=CustomRequestHandler, port=self.port
        )
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        # Send GET request to the server and verify the response
        # from the custom request handler
        response = self.client.open("/")
        server.stop()

        self.assertEqual(response.status, 200)
        self.assertIn("Custom Request Handler", response.read().decode("utf-8"))

    def test_port(self):
        server = AutoReloadHTTPServer(port=self.port)
        self.assertEqual(server._httpd.server_port, self.port)

    def test_serve_changed_file(self):
        server = AutoReloadHTTPServer(port=self.port)
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        new_file = Path("style.css")
        new_file.write_text(".new-style { color: white;}")

        response = self.client.open(f"/{new_file}")
        new_file.unlink()
        server.stop()

        self.assertEqual(response.status, 200)
        self.assertIn("color: white", response.read().decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
