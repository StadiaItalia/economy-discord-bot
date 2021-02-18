import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="economy-bot",
    version="1.0.0",
    author="ivozzo",
    description="Build your own discord guild economy with this bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StadiaItalia/economy-discord-bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)