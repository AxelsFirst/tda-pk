import math
import numpy as np

wymiar = 2

class punkt:
    def ustaw_wsp(self, wymiar):
        self.lista_wsp = []
        for i in range(wymiar):
            self.wsp.append(input('Wypisz {}-tą współrzędną: '.format(i)))

    def __init__(self, nazwa, wymiar):
        self.nazwa = nazwa
        self.ustaw_wsp(wymiar)
    
    def wypisz_wsp(self, wydrukuj = False):
        if wydrukuj == True:
            print(self.lista_wsp)
        else:
            return self.lista_wsp

    def zmien_wsp(self, indeks, wartosc):
        self.lista_wsp[indeks] = wartosc

    def __add__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] + other.lista_wsp[i])
        return wynik

    def __iadd__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] + other.lista_wsp[i])
        return wynik

    def __sub__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] - other.lista_wsp[i])
        return wynik

    def __isub__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] - other.lista_wsp[i])
        return wynik

    def __mul__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] * other.lista_wsp[i])
        return wynik

    def __imul__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] * other.lista_wsp[i])
        return wynik

    def __div__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] / other.lista_wsp[i])
        return wynik

    def __idiv__(self, other):
        wynik = []
        for i in range(wymiar):
            wynik.append(self.lista_wsp[i] / other.lista_wsp[i])
        return wynik

    def norma(self):
        suma = 0
        for i in wymiar:
            suma += self.lista_wsp[i]**2
        return math.sqrt(suma)

    def metryka(self, other):
        return norma(self - other)

class graf:
    def __init__(self, lista_punkt):
        self.lista_punkt = lista_punkt