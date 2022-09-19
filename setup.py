from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyaccsharedmemory",
    version="1.0.0",
    author="Ryan Rennoir",
    author_email="ryanrennoir9@gmail.com",
    url="https://github.com/rrennoir/PyAccSharedMemory",
    description="ACC shared memory reader in python",
    py_modules=["pyaccsharedmemory"],
    package_dir={"": "src"},
    classifiers=[
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)