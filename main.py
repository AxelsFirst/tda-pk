import math
import numpy
from itertools import combinations
from scipy.sparse import dok_matrix
from operator import add

import networkx
from scipy.spatial import distance
from itertools import product

# Klasa punktów leżących na przestrzeni euklidesowej R^n
class Punkt:

    # Skomentowane by to zaimplementować poza klasą
    # # Metoda tworzy listę współrzędnych punktu,
    # # może zostać użyta by od nowa wpisać współrzędne
    # def ustaw_wsp(self):
    #     self.lista_wspolrzednych = []
    #     for i in range(self.wymiar):
    #         self.wsp.append(input('Wypisz {}-tą współrzędną: '.format(i)))

    # Metoda przypisuje pozostałe atrybuty punktu
    def __init__(self, nazwa, wymiar, lista_wspolrzednych):
        self.nazwa = nazwa
        self.wymiar = wymiar
        self.lista_wspolrzednych = lista_wspolrzednych
    
    # # Metoda najprawdopodobniej niepotrzebna,
    # # zwraca bądź drukuje współrzędne punktu
    # def wypisz_wsp(self, wydrukuj = False):
    #     if wydrukuj == True:
    #         print(self.lista_wspolrzednych)
    #     else:
    #         return self.lista_wspolrzednych

    # Metoda zmienia jedną współrzędną punktu o określonym indeksie
    def zmien_wsp(self, indeks, wartosc):
        self.lista_wspolrzednych[indeks] = wartosc

    # Metoda zmienia wszystkie współrzędne punktu
    def ustaw_wsp(self, lista_wspolrzednych, nowa_lista_wspolrzednych):
        self.lista_wspolrzednych = nowa_lista_wspolrzednych

    # Metoda sprzężona dodawania punktów po współrzędnych (a + b)
    def __add__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wspolrzednych[i] + other.lista_wspolrzednych[i])
        return suma

    # Metoda sprzężona dodawania punktów po współrzędnych (a += b)
    def __iadd__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wspolrzednych[i] + other.lista_wspolrzednych[i])
        return suma

    # Metoda sprzężona odejmowania punktów po współrzędnych (a - b)
    def __sub__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wspolrzednych[i] - other.lista_wspolrzednych[i])
        return roznica

    # Metoda sprzężona odejmowania punktów po współrzędnych (a -= b)
    def __isub__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wspolrzednych[i] - other.lista_wspolrzednych[i])
        return roznica

    # Metoda sprzężona mnożenia punktów po współrzędnych (a * b)
    def __mul__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wspolrzednych[i] * other.lista_wspolrzednych[i])
        return iloczyn
    
    # Metoda sprzężona mnożenia punktów po współrzędnych (a *= b)
    def __imul__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wspolrzednych[i] * other.lista_wspolrzednych[i])
        return iloczyn

    # Metoda sprzężona dzielenia punktów po współrzędnych (a * b)
    def __div__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wspolrzednych[i] / other.lista_wspolrzednych[i])
        return iloraz

    # Metoda sprzężona dzielenia punktów po współrzędnych (a *= b)
    def __idiv__(self, other):
        if self.wymiar!=other.wymiar:
            raise IndexError
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wspolrzednych[i] / other.lista_wspolrzednych[i])
        return iloraz

    # Metoda zwraca normę euklidesową punktu
    def norma(self):
        suma = 0
        for wsp in self.lista_wspolrzednych:
            suma += wsp**2
        return math.sqrt(suma)

    # Metoda zwraca metrykę euklidesową punktu względem innego punktu
    def metryka(self, other):
        return self.norma(self - other)

# # Klasa zbioru punktów, nazwana grafem dla uproszczenia
# class graf:

#     # Metoda tworzy punkty i od razu dodaje je do listy punktów,
#     # może zostać użyta by od nowa wpisać punkty
#     def ustaw_liste_punkt(self):
#         lista_punkt = []
#         for i in range(self.liczba_punkt):
#             nazwa_punkt = input('Podaj nazwę punktu: ')
#             punkt(nazwa_punkt, self.wymiar)
#             lista_punkt.append(nazwa_punkt)
#         self.lista_punkt = lista_punkt

