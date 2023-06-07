from http import client
from urllib import parse, request


class HttpClient:

    def __init__(self, host: str, port: int = None) -> None:
        self.host = host
        self.port = port

    def open(self, url: str, data: dict = None) -> client.HTTPResponse:
        full_url = parse.urljoin(f"http://{self.host}:{self.port}", url)
        return request.urlopen(full_url, data=data)
