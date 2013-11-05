# Lysis

Python based solver for propositional calculus.

## Command-line interface

```
$ lysis -t "A => B" "ZED & /BE"
| A   | B   | BE   | ZED   | (A => B)   | (ZED & /BE)   |
|-----+-----+------+-------+------------+---------------|
| t   | t   | t    | t     | t          | f             |
| t   | t   | t    | f     | t          | f             |
| t   | t   | f    | t     | t          | t             |
| t   | t   | f    | f     | t          | f             |
| t   | f   | t    | t     | f          | f             |
| t   | f   | t    | f     | f          | f             |
| t   | f   | f    | t     | f          | t             |
| t   | f   | f    | f     | f          | f             |
| f   | t   | t    | t     | t          | f             |
| f   | t   | t    | f     | t          | f             |
| f   | t   | f    | t     | t          | t             |
| f   | t   | f    | f     | t          | f             |
| f   | f   | t    | t     | t          | f             |
| f   | f   | t    | f     | t          | f             |
| f   | f   | f    | t     | t          | t             |
| f   | f   | f    | f     | t          | f             |
```

## Features

- operator precedence is taken into account (eg. `C => A & B` evaluates to `C => (A & B)`)
- colorized output if supported (requires `termcolor` module, plus `colorama` on Windows)
- unicode table-frame

## Requirements

- Python 2 (tested under Python 2.5 and 2.7)
- [scan](https://github.com/NiklasRosenstein/scan) (>= 4.6.0)
- [tabulate](https://pypi.python.org/pypi/tabulate) (>= 0.6)
- [termcolor](https://pypi.python.org/pypi/termcolor) (>= 1.1.0; optional)
- [colorama](https://pypi.python.org/pypi/colorama) (>= 0.2.7; optional, for colored output on Windows)

## License

Lysis is licensed under the MIT License.
