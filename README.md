# veq
Veq, short for **V**iew **Eq**uation, is a pygame based application for graphing equations.

## Getting Started

### Installation

The recommended way to install the most up-to-date version of this project is by cloning the respository and running `setup.py install`. This allows you to control which branch you install as well. This may not always guarantee a stable release, however.

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
```

## Features

### Syntax

The following operations are supported:

| symbol  | operation      |
| ------- | -------------- |
| +       | Addition       |
| -       | Subtraction    |
| *       | Multiplication |
| /       | Division       |
| ^       | Exponential    |
| ( )     | Paranthesis    |
| x       | "x" variable.  |
| sin[^1] | Sin            |
| cos[^1] | Cos            |
| tan[^1] | Tan            |
| log[^1] | Log            |

[^1]: Must be followed by a sub-expression in paranthesis, i.e. `sin(x)`

### Controls

The following controls are supported:

| control | action |
| ------- | ------ |
| Mouse Drag | Move view by changing domain and range. |
| Mouse Wheel Up | Zoom in by decreasing domain and range. |
| Mouse Wheel Down | Zoom out by increasing domain and range. |
| r | Reset domain and range. |

## License

This project is licensed under GNU GENERAL PUBLIC LICENSE V3. View [LICENSE](LICENSE) for details.

## Authors

- Willow Ciesialka