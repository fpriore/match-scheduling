import random
from pprint import pprint as pp


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
'''
list_squadre2=list_squadre.copy()

squadre_comb=[]
giornata=0
for element1 in list_squadre:
    for element2 in list_squadre2:
        if element1!=element2:   
            squadre_comb.append([element1,element2,giornata])           
            
print(squadre_comb)
squadre_swap=squadre_comb.copy()
                
swapsquad(squadre_swap,0,1)
print(squadre_swap)
inputl = list_squadre2
incontri = sum([list(map(list, combinations(inputl, 2)))], []) #Incontri e' la lista (Team1,Team2,0) con giornata nulla'''

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

      
#pp('Ecco la schedule generata col round robin:')
#pp(schedule)
#genero una copia dello scheduling attuale per introdurre una randomizzazione sul punto di partenza della ricerca,
# in modo da rimanere indipendente dall'ordine di inserimento delle squadre
#schedule_shuf=schedule.copy()
            
#random.shuffle(schedule_shuf)
#pp('Scheduling shuffled:')
#pp(schedule_shuf)
                                    
'''mentre avremo una funzione obiettivo da minimizzare che assegna un punteggio ogni qualvolta riscontri che
una stessa squadra ha giocato in due match consecutivi entrambe le partite in casa o fuori???

l'idea e' quella di partire da una soluzione ammissibile, assegnarle un punteggio sulla base del numero di rotture riscontrate e 
 adottare la mossa 1 (swap di due Teams) sulla squadra che mi crea piu' problemi, ovvero quella che presenta un piu' alto numero di rotture.
Se dopo TOT iterazioni il valore delle rotture non migliora, mi sposto su un altro intorno effettuando la mossa 2 ( swap random di righe)
 e riappplicando la mossa 1 con gli stessi criteri. Nel frattempo mantengo in memoria una lista dei ToT migliori scheduling trovati finora.
 ALla fine restituisco la sol in cima alla lista che sara' la migliore riscontrata
'''
''' si proveranno anche diverse alternative, ovvero si applichera' la meta euristica proposta sopra ad una soluzione inizialmente perturbata
 con mossa 2 per rendere la soluzione indipendente dall'algoritmo di costruzione della sol ammissibile, confrontando i risultati finali attraverso grafici'''
#funzione che scambia una coppia di Teams (Inter,Juve)-->(Juve,Inter)

def swapsquad(listtoswap,pos1,pos2):    
    for s in listtoswap:
        s[pos1],s[pos2]=s[pos2],s[pos1]

#funzione che conta il numero di rotture di ogni sq e le somma
def contabreaks(lista1,verbose=False):
    rotture=0
    squadre_rotture = []
    rotture_per_squadre = []
    for s,s1 in zip(lista1,lista1[1:]):
        for match in s:
            for match1 in s1:
                if match[0]==match1[0]:
                    rotture+=1
                    squadre_rotture.append(match[0])
                    if verbose:
                        print("rottura in casa: ",match[0])
                if match[1]==match1[1]:
                    rotture+=1
                    squadre_rotture.append(match[1])
                    if verbose:
                        print("rottura fuori casa: ",match[1])
            if verbose:
                print("--nuova giornata--")
    for sr in squadre_rotture:
        cnt = squadre_rotture.count(sr)
        if [sr,cnt] not in rotture_per_squadre:
            rotture_per_squadre.append([sr,cnt])
    rotture_per_squadre.sort(key=lambda tup: tup[1], reverse=True) 


    return rotture, rotture_per_squadre             
    
num_rott=100
nrotture=0
listtmp=[]

def scambiamaxmin(listasw):
    listtmp=contabreaks(listasw, verbose=False)
    if num_rott> listtmp[0]:
        sqprobl=listtmp[1][0][0]
        sqmenoprobl=listtmp[1][-1][0]
        
        listprob=(sqprobl,sqmenoprobl)
        listprobinv=(sqmenoprobl,sqprobl)
        
        for e in listasw:
            if listprob in e:
                e.remove(listprob)
                e.append(listprobinv)
        
    return listasw

soglia=3*(num_sq-2)
sogliaint=int(soglia)

def metaeurbil():
        
    maxcontswapcoppie=100
    maxcontswaprighe=100
    
    listabestsch=[]
    schedule=make_schedule(n)
    #parto da soluzione non randomizzata ottenuta col cirle method, da provare i risultati partendo da random 
    tuplasol=contabreaks(schedule, verbose=False)
    pp(tuplasol)
    pp(schedule)
    #if tuplasol[0] <= sogliaint:
    
    sogliaint = tuplasol[0]
    listabestsch.append([schedule,tuplasol[0], tuplasol[1]])
    
    
    for i in range(maxcontswaprighe):
        for l in range ( maxcontswapcoppie):
                
            listascambiata=scambiamaxmin(schedule)
            
            tuplasolmaxmin=contabreaks(listascambiata, verbose=False)
            if tuplasolmaxmin[0] <= sogliaint:    
                if [listascambiata,tuplasolmaxmin[0], tuplasolmaxmin[1]] not in listabestsch:
                    listabestsch.append([listascambiata,tuplasolmaxmin[0], tuplasolmaxmin[1]])

            
        random.shuffle(listascambiata)
            
    listabestsch.sort(key=lambda tup: tup[1], reverse=True)
    return listabestsch
            
#funzione che scambia squadre con max/min rotture
#conto i break sullo schedule scambiato
#controllo che la somma delle rotture sia migliore
#se dopo 10 iterazioni non migliora rispetto al valore soglia(?) cioe' se resta sempre soglia
#faccio mossa di scambio righe random.shuffle(schedule) e riparto da funz1
#se ho scambiato 10 volte le righe, mi fermo e prendo la miglior soluzione trovata che sta sottosoglia (si spera)
                    
migliorisol=metaeurbil()       
pp(migliorisol)   
print("sol trovate", len(migliorisol)) 
