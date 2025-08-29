# -*- coding: utf-8 -*-
# Ejercicio 1 - Ordenamientos y tiempos (versión estudiante)
# Nota: Código sencillo, con comentarios "de a pie". Sin optimizaciones raras :D

import random
import time

# --------------------------
# Datos de prueba
# --------------------------
N = 12000                  # cantidad de números
RANGO_MIN = 0
RANGO_MAX = 20000          # rango moderado para que CountingSort no se dispare en memoria
SEED = 42
random.seed(SEED)
datos = [random.randint(RANGO_MIN, RANGO_MAX) for _ in range(N)]
verdad = sorted(datos)     # para verificar que ordenamos bien

# --------------------------
# HeapSort (max-heap)
# --------------------------
def heapsort(arr):
    # Lo hacemos in-place. La idea: armar un max-heap y
    # luego ir sacando el máximo al final.
    n = len(arr)

    def heapify(n, i):
        mayor = i
        izq = 2*i + 1
        der = 2*i + 2

        if izq < n and arr[izq] > arr[mayor]:
            mayor = izq
        if der < n and arr[der] > arr[mayor]:
            mayor = der
        if mayor != i:
            arr[i], arr[mayor] = arr[mayor], arr[i]
            heapify(n, mayor)

    # construir heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # sacar de uno en uno y mandar al final
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)

    return arr  # por costumbre, aunque se ordena in-place

# --------------------------
# QuickSort (recursivo, pivote aleatorio)
# --------------------------
def quicksort(arr):
    # Versión simple “de estudiante”: elegir pivote al azar
    # para evitar el peor caso seguido, y usar recursión.
    if len(arr) <= 1:
        return arr
    pivote = arr[random.randint(0, len(arr) - 1)]
    menores = [x for x in arr if x < pivote]
    iguales  = [x for x in arr if x == pivote]
    mayores = [x for x in arr if x > pivote]
    # Se crean listas nuevas (no es in-place, pero es clarito de entender).
    return quicksort(menores) + iguales + quicksort(mayores)

# --------------------------
# CountingSort (para enteros no negativos)
# --------------------------
def counting_sort(arr, max_value=None):
    # Funciona bien cuando los valores son enteros no negativos y
    # el rango (0..k) no es enorme. Si k es gigante, consume memoria.
    if not arr:
        return []
    if min(arr) < 0:
        raise ValueError("CountingSort aquí solo acepta enteros no negativos.")
    k = max_value if max_value is not None else max(arr)
    conteo = [0] * (k + 1)

    # contar ocurrencias
    for x in arr:
        conteo[x] += 1

    # acumular (prefijos) para saber en qué índice va cada número
    total = 0
    for i in range(len(conteo)):
        conteo[i], total = total, total + conteo[i]

    # construir salida
    salida = [0] * len(arr)
    for x in arr:
        salida[conteo[x]] = x
        conteo[x] += 1
    return salida

# --------------------------
# Medición de tiempos
# --------------------------
def medir(nombre, funcion, usa_copia=True, **kwargs):
    if usa_copia:
        arr = list(datos)
    else:
        arr = datos  # no lo usamos así para no dañar "datos"
    t0 = time.perf_counter()
    if funcion is counting_sort:
        resultado = funcion(arr, **kwargs)
    elif funcion is quicksort:
        resultado = funcion(arr)            # retorna nueva lista
    else:
        funcion(arr)                        # heapsort ordena in-place
        resultado = arr
    t1 = time.perf_counter()
    ok = (resultado == verdad)
    return nombre, (t1 - t0) * 1000.0, ok

resultados = []
resultados.append(medir("HeapSort", heapsort))
resultados.append(medir("QuickSort (pivote aleatorio)", quicksort))
resultados.append(medir("CountingSort", counting_sort, max_value=RANGO_MAX))

# --------------------------
# Mostrar resultados
# --------------------------
print("\n=== Ejercicio 1: Medición de Eficiencia Temporal ===")
print(f"n = {N} | rango = [{RANGO_MIN}, {RANGO_MAX}] | seed = {SEED}\n")
for nombre, ms, ok in resultados:
    print(f"{nombre:30s} -> {ms:8.3f} ms | Correcto: {ok}")

# --------------------------
# Mini análisis (≥ 5 líneas)
# --------------------------
analisis = """

print(analisis)
