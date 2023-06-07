# import unittest
# import threading
# import time
# from http.server import BaseHTTPRequestHandler, HTTPServer

# from pyautoreloadserver import AutoReloadHTTPServer
# from tests.client import HttpClient


# class Server(HTTPServer):
#     pass


# class RequestHandler(BaseHTTPRequestHandler):
#     pass


# class AutoReloadHTTPServerTests(unittest.TestCase):

#     def setUp(self):
#         self.port = 5555
#         self.host = "localhost"
#         self.client = HttpClient(host=self.host, port=self.port)
#         self.server = None
#         self.server_thread: threading.Thread = None

#     def tearDown(self) -> None:

#         if self.server_thread is not None and self.server_thread.is_alive():
#             if self.server and self.server._stop_flag:
#                 self.server.stop()
#             self.server_thread.join()

#     def test_serve(self):
#         self.server = AutoReloadHTTPServer(port=8000)
#         self.server_thread = threading.Thread(target=self.server.serve)
#         self.server_thread.start()

#         time.sleep(0.1)  # Allow server to start

#         # Send GET request to the server and verify the response
#         response = self.client.open("/")
#         self.assertEqual(response.status, 200)

#     def test_stop(self):
#         self.server = AutoReloadHTTPServer()
#         self.server_thread = threading.Thread(target=self.server.serve)
#         self.server_thread.start()

#         time.sleep(0.1)  # Allow server to start

#         # Send GET request to the server and verify the response
#         response = self.client.open("/")
#         self.server.stop()
#         self.assertEqual(response.status, 200)

#         # Stop the server and send another request to verify it's not serving anymore
#         # server_thread.join()

#         response = self.client.open("/")
#         self.assertEqual(response.status, 500)

#     def test_custom_request_handler(self):
#         class CustomRequestHandler(BaseHTTPRequestHandler):
#             def do_GET(self):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/plain')
#                 self.end_headers()
#                 self.wfile.write(b'Custom Request Handler')

#         self.server = AutoReloadHTTPServer(RequestHandlerClass=CustomRequestHandler)
#         self.server_thread = threading.Thread(target=self.server.serve)
#         self.server_thread.start()

#         time.sleep(0.1)  # Allow server to start

#         # Send GET request to the server and verify the response from the custom request handler
#         response = self.client.open("/")
#         self.server.stop()
#         self.assertEqual(response.status, 200)
#         self.assertEqual(response.read().decode(), 'Custom Request Handler')

#         # self.server_thread.join()

#     def test_port(self):
#         self.server = AutoReloadHTTPServer(port=9000)
#         self.assertEqual(self.server._httpd.server_port, 9000)

#     def test_request_handler_directory(self):
#         self.server = AutoReloadHTTPServer(root='/path/to/directory')
#         request_handler = self.server._httpd.RequestHandlerClass(
#             None, '/', self.server._httpd.server_address, self.server._httpd
#         )
#         self.assertEqual(request_handler.directory, '/path/to/directory')


# if __name__ == '__main__':
#     # unittest.main()
#     import pytest
#     pytest.main(["-s", __file__])
import unittest
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process

from pyautoreloadserver import AutoReloadHTTPServer
from tests.client import HttpClient


class Server(HTTPServer):
    pass


class RequestHandler(BaseHTTPRequestHandler):
    pass


class AutoReloadHTTPServerTests(unittest.TestCase):

    def setUp(self):
        self.port = 5555
        self.host = "localhost"
        self.client = HttpClient(host=self.host, port=self.port)
        self.server_process: Process = None

    def tearDown(self) -> None:
        if self.server_process is not None and self.server_process.is_alive():
            self.server_process.terminate()  # Terminate the server process
            self.server_process.join()  # Wait for the process to finish

    def test_serve(self):
        server = AutoReloadHTTPServer(port=8000)
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        time.sleep(0.1)  # Allow server to start

        # Send GET request to the server and verify the response
        response = self.client.open("/")
        server.stop()
        self.assertEqual(response.status, 200)

    def test_stop(self):
        server = AutoReloadHTTPServer()
        self.server_process = Process(target=server.serve)
        self.server_process.start()

        time.sleep(0.1)  # Allow server to start

        # Send GET request to the server and verify the response
        response = self.client.open("/")
        self.assertEqual(response.status, 200)

        # Terminate the server process and send another request to verify it's not serving anymore
        server.stop()
        self.server_process.terminate()
        self.server_process.join()

        response = self.client.open("/")
        self.assertEqual(response.status, 500)

    # def test_custom_request_handler(self):
    #     class CustomRequestHandler(BaseHTTPRequestHandler):
    #         def do_GET(self):
    #             self.send_response(200)
    #             self.send_header('Content-type', 'text/plain')
    #             self.end_headers()
    #             self.wfile.write(b'Custom Request Handler')

    #     server = AutoReloadHTTPServer(RequestHandlerClass=CustomRequestHandler)
    #     self.server_process = Process(target=server.serve)
    #     self.server_process.start()

    #     time.sleep(0.1)  # Allow server to start

        # Send GET request to the server and verify the response from the custom request handler
        response = self.client.open("/")
        server.stop()
        self.server_process.terminate()
        self.server_process.join()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.read().decode(), 'Custom Request Handler')

    def test_port(self):
        server = AutoReloadHTTPServer(port=9000)
        self.assertEqual(server._httpd.server_port, 9000)

    def test_request_handler_directory(self):
        server = AutoReloadHTTPServer(root='/path/to/directory')
        request_handler = server._httpd.RequestHandlerClass(
            None, '/', server._httpd.server_address, server._httpd
        )
        self.assertEqual(request_handler.directory, '/path/to/directory')


if __name__ == '__main__':
    unittest.main()
