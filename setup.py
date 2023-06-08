import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent
readme = (here / "README.md").read_text()

extras_require = (here / "requirements.txt").read_text().splitlines()


setup(
    name="pyautoreloadserver",
    version="0.0.1",
    author="Jay Ess",
    description="A simple HTTP server that serves files, even on file change",
    url="https://github.com/jay3ss/pyautoreloadserver",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    extras_require={"dev": extras_require},
    entry_points={
        "console_scripts": [
            "pyautoreloadserver = pyautoreloadserver.cli:main",
        ],
    },
    package_dir={
        "tests": "tests",
        "pyautoreloadserver": "pyautoreloadserver",
    },
)
