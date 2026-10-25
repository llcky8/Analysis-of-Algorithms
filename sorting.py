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


if __name__ == "__main__":
    print(merge_sort([5, 3, 8, 1]))
    print(radix_sort([5, 3, 8, 1]))
