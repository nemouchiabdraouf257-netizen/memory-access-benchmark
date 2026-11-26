import csv
import os
import platform
import statistics
import sys
import time


def make_strided_indices(n_elements: int, stride: int) -> list[int]:
    """Precompute strided indices outside the timed traversal loop."""
    indices = []
    idx = 0
    for _ in range(n_elements):
        indices.append(idx)
        idx = (idx + stride) % n_elements
    return indices


def run_sequential(arr: list[int]) -> int:
    total = 0
    for x in arr:
        total += x
    return total


def run_strided(arr: list[int], indices: list[int]) -> int:
    total = 0
    for idx in indices:
        total += arr[idx]
    return total


def main() -> None:
    array_sizes = [2_000, 32_000, 500_000, 4_000_000]
    strides = [1, 8, 16, 64]
    warmup_runs = 3
    measured_runs = 20
    output_path = "results.csv"
    rows = []

    print(
        f"Python: {sys.version.split()[0]} | OS: {platform.platform()} | "
        f"CPUs: {os.cpu_count()} | Warmup: {warmup_runs} | Runs: {measured_runs}"
    )

    for n in array_sizes:
        arr = [i % 1024 for i in range(n)]
        sink = 0

        for stride in strides:
            if stride == 1:
                for _ in range(warmup_runs):
                    sink ^= run_sequential(arr)

                times_ms = []
                for _ in range(measured_runs):
                    t0 = time.perf_counter()
                    sink ^= run_sequential(arr)
                    t1 = time.perf_counter()
                    times_ms.append((t1 - t0) * 1000.0)
            else:
                indices = make_strided_indices(n, stride)
                for _ in range(warmup_runs):
                    sink ^= run_strided(arr, indices)

                times_ms = []
                for _ in range(measured_runs):
                    t0 = time.perf_counter()
                    sink ^= run_strided(arr, indices)
                    t1 = time.perf_counter()
                    times_ms.append((t1 - t0) * 1000.0)

            mean_ms = statistics.mean(times_ms)
            stdev_ms = statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0
            median_ms = statistics.median(times_ms)

            print(
                f"N={n:<9} | stride={stride:<2} | "
                f"mean={mean_ms:8.3f} ms | sd={stdev_ms:7.3f} ms | median={median_ms:8.3f} ms"
            )

            for run_idx, val in enumerate(times_ms, start=1):
                rows.append({
                    "n_elements": n,
                    "stride": stride,
                    "run": run_idx,
                    "elapsed_ms": f"{val:.6f}",
                    "mean_ms": f"{mean_ms:.6f}",
                    "stdev_ms": f"{stdev_ms:.6f}",
                    "median_ms": f"{median_ms:.6f}",
                    "python_version": sys.version.split()[0],
                    "os": platform.platform(),
                })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "n_elements",
            "stride",
            "run",
            "elapsed_ms",
            "mean_ms",
            "stdev_ms",
            "median_ms",
            "python_version",
            "os",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved raw results to {output_path} (checksum sink={sink})")


if __name__ == "__main__":
    main()