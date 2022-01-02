# veq
Veq, short for **V**iew **Eq**uation, is a pygame based application for graphing equations.

Note: If you are viewing this README from PyPI, you may be unable to properly open links. Please check the README on the [GitHub page](https://github.com/wciesialka/veq), instead. 

## Getting Started

### Installation

The recommended way to install the most up-to-date version of this project is by cloning the respository and running `setup.py install`. This allows you to control which branch you install as well. This may not always guarantee a stable release, however.

You can also use pip to install the recommended release from [PyPI](https://pypi.org/project/veq/) with `pip install veq`.

### Requirements

It is recommended you use the most recent stable version of Python. This project was built using Python 3.8.10. Dependencies are listed in [requirements.txt](requirements.txt) and should be installed when running `setup.py`.

### Running

Running the application can be done through the console script entry point `veq` or through `python3 -m veq`. The application takes the following command-line arguments:

```
usage: veq [-h] [--debug] [-s n] [-a] [-p PRECISION] [-d DOMAIN] [-r RANGE]
           equation

Visualize an equation.

positional arguments:
  equation              Equation to plot.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable debug logging.
  -s n, --step n        Enable gridlines with step n
  -a, --noaxis          Disable axis.
  -p PRECISION, --precision PRECISION
                        Number precision for text formatting.
  -d DOMAIN, --domain DOMAIN
                        Initial domain.
  -r RANGE, --range RANGE
                        Initial range.
```

## Features

Expressions will be evaluated and graphed with `y = f(x)` over a set domain and range. You can view exactly where a point falls on an equation by hovering over the line. You can also find the corresponding y-value to an x-value by moving the mouse. You can save one point for reference.

### Syntax

See [OPERATIONS.md](OPERATIONS.md) for valid operations.

### Controls

The following controls are supported:

| control | action |
| ------- | ------ |
| Left Mouse Button | Save point. |
| Mouse Right-Click Drag | Move view by changing domain and range. |
| Mouse Wheel Up | Zoom in by decreasing domain and range. |
| Mouse Wheel Down | Zoom out by increasing domain and range. |
| + | Zoom in by decreasing domain and range. |
| - | Zoom out by increasing domain and range. |
| R | Reset domain and range. |
| SHIFT-R | Reset variable t. |
| Left/Right Arrow | Shift domain left/right. |
| Up/Down Arrow | Shift range up/down. |

## Documentation

Documentation is supplied through Sphinx Auto-Doc and is available on [readthedocs](https://veq.readthedocs.io/en/latest/index.html).

## License

This project is licensed under GNU GENERAL PUBLIC LICENSE V3. View [LICENSE](LICENSE) for details.

## Authors

- Willow Ciesialka
