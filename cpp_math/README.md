# Matrix Engine

## Features

- Vector arithmetic
- Matrix arithmetic
- Matrix multiplication
- Determinants
- Matrix inversion
- Transpose
- Vector operations

## Build

cmake -S . -B build
cmake --build build

## Install

pip install -e .

## Usage

```python
import matrix_engine

v = matrix_engine.Vector([1,2,3])
w = matrix_engine.Vector([4,5,6])

print(v.dot(w))
```
