import csv
import random
import statistics
import time

import matplotlib.pyplot as plt


def merge(left, right, counters=None):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if counters is not None:
            counters["comparisons"] += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        if counters is not None:
            counters["copies"] += 1
    result.extend(left[i:])
    result.extend(right[j:])
    if counters is not None:
        counters["copies"] += len(left[i:]) + len(right[j:])
    return result


def merge_sort(arr, counters=None):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], counters)
    right = merge_sort(arr[mid:], counters)
    return merge(left, right, counters)


def counting_sort_by_digit(arr, exp, counters=None):
    buckets = [[] for _ in range(10)]
    for num in arr:
        digit = (num // exp) % 10
        if counters is not None:
            counters["digit_inspections"] += 1
            counters["placements"] += 1
        buckets[digit].append(num)
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


def radix_sort(arr, counters=None):
    if not arr:
        return []
    max_digits = 7  # фиксировано под диапазон 0..9 999 999
    result = arr[:]
    exp = 1
    for _ in range(max_digits):
        result = counting_sort_by_digit(result, exp, counters)
        if counters is not None:
            counters["copies_back"] += len(result)
        exp *= 10
    return result


def is_ascending(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def same_multiset(a, b):
    return sorted(a) == sorted(b)  # встроенный sort


def generate_dataset(n, seed):
    rng = random.Random(seed)
    return [rng.randint(0, 9_999_999) for _ in range(n)]


SIZES = [1000, 5000, 10000, 50000, 100000]


def benchmark(sort_fn, data, runs=7):
    times = []
    for _ in range(runs):
        arr_copy = data[:]
        start = time.perf_counter()
        sort_fn(arr_copy)
        times.append(time.perf_counter() - start)
    return statistics.median(times)


def count_operations(sort_fn, data, counter_keys):
    counters = {k: 0 for k in counter_keys}
    sort_fn(data[:], counters)
    return counters


if __name__ == "__main__":
    print(merge_sort([5, 3, 8, 1]))
    print(radix_sort([5, 3, 8, 1]))

    test_cases = {
        "empty": [],
        "one value": [42],
        "repeated values": [5, 2, 5, 2, 5, 0],
        "already sorted": [1, 2, 3, 4, 5],
        "reverse order": [9, 7, 5, 3, 1],
        "mixed digit lengths": [9999999, 0, 10, 1000000, 5, 10],
    }

    for name, data in test_cases.items():
        for sort_name, sort_fn in [("merge_sort", merge_sort), ("radix_sort", radix_sort)]:
            result = sort_fn(data)
            ok_order = is_ascending(result)
            ok_values = same_multiset(result, data)
            print(f"{name} / {sort_name}: input={data} -> output={result}, order={ok_order}, values={ok_values}")

    datasets = {n: generate_dataset(n, seed=1000 + n) for n in SIZES}

    for n, data in datasets.items():
        for sort_name, sort_fn in [("merge_sort", merge_sort), ("radix_sort", radix_sort)]:
            result = sort_fn(data)
            ok = len(result) == n and is_ascending(result) and same_multiset(result, data)
            print(f"dataset n={n} / {sort_name}: len={len(result)}, sorted and same values: {ok}")

    for n, data in datasets.items():
        print(f"n={n}, seed={1000 + n}, first 5: {data[:5]}")

    results_time = {}
    results_ops = {}

    for n, data in datasets.items():
        results_time[("merge_sort", n)] = benchmark(merge_sort, data)
        results_time[("radix_sort", n)] = benchmark(radix_sort, data)
        results_ops[("merge_sort", n)] = count_operations(merge_sort, data, ["comparisons", "copies"])
        results_ops[("radix_sort", n)] = count_operations(radix_sort, data, ["digit_inspections", "placements", "copies_back"])

    for key, t in results_time.items():
        print(key, f"{t*1000:.3f} ms, {t*1e9/key[1]:.1f} ns/element")
    for key, ops in results_ops.items():
        print(key, ops)

    ns = SIZES

    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['algorithm', 'n', 'median_time_ms', 'ns_per_record'])
        for n in ns:
            for name in ['merge_sort', 'radix_sort']:
                t_ms = results_time[(name, n)] * 1000
                writer.writerow([name, n, f"{t_ms:.3f}", f"{t_ms*1e6/n:.1f}"])

        f.write('\n')
        writer.writerow(['algorithm', 'n', 'counters'])
        for n in ns:
            for name in ['merge_sort', 'radix_sort']:
                writer.writerow([name, n, results_ops[(name, n)]])

    # время
    merge_times = [results_time[("merge_sort", n)] * 1000 for n in ns]
    radix_times = [results_time[("radix_sort", n)] * 1000 for n in ns]

    plt.figure()
    plt.plot(ns, merge_times, marker='o', label='Merge Sort')
    plt.plot(ns, radix_times, marker='s', label='Radix Sort')
    plt.xlabel('Input size n')
    plt.ylabel('Median elapsed time (ms)')
    plt.title('Elapsed time vs input size')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('time_vs_n.png', dpi=150, bbox_inches='tight')

    # операции merge sort
    merge_comp = [results_ops[("merge_sort", n)]["comparisons"] for n in ns]
    merge_copy = [results_ops[("merge_sort", n)]["copies"] for n in ns]

    plt.figure()
    plt.plot(ns, merge_comp, marker='o', label='Comparisons')
    plt.plot(ns, merge_copy, marker='s', label='Copies')
    plt.xlabel('Input size n')
    plt.ylabel('Operation count')
    plt.title('Merge Sort: operation counts vs input size')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('merge_ops_vs_n.png', dpi=150, bbox_inches='tight')

    # операции radix sort
    radix_insp = [results_ops[("radix_sort", n)]["digit_inspections"] for n in ns]
    radix_place = [results_ops[("radix_sort", n)]["placements"] for n in ns]

    plt.figure()
    plt.plot(ns, radix_insp, marker='o', label='Digit inspections')
    plt.plot(ns, radix_place, marker='s', label='Placements')
    plt.xlabel('Input size n')
    plt.ylabel('Operation count')
    plt.title('Radix Sort: operation counts vs input size')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('radix_ops_vs_n.png', dpi=150, bbox_inches='tight')

    plt.show()
