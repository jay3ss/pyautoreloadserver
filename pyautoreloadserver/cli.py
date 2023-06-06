#!/usr/bin/env python

from pyautoreloadserver import AutoReloadHTTPServer

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the server")
    parser.add_argument(
        "-r",
        dest="root",
        default=".",
        type=str,
        help="The root directory to monitor",
    )
    parser.add_argument(
        "-p",
        action="store",
        dest="port",
        default=8000,
        type=int,
        help="The port to use",
    )
    parser.add_argument(
        "-n",
        action="store",
        dest="name",
        default="localhost",
        type=str,
        help="The host name to use",
    )

    args = parser.parse_args()

    server = AutoReloadHTTPServer(port=args.port, root=args.root)
    server.serve()

if __name__ == "__main__":
    main()
