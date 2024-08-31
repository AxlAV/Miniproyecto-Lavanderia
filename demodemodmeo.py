lista = [15, 33, 42, 8, 22, 21, 10]

for i in range(1,len(lista)):
    cont = 1
    while i > 0 and lista[i-1] > lista[i]:
        
        key = lista[i]
        lista[i] = lista[i-1]
        lista[i-1] = key
        i = i - 1  
        cont += 1
    print (cont)
print(lista)
