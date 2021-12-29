# veq
Veq, short for **V**iew **Eq**uation, is a pygame based application for graphing equations.

## Getting Started

### Installation

The recommended way to install the most up-to-date version of this project is by cloning the respository and running `setup.py install`. This allows you to control which branch you install as well. This may not always guarantee a stable release, however.

You can also use pip to install the recommended release from [PyPI](https://pypi.org/project/veq/) with `pip install veq`.

### Requirements

It is recommended you use the most recent stable version of Python. This project was built using Python 3.8.10. Dependencies are listed in [requirements.txt](requirements.txt) and should be installed when running `setup.py`.

### Running

Running the application can be done through the console script entry point `veq` or through `python3 -m veq`. The application takes the following command-line arguments:

```
usage: veq [-h] [-d] equation

Visualize an equation.

positional arguments:
  equation     Equation to plot.

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug logging.
  -s n, --step n  Enable gridlines with step n
  -a, --noaxis    Disable axis.
```

## Features

Expressions will be evaluated and graphed with `y = f(x)` over a set domain and range. You can view exactly where a point falls on an equation by hovering over the line. You can also find the corresponding y-value to an x-value by moving the mouse. You can save one point for reference.

### Syntax

The following operations are supported:

| symbol  | operation      |
| ------- | -------------- |
| Number  | Any floating point number.      |
| pi      | Pi             |
| e       | Euler's constant |
| x       | The variable x  |
| t       | A time-based variable t |
| +       | Addition       |
| -       | Subtraction    |
| *       | Multiplication |
| /       | Division       |
| ^       | Exponential    |
| ( )     | Paranthesis    |
| sin[^1] | Sin            |
| cos[^1] | Cos            |
| tan[^1] | Tan            |
| log[^1] | Log            |

[^1]: Must be followed by a sub-expression in paranthesis, i.e. `sin(x)`

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
| r | Reset domain and range. |

## Documentation

Documentation is supplied through Sphinx Auto-Doc and is available in [docs/build/html](docs/build/html).

## License

This project is licensed under GNU GENERAL PUBLIC LICENSE V3. View [LICENSE](LICENSE) for details.

## Authors

- Willow Ciesialka
