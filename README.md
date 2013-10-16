# Lysis

Python based solver for propositional calculus.

## Command-line interface

```
$ lysis --table "A & B <=> A | /B" "A | /B"
 A | B | ((A & B) <=> (A | /B)) | (A | /B)
---+---+------------------------+---------
 t | t | t                      | t
 t | f | f                      | t
 f | t | t                      | f
 f | f | f                      | t
```

## Features

- operator precedence is taken into account (eg. `C => A & B` evaluates to `C => (A & B)`)
- colorized output if supported (requires `termcolor` module, plus `colorama` on Windows)

## Requirements

- Python 2 (tested under Python 2.5 and 2.7)
- [scan](https://github.com/NiklasRosenstein/scan) (>= 4.6.0)
- [termcolor](https://pypi.python.org/pypi/termcolor) (>= 1.1.0; optional)
- [colorama](https://pypi.python.org/pypi/colorama) (>= 0.2.7; optional)

## License

Lysis is licensed under the MIT License.