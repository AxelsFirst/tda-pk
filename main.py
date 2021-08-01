import math
import numpy as np

# Klasa punktów leżących na przestrzeni euklidesowej R^n
class punkt:

    # Metoda tworzy listę współrzędnych punktu,
    # może zostać użyta by od nowa wpisać współrzędne
    def ustaw_wsp(self):
        self.lista_wsp = []
        for i in range(self.wymiar):
            self.wsp.append(input('Wypisz {}-tą współrzędną: '.format(i)))

    # Metoda przypisuje pozostałe atrybuty punktu
    def __init__(self, nazwa, wymiar):
        self.nazwa = nazwa
        self.wymiar = wymiar
        self.ustaw_wsp()
    
    # Metoda najprawdopodobniej niepotrzebna,
    # zwraca bądź drukuje współrzędne punktu
    def wypisz_wsp(self, wydrukuj = False):
        if wydrukuj == True:
            print(self.lista_wsp)
        else:
            return self.lista_wsp

    # Metoda zmienia jedną współrzędną punktu o określonym indeksie
    def zmien_wsp(self, indeks, wartosc):
        self.lista_wsp[indeks] = wartosc

    # Metoda sprzężona dodawania punktów po współrzędnych (a + b)
    def __add__(self, other):
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wsp[i] + other.lista_wsp[i])
        return suma

    # Metoda sprzężona dodawania punktów po współrzędnych (a += b)
    def __iadd__(self, other):
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wsp[i] + other.lista_wsp[i])
        return suma

    # Metoda sprzężona odejmowania punktów po współrzędnych (a - b)
    def __sub__(self, other):
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wsp[i] - other.lista_wsp[i])
        return roznica

    # Metoda sprzężona odejmowania punktów po współrzędnych (a -= b)
    def __isub__(self, other):
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wsp[i] - other.lista_wsp[i])
        return roznica

    # Metoda sprzężona mnożenia punktów po współrzędnych (a * b)
    def __mul__(self, other):
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wsp[i] * other.lista_wsp[i])
        return iloczyn
    
    # Metoda sprzężona mnożenia punktów po współrzędnych (a *= b)
    def __imul__(self, other):
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wsp[i] * other.lista_wsp[i])
        return iloczyn

    # Metoda sprzężona dzielenia punktów po współrzędnych (a * b)
    def __div__(self, other):
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wsp[i] / other.lista_wsp[i])
        return iloraz

    # Metoda sprzężona dzielenia punktów po współrzędnych (a *= b)
    def __idiv__(self, other):
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wsp[i] / other.lista_wsp[i])
        return iloraz

    # Metoda zwraca normę euklidesową punktu
    def norma(self):
        suma = 0
        for wsp in self.lista_wsp:
            suma += wsp**2
        return math.sqrt(suma)

    # Metoda zwraca metrykę euklidesową punktu względem innego punktu
    def metryka(self, other):
        return self.norma(self - other)

# Klasa zbioru punktów, nazwana grafem dla uproszczenia
class graf:

    # Metoda tworzy punkty i od razu dodaje je do listy punktów,
    # może zostać użyta by od nowa wpisać punkty
    def ustaw_liste_punkt(self):
        lista_punkt = []
        for i in range(self.liczba_punkt):
            nazwa_punkt = input('Podaj nazwę punktu: ')
            punkt(nazwa_punkt, self.wymiar)
            lista_punkt.append(nazwa_punkt)
        self.lista_punkt = lista_punkt

    # Metoda ustawia pozostałe atrybuty "grafu"
    def __init__(self, liczba_punkt, wymiar):
        self.liczba_punkt = liczba_punkt
        self.wymiar = wymiar
        self.ustaw_liste_punkt()
