from pprint import pprint as pp
import random
from time import time
from datetime import datetime

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

#test = [[('a', 'd'), ('f', 'b'), ('c', 'e')], [('f', 'd'), ('c', 'b'), ('e', 'a')], [('d', 'b'), ('c', 'a'), ('e', 'f')], [('a', 'b'), ('d', 'e'), ('f', 'c')], [('a', 'f'), ('b', 'e'), ('c', 'd')]]
#pp(test)

#nsquadre

n=int(input("Inserire il numero di squadre che partecipano al campionato:"))


while (n == 0 or n <= 0 or n%2!=0):
    print ("devi inserire un numero di squadre > 0 e pari")
    n=int(input("Inserire il numero di squadre che partecipano al campionato:"))
    
print("Hai inserito",n,"squadre")
list_squadre=[]
num_sq=0

while num_sq < n:
    
    nome_sq=input("Inserire il nome della squadra oppure premi 0 per terminare")
    if nome_sq =="0":
        exit (-1)
    else:
        list_squadre.append(nome_sq)
        num_sq +=1
            
print(list_squadre)
#weeks sono le giornate del campionato, calcolate a meta' perche' il campionato e' a specchio (double round robin)
weeks=n-1
print("il numero delle giornate da cui sara' composto il tuo campionato e':", weeks)    

print ('''I match saranno presentati in questa forma Match1(TeamHome,TeamAway) 
e il nostro obiettivo e' quello di ottenere una schedulazione col numero minimo di rotture
che secondo le stime di Schreuder sono al meglio : numero di squadre-2, in questo caso :''',n-2, 
'''Vediamo se riusciamo ad avvicinarci a quel numero''')
#le rotture sono invece nulle nel caso di squadre DISPARI(perche' sostituisco la rottura con una squadra fasulla di riposo)
#https://www.sciencedirect.com/science/article/pii/0166218X92902526?ref=cra_js_challenge&fr=js
#http://cse.unl.edu/~choueiry/Documents/Regin/minbreak.pdf
#http://www.dcs.gla.ac.uk/~pat/jchoco/boatAllocation/papers/Round%20Robin%20Scheduling%20-%20A%20Survey.pdf per terminologie varie
'''iniziamo con la struttura delle varie soluzioni di scheduling
si e' scelto di usare una matrice v=[m1,m2..mn] ogni match contiene le informazioni relative a quel match M12(juve,inter)
in cui ogni riga corrisponde al numero di giornata

generiamo inizialmente un vicinato, ovvero delle soluzioni ammissibili ma non ottime
utilizziamo un approccio first generate, then schedule (la giornata) ovvero prima genero gli incontri e poi assegno il numero di giornate
rappresentate dalle righe della matrice di soluzioni di scheduling
'''
''' eventualmente si possono utilizzare delle mosse di swap parziale delle giornate che pero' generano delle soluzioni non amissibili, da ripristinare

'''

gamesinaweek=n//2
totalgames=n-1
#il primo requisito e'che una squadra non possa giocare contro se stessa
#il secondo requisito e' che durante la meta' di campionato calcolata due squadre si incontrino una sola volta, in casa o fuori.
#il terzo requisito e' che in una giornata si devono disputare n/2 incontri totali
#funzione che crea gli accppiamenti usando l'algoritmo Round Robin https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
def make_day(num_teams, day):
     
    assert not num_teams % 2, "Il numero delle squadre deve essere pari!"
    # generate list of teams
    #lst = list(range(1, num_teams + 1))
    lst=list_squadre
    # rotate
    day %= (num_teams - 1)  # clip to 0 .. num_teams - 2
    if day:                 # if day == 0, no rotation is needed (and using -0 as list index will cause problems)
        lst = lst[:1] + lst[-day:] + lst[1:-day]
    # pair off - zip the first half against the second half reversed
    half = num_teams // 2
    return list(zip(lst[:half], lst[half:][::-1]))
#funzione che costruisce la matrice degli incontri in cui ogni riga e' un numero di giornata
def make_schedule(num_teams):
    """
    Funzione che genera il calendario
    """
    # number of teams must be even
    if num_teams % 2:
        num_teams += 1  # add a dummy team for padding
    # build first round-robin
    schedule = [make_day(num_teams, day) for day in range(num_teams - 1)]
    return schedule 

schedule=make_schedule(n)

max_swap_coppie = 10*n
max_swap_righe = n
soglia = 0

t1 = time()
lista_sol_bilanciata = metaeuristica_bilanciata(schedule, max_swap_coppie, max_swap_righe, soglia)
t2 = time()
lista_sol_random = metaeuristica_random(schedule, list_squadre, max_swap_coppie, max_swap_righe, soglia)
t3 = time()

now = datetime.now()
timestamp = int(datetime.timestamp(now))

name_b = "out_bilanciata_" + str(n) + "_" + str(max_swap_coppie) + "_" + str(max_swap_righe) + "_" + str(timestamp) + ".txt"
name_r = "out_random_" + str(n) + "_" + str(max_swap_coppie) + "_" + str(max_swap_righe) + "_"  + str(timestamp) + ".txt"

fout_b = open(name_b,"w")
fout_r = open(name_r,"w")

print("Soluzioni metaeuristica bilanciata", file=fout_b)
print("soluzioni trovate: ", len(lista_sol_bilanciata), file=fout_b)
print("tempo d'esecuzione: ", t2-t1, file=fout_b)
for sol in lista_sol_bilanciata:
    for s in sol:
        print(s,file=fout_b)
    print(conta_breaks(sol),file=fout_b)

sol_costo_minimo, costo_minimo = soluzione_costo_minimo(lista_sol_bilanciata)
print("soluzione(i) di costo minore (costo soluzione {0} - numero soluzioni {1}):".format(costo_minimo, len(sol_costo_minimo)),file=fout_b)
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
print("soluzione(i) di costo minore (costo soluzione {0} - numero soluzioni {1}):".format(costo_minimo, len(sol_costo_minimo)),file=fout_r)
for sol_min in sol_costo_minimo:
    for s_min in sol_min:
        print(s_min,file=fout_r)
    print("---",file=fout_r)