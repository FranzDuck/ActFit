from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().split("\n")

setup(
    name="ActFit",
    version="1.0",
    description="A small library and tools to help fitting functions to data.",
    long_description=long_description,
    packages=find_namespace_packages(),
    author="Philipp Stärk, Tim Fischer",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=requirements,
    entry_points={
        "console_scripts": ["ActFit = ActFit.ui.__main__:main"],
        "gui_scripts": ["ActFit = ActFit.ui.__main__:main"],
    },
)
