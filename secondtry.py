from pprint import pprint as pp
import random
from time import time
test = [[('a', 'd'), ('f', 'b'), ('c', 'e')], [('f', 'd'), ('c', 'b'), ('e', 'a')], [('d', 'b'), ('c', 'a'), ('e', 'f')], [('a', 'b'), ('d', 'e'), ('f', 'c')], [('a', 'f'), ('b', 'e'), ('c', 'd')]]
pp(test)

def inverti_coppie(campionato,squadra_1,squadra_2):
    scambio_avvenuto = False
    for c in campionato:
        if (squadra_1,squadra_2) in c:
            c.remove((squadra_1,squadra_2))
            c.append((squadra_2,squadra_1))
            scambio_avvenuto = True
    return campionato, scambio_avvenuto

def conta_breaks(campionato):
    breaks = 0
    squadre_rotture = []
    rotture_per_squadre = []

    for giornata_1,giornata_2 in zip(campionato,campionato[1:]): # compara il campionato due giornate alla volta
        for match_1 in giornata_1:
            for match_2 in giornata_2:
                if match_1[0] == match_2[0]:
                    breaks += 1
                    squadre_rotture.append(match_1[0])
                if match_1[1] == match_2[1]:
                    squadre_rotture.append(match_1[1])
                    breaks += 1

    for sr in squadre_rotture:
        cnt = squadre_rotture.count(sr)
        if [sr,cnt] not in rotture_per_squadre:
            rotture_per_squadre.append([sr,cnt])
    rotture_per_squadre.sort(key=lambda tup: tup[1], reverse=True) 

    return breaks, rotture_per_squadre


def scambia_max_min(campionato):
    breaks, rps = conta_breaks(campionato)
    squadra_max = rps[0][0]
    squadra_min = rps[-1][0]

    campionato, scambio_avvenuto = inverti_coppie(campionato,squadra_max,squadra_min)
    if not scambio_avvenuto:
        campionato, scambio_avvenuto = inverti_coppie(campionato,squadra_min,squadra_max)
    
    return campionato

def scambia_random(campionato, nomi_squadre):
    squadra_1 = ""
    squadra_2 = ""
    while squadra_1 == squadra_2:
        squadra_1 = nomi_squadre[random.randint(0,len(nomi_squadre)-1)]
        squadra_2 = nomi_squadre[random.randint(0,len(nomi_squadre)-1)]
    
    campionato, scambio_avvenuto = inverti_coppie(campionato,squadra_1,squadra_2)
    if not scambio_avvenuto:
        campionato, scambio_avvenuto = inverti_coppie(campionato,squadra_2,squadra_1)

    return campionato

def metaeuristica_bilanciata(campionato,max_swap_coppie,max_swap_righe,soglia=0):
    '''
    Input: campionato\n
    Output: lista_soluzioni - la lista di soluzioni ottenute
    '''
    campionato_meta = campionato.copy()
    lista_soluzioni = []
    nbreaks, rps = conta_breaks(campionato_meta)
    if soglia == 0:
        soglia = nbreaks
    
    for i in range(max_swap_righe):
        for j in range(max_swap_coppie):
            campionato_meta = scambia_max_min(campionato_meta)
            nbreaks, rps = conta_breaks(campionato_meta)
            if nbreaks <= soglia:
                if campionato_meta not in lista_soluzioni:
                    lista_soluzioni.append(campionato_meta.copy())
                
        random.shuffle(campionato_meta)

    return lista_soluzioni

def metaeuristica_random(campionato, nomi_squadre, max_swap_coppie,max_swap_righe,soglia=0):
    '''
    Input: campionato\n
    Output: lista_soluzioni - la lista di soluzioni ottenute
    '''
    campionato_meta = campionato.copy()
    lista_soluzioni = []
    nbreaks, rps = conta_breaks(campionato_meta)
    if soglia == 0:
        soglia = nbreaks
    
    for i in range(max_swap_righe):
        for j in range(max_swap_coppie):
            campionato_meta = scambia_random(campionato_meta,nomi_squadre)
            nbreaks, rps = conta_breaks(campionato_meta)
            if nbreaks <= soglia:
                if campionato_meta not in lista_soluzioni:
                    lista_soluzioni.append(campionato_meta.copy())
                
        random.shuffle(campionato_meta)

    return lista_soluzioni

def soluzione_costo_minimo(lista_soluzioni):
    sol_costo_minimo = []
    costo_minimo, rps = conta_breaks(lista_soluzioni[0])
    sol_costo_minimo.append(lista_soluzioni[0])
    for sol in lista_soluzioni[1:]:
        breaks, rps = conta_breaks(sol)
        if breaks < costo_minimo:
            costo_minimo = breaks
            sol_costo_minimo.clear()
            sol_costo_minimo.append(sol)
        elif breaks == costo_minimo:
            sol_costo_minimo.append(sol)
    return sol_costo_minimo, costo_minimo


nomi_squadre = ['a','b','c','d','e','f']

max_swap_coppie = 10
max_swap_righe = 10
soglia = 0

t1 = time()
lista_sol_bilanciata = metaeuristica_bilanciata(test, max_swap_coppie, max_swap_righe, soglia)
t2 = time()
lista_sol_random = metaeuristica_random(test, nomi_squadre, max_swap_coppie, max_swap_righe, soglia)
t3 = time()

fout_b = open("out_bilanciata.txt","w")
fout_r = open("out_random.txt","w")

print("Soluzioni metaeuristica bilanciata", file=fout_b)
print("soluzioni trovate: ", len(lista_sol_bilanciata), file=fout_b)
print("tempo d'esecuzione: ", t2-t1, file=fout_b)
for sol in lista_sol_bilanciata:
    for s in sol:
        print(s,file=fout_b)
    print(conta_breaks(sol),file=fout_b)

sol_costo_minimo, costo_minimo = soluzione_costo_minimo(lista_sol_bilanciata)
print("soluzione(i) di costo minore (costo soluzione {0}):".format(costo_minimo),file=fout_b)
for sol_min in sol_costo_minimo:
    for s_min in sol_min:
        print(s_min,file=fout_b)
    print("---",file=fout_b)


print("Soluzioni metaeuristica random", file=fout_r)
print("soluzioni trovate: ", len(lista_sol_bilanciata), file=fout_r)
print("tempo d'esecuzione: ", t3-t2, file=fout_r)
for sol in lista_sol_random:
    for s in sol:
        print(s,file=fout_r)
    print(conta_breaks(sol),file=fout_r)

sol_costo_minimo, costo_minimo = soluzione_costo_minimo(lista_sol_random)    
print("soluzione(i) di costo minore (costo soluzione {0}):".format(costo_minimo),file=fout_r)
for sol_min in sol_costo_minimo:
    for s_min in sol_min:
        print(s_min,file=fout_r)
    print("---",file=fout_r)