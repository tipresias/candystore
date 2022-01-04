"""Setup the candystore package."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="candystore",
    version="0.3.4",
    author="Craig Franklin",
    author_email="craigjfranklin@gmail.com",
    description="Factories for randomised AFL data sets for testing purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tipresias/candystore",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "faker",
        "mypy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
