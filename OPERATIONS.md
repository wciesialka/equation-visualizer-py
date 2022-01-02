# Valid Tokens

## Variables

The following variables are supported:

| symbol  | value          |
| ------- | -------------- |
| literal | Literal float value |
| x       | Dependent on x-position of graph |
| t       | Dependent on time[^t] |
| pi      | Pi[^pi] |
| e       | Euler's constant[^e] |
| g       | Gravity on Earth[^g]

[^pi]: Roughly 3.14. 
[^e]: Roughly 0.577.
[^g]: Roughly 9.81.
[^t]: Measured in seconds.

## Operations


### Unary Operations

The following unary operations are supported:

| symbol | operation |
| ------ | --------- |
| -      | Negation  |
### Binary Operations

The following binary operations are supported:

| symbol  | operation      |
| ------- | -------------- |
| +       | Addition       |
| -       | Subtraction    |
| *       | Multiplication |
| /       | Division       |
| ^       | Exponentiation    |
| %       | Floating-point Modulo Operation |

## Functions

The following functions are supported.

| symbol | operation |
| ------ | --------- |
| sin    | Sine      |
| cos    | Cosine    |
| tan    | Tangent   |
| acos   | Arc Cosine |
| asin   | Arc Sine |
| atan   | Arc Tangent |
| cosh   | Hyperbolic Cosine |
| sinh   | Hyperbolic Sine |
| tanh   | Hyperbolic Tangent |
| acosh  | Inverse Hyperbolic Cosine |
| asinh  | Inverse Hyperbolic Sine |
| atanh  | Inverse Hyperbolic Tangent |
| rad    | Convert to radians |
| deg    | Convert to degrees |
| log    | Natural Logarithm |
| abs    | Absolute value of sub-expression |
| round  | Round result of sub-expression |
| sign   | Sign of sub-expression[^sign] |

[^sign]: That is, -1 for a negative result, 1 for a positive result, and 0 otherwise.

Functions must be followed by a sub-expression in paranthesis, i.e. `sin(x)`

## Other

The following are also supported:

| symbol | effect |
| ------ | ------ |
| (      | Begin sub-expression. |
| )      | End sub-expression. |