
import random
import time


N = 12000
MIN_V = 0
MAX_V = 20000 
SEED = 42
random.seed(SEED)
datos = [random.randint(MIN_V, MAX_V) for _ in range(N)]


def heapsort(arr):
    n = len(arr)

    def heapify(n, i):
        m = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and arr[l] > arr[m]:
            m = l
        if r < n and arr[r] > arr[m]:
            m = r
        if m != i:
            arr[i], arr[m] = arr[m], arr[i]
            heapify(n, m)

   
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
   
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr  


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    p = arr[random.randint(0, len(arr) - 1)]
    menores = [x for x in arr if x < p]
    iguales  = [x for x in arr if x == p]
    mayores = [x for x in arr if x > p]
    return quicksort(menores) + iguales + quicksort(mayores)


def counting_sort(arr, max_value=None):
    if not arr:
        return []
    if min(arr) < 0:
        raise ValueError("CountingSort aquí solo acepta enteros no negativos.")
    k = max_value if max_value is not None else max(arr)
    conteo = [0] * (k + 1)
    for x in arr:
        conteo[x] += 1
    total = 0
    for i in range(len(conteo)):
        conteo[i], total = total, total + conteo[i]
    out = [0] * len(arr)
    for x in arr:
        out[conteo[x]] = x
        conteo[x] += 1
    return out


def medir(nombre, func, **kwargs):
    arr = list(datos)  
    t0 = time.perf_counter()
    if func is heapsort:
        func(arr)                 
        res = arr
    elif func is counting_sort:
        res = func(arr, **kwargs) 
    else:
        res = func(arr)           
    t1 = time.perf_counter()
    return nombre, (t1 - t0) * 1000.0, res

print("\n=== Medición de Eficiencia Temporal (n=12,000) ===")

nomb, ms, r1 = medir("HeapSort", heapsort)
print(f"{nomb:28s} -> {ms:8.3f} ms")

nomb, ms, r2 = medir("QuickSort (pivote aleatorio)", quicksort)
print(f"{nomb:28s} -> {ms:8.3f} ms")

nomb, ms, r3 = medir("CountingSort", counting_sort, max_value=MAX_V)
print(f"{nomb:28s} -> {ms:8.3f} ms")


ok1 = (r1 == sorted(datos))
ok2 = (r2 == sorted(datos))
ok3 = (r3 == sorted(datos))
print(f"\nVerificación -> HeapSort:{ok1} | QuickSort:{ok2} | CountingSort:{ok3}")
