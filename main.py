import math
import numpy as np

class punkt:
    def ustaw_wsp(self):
        self.lista_wsp = []
        for i in range(self.wymiar):
            self.wsp.append(input('Wypisz {}-tą współrzędną: '.format(i)))

    def __init__(self, nazwa, wymiar):
        self.nazwa = nazwa
        self.wymiar = wymiar
        self.ustaw_wsp()
    
    def wypisz_wsp(self, wydrukuj = False):
        if wydrukuj == True:
            print(self.lista_wsp)
        else:
            return self.lista_wsp

    def zmien_wsp(self, indeks, wartosc):
        self.lista_wsp[indeks] = wartosc

    def __add__(self, other):
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wsp[i] + other.lista_wsp[i])
        return suma

    def __iadd__(self, other):
        suma = []
        for i in range(self.wymiar):
            suma.append(self.lista_wsp[i] + other.lista_wsp[i])
        return suma

    def __sub__(self, other):
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wsp[i] - other.lista_wsp[i])
        return roznica

    def __isub__(self, other):
        roznica = []
        for i in range(self.wymiar):
            roznica.append(self.lista_wsp[i] - other.lista_wsp[i])
        return roznica

    def __mul__(self, other):
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wsp[i] * other.lista_wsp[i])
        return iloczyn

    def __imul__(self, other):
        iloczyn = []
        for i in range(self.wymiar):
            iloczyn.append(self.lista_wsp[i] * other.lista_wsp[i])
        return iloczyn

    def __div__(self, other):
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wsp[i] / other.lista_wsp[i])
        return iloraz

    def __idiv__(self, other):
        iloraz = []
        for i in range(self.wymiar):
            iloraz.append(self.lista_wsp[i] / other.lista_wsp[i])
        return iloraz

    def norma(self):
        suma = 0
        for wsp in self.lista_wsp:
            suma += wsp**2
        return math.sqrt(suma)

    def metryka(self, other):
        return self.norma(self - other)

class graf:
    def ustaw_liste_punkt(self):
        lista_punkt = []
        for i in range(self.liczba_punkt):
            nazwa_punkt = input('Podaj nazwę punktu: ')
            punkt(nazwa_punkt, self.wymiar)
            lista_punkt.append(nazwa_punkt)
        self.lista_punkt = lista_punkt

    def __init__(self, liczba_punkt, wymiar):
        self.liczba_punkt = liczba_punkt
        self.wymiar = wymiar
        self.ustaw_liste_punkt()
