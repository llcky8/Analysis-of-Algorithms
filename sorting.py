import random


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def counting_sort_by_digit(arr, exp):
    buckets = [[] for _ in range(10)]
    for num in arr:
        digit = (num // exp) % 10
        buckets[digit].append(num)
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


def radix_sort(arr):
    if not arr:
        return []
    max_digits = len(str(max(arr)))
    result = arr[:]
    exp = 1
    for _ in range(max_digits):
        result = counting_sort_by_digit(result, exp)
        exp *= 10
    return result


def is_ascending(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def same_multiset(a, b):
    return sorted(a) == sorted(b)  # встроенный sort тут разрешён — это просто сверка, не наш алгоритм


def generate_dataset(n, seed):
    rng = random.Random(seed)
    return [rng.randint(0, 9_999_999) for _ in range(n)]


SIZES = [1000, 5000, 10000, 50000, 100000]


if __name__ == "__main__":
    print(merge_sort([5, 3, 8, 1]))
    print(radix_sort([5, 3, 8, 1]))

    test_cases = {
        "empty": [],
        "one value": [42],
        "repeated values": [5, 2, 5, 2, 5, 0],
        "already sorted": [1, 2, 3, 4, 5],
        "reverse order": [9, 7, 5, 3, 1],
    }

    for name, data in test_cases.items():
        for sort_name, sort_fn in [("merge_sort", merge_sort), ("radix_sort", radix_sort)]:
            result = sort_fn(data)
            ok_order = is_ascending(result)
            ok_values = same_multiset(result, data)
            print(f"{name} / {sort_name}: order={ok_order}, values={ok_values}")

    datasets = {n: generate_dataset(n, seed=1000 + n) for n in SIZES}

    for n, data in datasets.items():
        print(f"n={n}, seed={1000 + n}, first 5: {data[:5]}")
