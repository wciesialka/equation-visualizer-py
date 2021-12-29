#!/bin/env python3
'''Setup script.'''
from pathlib import Path
from setuptools import setup, find_packages

THIS_DIRECTORY = Path(__file__).parent

REQUIREMENTS = (THIS_DIRECTORY / "requirements.txt").read_text().split('\n')[:-1]
LONG_DESCRIPTION = (THIS_DIRECTORY / "README.md").read_text()

CONTENT = {
    "name": "veq",
    "version": "1.3.2",
    "author": "Willow Ciesialka",
    "author_email": "wciesialka@gmail.com",
    "url": "https://github.com/wciesialka/riemann-sum-py",
    "description": "Equation visualizer.",
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "license": "GPL-3.0",
    "packages": find_packages(where="src"),
    "entry_points": {
        'console_scripts': [
            'veq = veq.__main__:main'
        ]
    },
    "classifiers": [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    "keywords": "python image math",
    "package_dir": {"": "src"},
    "install_requires": REQUIREMENTS,
    "zip_safe": False,
    "python_requires": ">=3.8.10"
}

setup(**CONTENT)
