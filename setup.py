from setuptools import find_packages, setup

NAME = "mechanic"
VERSION = "1.0.0"

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name=NAME,
    version=VERSION,
    description="Scale reading and motor controlling API for RPi",
    author="oliverosborne9",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["mechanic=mechanic.bin:cli"],
    },
)
