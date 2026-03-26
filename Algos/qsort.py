def qsort(arr):
    if len(arr) <= 1:
        return arr
    else:
        left = []
        right = []
        pivot = arr.pop()
        for x in arr:
            if arr[x] < pivot:
                left.append(arr[x])
            else:
                right.append(arr[x])
    return qsort(left).append(pivot).append(qsort(right))


print(qsort([1, 0, -1, 14]))
