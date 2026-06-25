import time
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Import your C++ matrix class
# -------------------------------------------------
from matrix_engine import Vector as CppVector   # <-- Change this


# -------------------------------------------------
# Benchmark settings
# -------------------------------------------------
SIZES = [
    1,
    10,
    100,
    1_000,
    10_000,
    100_000,
    1_000_000,
]

REPEATS = 20

python_times = []
numpy_times = []
cpp_times = []


# -------------------------------------------------
# Timing helper
# -------------------------------------------------
def benchmark(func):
    times = []

    # Warmup
    func()

    for _ in range(REPEATS):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)

    return sum(times) / len(times)


# -------------------------------------------------
# Main benchmark loop
# -------------------------------------------------
for N in SIZES:

    print(f"Benchmarking N = {N:,}")

    # ------------------------
    # Python Lists
    # ------------------------
    list1 = list(range(N))
    list2 = list(range(N))

    python_time = benchmark(
        lambda: [a + b for a, b in zip(list1, list2)]
    )

    # ------------------------
    # NumPy
    # ------------------------
    np1 = np.arange(N, dtype=np.float64)
    np2 = np.arange(N, dtype=np.float64)

    numpy_time = benchmark(
        lambda: np1 + np2
    )

    # ------------------------
    # C++ Vector
    # ------------------------
    cpp1 = CppVector(N)
    cpp2 = CppVector(N)

    for i in range(N):
        cpp1[i] = i
        cpp2[i] = i

    cpp_time = benchmark(
        lambda: cpp1 + cpp2
    )

    python_times.append(python_time)
    numpy_times.append(numpy_time)
    cpp_times.append(cpp_time)

    print(
        f"Python: {python_time:.6e}s | "
        f"NumPy: {numpy_time:.6e}s | "
        f"C++ Vector: {cpp_time:.6e}s"
    )


# -------------------------------------------------
# Plot Runtime
# -------------------------------------------------
plt.figure(figsize=(10,6))

plt.plot(SIZES, python_times, "o-", label="Python List")
plt.plot(SIZES, numpy_times, "o-", label="NumPy")
plt.plot(SIZES, cpp_times, "o-", label="C++ Vector")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Number of Elements")
plt.ylabel("Average Runtime (seconds)")
plt.title("Runtime Comparison")
plt.grid(True)
plt.legend()

plt.tight_layout()


# -------------------------------------------------
# Plot Speedup
# -------------------------------------------------
plt.figure(figsize=(10,6))

python_speedup = [
    p / c for p, c in zip(python_times, cpp_times)
]

numpy_speedup = [
    n / c for n, c in zip(numpy_times, cpp_times)
]

plt.plot(SIZES, python_speedup, "o-", label="Python / C++")
plt.plot(SIZES, numpy_speedup, "o-", label="NumPy / C++")

plt.axhline(1.0, linestyle="--")

plt.xscale("log")

plt.xlabel("Number of Elements")
plt.ylabel("Speedup")
plt.title("Relative Performance")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# -------------------------------------------------
# Print Table
# -------------------------------------------------
print("\nResults")
print("-" * 75)
print(f"{'N':>10} {'Python':>12} {'NumPy':>12} {'C++ Vector':>12} {'Py/C++':>12}")

for n, pt, nt, ct in zip(
    SIZES,
    python_times,
    numpy_times,
    cpp_times,
):
    print(
        f"{n:>10} "
        f"{pt:>12.6e} "
        f"{nt:>12.6e} "
        f"{ct:>12.6e} "
        f"{pt/ct:>12.2f}"
    )