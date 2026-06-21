from app.engine.utils import validation


def summary(data):

    arr = validation.asarray(data)

    return {
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "minimum": float(arr.min()),
        "maximum": float(arr.max()),
        "variance": float(arr.var()),
    }