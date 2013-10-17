# Lysis

Python based solver for propositional calculus.

## Command-line interface

    $ python -m lysis --table "(A & B) & C" "A & (B & C)"
    A | B | C | ((A & B) & C) | (A & (B & C))
    --+---+---+---------------+--------------
    t | t | t | t             | t
    t | t | f | f             | f
    t | f | t | f             | f
    t | f | f | f             | f
    f | t | t | f             | f
    f | t | f | f             | f
    f | f | t | f             | f
    f | f | f | f             | f

## Requirements

- Python 2
- [py-scan](https://github.com/NiklasRosenstein/py-scan) (>= 4.6.0)

## License

Lysis is licensed under the MIT License.