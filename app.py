from flask import Flask, render_template, request, jsonify
import random
import time
from multiprocessing import Pool

app = Flask(__name__)


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
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def parallel_merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    with Pool(processes=2) as pool:
        left, right = pool.map(
            merge_sort,
            [arr[:mid], arr[mid:]]
        )

    return merge(left, right)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/benchmark", methods=["POST"])
def benchmark():

    size = int(request.json["size"])

    arr = [random.randint(1, 1000000) for _ in range(size)]

    start = time.perf_counter()
    merge_sort(arr.copy())
    normal_time = time.perf_counter() - start

    start = time.perf_counter()
    parallel_merge_sort(arr.copy())
    parallel_time = time.perf_counter() - start

    speedup = round(normal_time / parallel_time, 2)

    return jsonify({
        "normal": round(normal_time, 6),
        "parallel": round(parallel_time, 6),
        "speedup": speedup
    })


if __name__ == "__main__":
    app.run(debug=True)
