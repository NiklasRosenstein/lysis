# Lysis

Python based solver for propositional calculus and sets.

## Command-line interface

    $ lysis "(!A => B) <=> (A & !B)" -table
    A  |  B  |  (!A => B) <=> (A & !B)
    ---+-----+------------------------
    w  |  w  |           f
    w  |  f  |           w
    f  |  w  |           f
    f  |  f  |           w

## Requirements

- Python 2
- [py-scan](https://github.com/NiklasRosenstein/py-scan) (>= 4.6.0)
