# Scientific Computing API

A modular scientific computing backend built with FastAPI. The project separates numerical computation from the API layer, allowing the computation engine to be used independently or exposed through HTTP endpoints.

## Features

### Linear Algebra

* Matrix determinant
* Matrix inverse
* Matrix transpose
* Matrix trace
* Eigenvalue calculations

### Statistics

* Mean
* Standard deviation
* Variance
* Minimum and maximum values
* Statistical summaries

### Ordinary Differential Equations

* Euler method solver

## Architecture

The project is organized into two primary layers:

```text
API Layer
    ↓
Computation Engine
```

### Engine

The engine contains all numerical and scientific computation logic.

```python
from app.engine.linalg import determinant
from app.engine.stats import summary
from app.engine.ode import euler
```

### API

The API layer exposes engine functionality through FastAPI endpoints.

Features include:

* Request validation using Pydantic
* Response models
* Custom exception handling
* Structured logging
* OpenAPI/Swagger documentation

## Project Structure

```text
app/
│
├── api/
│   ├── models/
│   └── routes/
│
├── engine/
│   ├── linalg/
│   ├── stats/
│   └── ode/
│
├── utils/
├── tests/
└── logging_config.py
```

## Installation

Clone the repository:

```bash
git clone <git@github.com:your-username/scientific-api.git>
cd <Scientific-data-processing-backend-built-with-FastAPI>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requires.txt
```

## Running the API

Start the development server:

```bash
uvicorn app.api.main:app --reload
```

API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Execute the test suite:

```bash
pytest
```

## Example Requests

### Determinant

Request:

```json
{
    "matrix": [
        [1, 2],
        [3, 4]
    ]
}
```

Response:

```json
{
    "determinant": -2.0
}
```

### Statistics Summary

Request:

```json
{
    "data": [1, 2, 3, 4, 5]
}
```

Response:

```json
{
    "mean": 3.0,
    "std": 1.4142,
    "minimum": 1.0,
    "maximum": 5.0
}
```

## Design Goals

* Separation of concerns between API and computation layers
* Reusable scientific computation engine
* Strong validation and error handling
* Automated testing
* Extensible module-based architecture

## Future Development

Potential future modules include:

* Numerical integration
* Optimization algorithms
* Regression and statistical modeling
* Advanced ODE solvers (RK4, adaptive methods)
* Scientific visualization support
* C++ accelerated computational backends