#     # Metoda ustawia pozostałe atrybuty "grafu"
#     def __init__(self, liczba_punkt, wymiar):
#         self.liczba_punkt = liczba_punkt
#         self.wymiar = wymiar
#         self.ustaw_liste_punkt()

# Klasa kompleksu Vietorigo-Ripsa
class Kompleks_Vietorigo_Ripsa:

    # Obiekt przyjmuje:
    # listę punktów, 
    # epsilon będący maksymalną możliwą odległością do zarejestrowania krawędzi,
    # własne oznaczenia wierzchołków,
    # własną metrykę (tymczasowe, bo zaimplementowane także w klasie punktów)
    def __init__(self, punkty, epsilon, oznaczenia=None, metryka=distance.euclidean):
        self.punkty = punkty
        self.epsilon = epsilon

        # Jeśli nie podano oznaczeń funkcja sama ponumeruje
        self.oznaczenia = range(len(self.punkty)) if oznaczenia==None or len(oznaczenia)!=len(self.punkty) else oznaczenia
        self.metryka = metryka

        # Utworzenie grafu
        self.graf = self.utworz_graf()

        # # Szukanie sympleksów
        # self.znajdz_sympleksy(map(tuple, list(networkx.find_cliques(self.graf))))

        # Szukanie sympleksów (bez zewnętrznej metody)
        lista_sympleksow = map(tuple, list(networkx.find_cliques(self.graf)))
        self.lista_sympleksow = map(lambda sympleks: tuple(sorted(sympleks)), lista_sympleksow)

    # Metoda tworzy graf nieskierowany
    def utworz_graf(self):

        # Utworzenie obiektu grafu nieskierowanego
        graf = networkx.Graph()

        # Utworzenie wierzchołków z oznaczeń,
        # każdemu oznaczeniowi przyporządkowany jest wierzchołek
        graf.add_nodes_from(self.oznaczenia)

        # Przyporządkowanie wierzchołkom właściwe punkty
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków
        #   jeśli oznaczenia wierzchołków są różne
        #       oblicz odległość pomiędzy punktami,
        #       jeśli odległość jest mniejsza niż przyjęte epsilon
        #           utwórz bok prowadzący z jednego wierzchołka do drugiego
        # product() można zastąpić podwójną pętlą
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1]!=para[1][1]:
                # # Wersja dla metryki z distance.euclidean
                # odleglosc = self.metryka(para[0][0], para[1][0])

                # Wersja dla metryki z klasy punktów
                odleglosc = para[0][0].metryka(para[1][0])
                if odleglosc < self.epsilon:
                    graf.add_edge(para[0][1], para[1][1])
        
        return graf

    # # Początkowa metoda do szukania sympleksów
    # def znajdz_sympleksy(self, lista_sympleksow):
    #     self.lista_sympleksow = map(lambda sympleks: tuple(sorted(sympleks)), lista_sympleksow)
    #     self.lista_scian = self.wypisz_sciany()

    # Metoda zwraca wszystkie sympleksy kompleksu
    def wypisz_sciany(self):
        zbior_scian = set()
        for sympleks in self.lista_sympleksow:
            liczba_wierzcholkow = len(sympleks)
            for wymiar_sciany in range(liczba_wierzcholkow, 0, -1):
                for sciana in combinations(sympleks, wymiar_sciany):
                    zbior_scian.add(sciana)
        return zbior_scian

    # Metoda zwraca wszystkie sympleksy kompleksu o określonym wymiarze
    # (na razie nie wiem dlaczego ma być tu 'wymiar + 1')
    def wypisz_sciany_danego_wymiaru(self, wymiar):
        return filter(lambda sciana: len(sciana)==wymiar + 1, self.zbior_scian)

