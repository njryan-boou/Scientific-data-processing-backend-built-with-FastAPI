matrix_config = {
    "json_schema_extra": {
        "example": {
            "matrix": [
                [1, 2],
                [3, 4],
            ]
        }
    }
}

matrix_2_config = {
    "json_schema_extra": {
        "example": {
            "matrix_a": [
                [1, 2],
                [3, 4],
            ],
            "matrix_b": [
                [5, 6],
                [7, 8],
            ]
        }
    }
}

scalar_matrix_config = {
    "json_schema_extra": {
        "example": {
            "matrix": [
                [1, 2],
                [3, 4],
            ],
            "scalar": 2.5,
        }
    }
}

vector_config = {
    "json_schema_extra": {
        "example": {
            "vector": [1, 2, 3, 4]
        }
    }
}

euler_config = {
    "json_schema_extra": {
        "example": {
            "y0": 1.0,
            "t0": 0.0,
            "step_size": 0.5,
            "steps": 3,
        }
    }
}
