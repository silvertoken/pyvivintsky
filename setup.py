import setuptools

NAME = "pyVivintSky"
PACKAGE_NAME = "pyvivintsky"
VERSION = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author="Will Oldenburg",
    author_email="silvertoken99@gmail.com",
    description="Python library for interacting with Vivint Sky API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silvertoken/pyvivintsky",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	license='MIT',
	keywords='vivint',
)