# Tutaj zaczyna się właściwy program
if __name__ == "__main__":

    # Krótka informacja o programie
    print('Program służy do obliczania kompleksu Vietorigo-Ripsa w przestrzeni euklidesowej.')
    print('Autorami są Gibała Alex oraz Musielak Piotr.')
    
    # Tutaj użytkownik wpisuje liczbę punktów
    # Pętla została umieszczona w celu upewnienia się, że podano liczbę oraz czy jest ona poprawna
    # Ilość punktów musi być niezerową liczbą naturalną
    while True:
        try:
            print('Ile jest punktów danych?')
            liczba_punktow = int(input('Wpisz tutaj: '))
            if liczba_punktow <= 0:
                print('Liczba punktów danych musi być dodatnia!')
            else:
                break
        except:
            print('Niepoprawna odpowiedź!')
            print('Podaj niezerową liczbę naturalną!')
        
    # Tutaj użytkownik oznajmia czy zamierza stosować własne oznaczenia punktów
    # W przypadku braku chęci progra samemu będzie numerować punkty
    while True:
        print('Czy zamierzasz stosować własne oznaczenia nazw?')
        wlasne_oznaczenia = input('Wpisz tutaj [TAK/nie]: ')
        if wlasne_oznaczenia.lower() == 'tak' or wlasne_oznaczenia.lower() == 't' or wlasne_oznaczenia == '':
            wlasne_oznaczenia = True
            break
        elif wlasne_oznaczenia.lower() == 'nie' or wlasne_oznaczenia.lower() == 'n':
            wlasne_oznaczenia = False
            break
        else:
            print('Niepoprawna odpowiedź!')
            print('Napisz "Tak" lub "Nie".')

    # Tutaj użytkownik oznajmia wymiar przestrzeni euklidesowej R^n, do której należą punkty
    # Wymiar przestrzeni musi być niezerową liczbą naturalną
    while True:
        try:
            print('Jaki jest wymiar rozważanej przestrzeni euklidesowej R^n?')
            wymiar = int(input('Wpisz tutaj: '))
            if wymiar <= 0:
                print('Liczba punktów danych musi być dodatnia!')
            else:
                break
        except:
            print('Niepoprawna odpowiedź!')
            print('Podaj niezerową liczbę naturalną!')

    # Tutaj użytkownik wypisuje wszystkie punkty
    # W przypadku, gdy użytkownik pomyli się, to program poprosi o ponownie wpisanie
    # danych, bez potrzeby restartowania aplikacji.
    if wlasne_oznaczenia == True:
        print('Teraz wypisz nazwy punktów wraz z współrzędnymi.')
    else:
        print('Teraz wypisz współrzędne wszystkich wierzchołków.')

    lista_punktow = list()

    for indeks_punktu in range(liczba_punktow):

        # Tutaj użytkownik wpisuje własne oznaczenie punktu
        if wlasne_oznaczenia == True:
            while True:
                nazwa_punktu = str(input('Wpisz nazwę punktu: '))
                if isinstance(nazwa_punktu, Punkt):
                    print('Niepoprawna odpowiedź!')
                    print('Oznaczenia nie mogą się powtarzać!')
                else:
                        break

        # Numerowanie od 1 z przyjętego standardu, że współrzędne wymienia się jako (x_1, x_2, ..., x_n)
        lista_wspolrzednych = list()
        for indeks_wspolrzednej in range(1, wymiar+1):
            while True:
                try:
                    lista_wspolrzednych.append(float(input('Wpisz współrzędną x{}: '.format(indeks_wspolrzednej))))
                    break
                except:
                    print('Niepoprawna odpowiedź!')
                    print('Podaj liczbę rzeczywistą!')
            
        # Tutaj tworzymy punkt
        if wlasne_oznaczenia == False:
            Punkt(indeks_punktu, wymiar, lista_wspolrzednych)
        else:
            Punkt(nazwa_punktu, wymiar, lista_wspolrzednych)
        lista_punktow.append(lista_wspolrzednych)
    
    print('Graf się tworzy...')
