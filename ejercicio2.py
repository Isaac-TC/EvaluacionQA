
def permutaciones(lista):
    
    if len(lista) == 1:
        return [lista]
    resultado = []
    for i in range(len(lista)): 
        elem = lista[i]
        resto = lista[:i] + lista[i+1:]
        for p in permutaciones(resto):
            resultado.append([elem] + p)
    return resultado

print("Permutaciones de [1,2,3]:")
for p in permutaciones([1,2,3]):
    print(p)

def es_palindromo(palabra):
    palabra = palabra.lower()
    if len(palabra) <= 1:
        return True
    if palabra[0] != palabra[-1]:
        return False
    return es_palindromo(palabra[1:-1])


print("\n¿'radar' es palíndromo?", es_palindromo("radar"))
print("¿'Python' es palíndromo?", es_palindromo("Python"))
print("¿'oso' es palíndromo?", es_palindromo("oso"))
