    # grupy homologii
    # operator brzegów w kompleksie
    # założenie, że pracujemy w ciele Z2
    # liczby Bettiego

    # Topologia stosowana i topologia algebraiczna
    # Topologiczna analiza danych

# Biblioteka z kombinatoryki została wykorzystana za pomocą funkcji combinations()
from itertools import combinations

# Biblioteka umożliwia dodawanie w miejscach wcześniech niemożliwych
from operator import add

# Biblioteka najprawdopodobniej niepotrzebna
#from scipy.sparse import dok_matrix

# Biblioteka networkx jest wykorzystana w celu stworzenia grafu oraz rozwiązania problemu znalezienia 
# kliki, czyli takiego podzbioru wierzchołków, że dwa dowolne i różne od siebie wierzchołki są sąsiednie
import networkx

# Z bliblioteki scipy.spatial wykorzystujemy metrykę euklidesową distance.euclidean()
from scipy.spatial import distance

# Funkcja product() jest wykorzystana w celu zastąpienia zagnieżdżonych pętel
from itertools import product

# Klasa punktów leżących na przestrzeni euklidesowej R^n
class Punkt:

    # Obiekt punktu przyjmuje:
    # - oznaczenie punktu,
    # - zbiór współrzędnych punktu
    def __init__(self, nazwa, lista_wspolrzednych):
        self.nazwa = nazwa
        self.lista_wspolrzednych = lista_wspolrzednych

# Klasa kompleksu Vietorigo-Ripsa
class Kompleks_Vietorigo_Ripsa:

    # Obiekt kompleksu przyjmuje:
    # - listę punktów (zbiór zbiorów współrzędnych, nie oznaczeń), 
    # - epsilon będący maksymalną możliwą odległością do zarejestrowania krawędzi,
    # - (opcjonalnie) zbiór własnych oznaczeń wierzchołków,
    # - (opcjonalnie, nie zaimplementowane w praktyce) własną metrykę - standardowo metryka euklidesowa
    def __init__(self, punkty, epsilon, oznaczenia=None, metryka=distance.euclidean):
        self.punkty = punkty
        self.epsilon = epsilon

        # Jeśli nie podano oznaczeń funkcja sama ponumeruje (zaczynając od 1 z powodu przyjętego standardu)
        self.oznaczenia = range(1, len(self.punkty)+1) if oznaczenia==None or len(oznaczenia)!=len(self.punkty) else oznaczenia
        self.metryka = metryka

        # Utworzenie grafu
        self.graf = self.utworz_graf()

        # Szukanie sympleksów
        self.lista_sympleksow = self.znajdz_sympleksy()

        # # Szukanie sympleksów (bez zewnętrznej metody)
        # lista_sympleksow = map(tuple, list(networkx.find_cliques(self.graf)))
        # self.lista_sympleksow = map(lambda sympleks: tuple(sorted(sympleks)), lista_sympleksow)

    # Metoda tworzy graf nieskierowany
    def utworz_graf(self):

        # Utworzenie obiektu grafu nieskierowanego
        graf = networkx.Graph()

        # Utworzenie wierzchołków z oznaczeń,
        # każdej nazwie przyporządkowany jest wierzchołek
        graf.add_nodes_from(self.oznaczenia)

        # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        #   jeśli oznaczenia wierzchołków są różne
        #       oblicz odległość pomiędzy punktami,
        #       jeśli odległość jest mniejsza niż przyjęte epsilon
        #           utwórz bok prowadzący z jednego wierzchołka do drugiego
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1]!=para[1][1]:
                odleglosc = self.metryka(para[0][0], para[1][0])
                if odleglosc < self.epsilon:
                    graf.add_edge(para[0][1], para[1][1])
        
        # Utworzony graf zostaje zwrócony
        return graf

    # Metoda podobna do powyższej, tylko nie tworzy nowego grafu i nie tworzy nowych wierzchołków, tylko dodaje nowe krawędzie
    def utworz_krawedzie(self):
        # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        #   jeśli oznaczenia wierzchołków są różne
        #       oblicz odległość pomiędzy punktami,
        #       jeśli odległość jest mniejsza niż przyjęte epsilon
        #           utwórz bok prowadzący z jednego wierzchołka do drugiego
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1]!=para[1][1]:
                odleglosc = self.metryka(para[0][0], para[1][0])
                if odleglosc < self.epsilon:
                    self.graf.add_edge(para[0][1], para[1][1])

    # Metoda podobna do powyższej, tylko usuwa wszystkie pozostałe krawędzie zamiast dodawać nowych
    def usun_krawedzie(self):
        # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        #   jeśli oznaczenia wierzchołków są różne
        #       spróbuj usunąć krawędź
        #       jeśli krawędź nie istnieje zignoruj błąd (wymagane by ta metoda działała)
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1]!=para[1][1]:
                try:
                    self.graf.remove_edge(para[0][1],para[1][1]) 
                except networkx.exception.NetworkXError: # Funkcja remove_edge() zwróci ten błąd jak nie istnieje krawędź łącząca daną parę wierzchołków
                    pass    

    # Metoda do szukania sympleksów
    # Funkcja map() wykonuje funkcję na każdym elemencie listy
    # Funkcja find_cliques szuka kliki, czyli takie podzbiory wierzchołków, że dwa dowolne wierzchołki
    # różne od siebie są sąsiednie
    # WAŻNE! Ta funkcja nie będzie zwracać takich sympleksów, które będą zawierać się w innych sympleksach
    def znajdz_sympleksy(self):
        # lista_sympleksow = map(tuple, list(networkx.find_cliques(self.graf)))

        # Tutaj szukamy sympleksów (kliki)
        lista_sympleksow = tuple(networkx.find_cliques(self.graf))

        # Tutaj zamieniamy każdy sympleks ze zbioru na krotkę
        lista_sympleksow = map(lambda sympleks: tuple(sorted(sympleks)), lista_sympleksow)

        # Zwracamy zbiór sympleksów
        return tuple(lista_sympleksow)

    # Metoda wykorzystuje powyższą metodę w celu zwrócenia wszystkich ścian (krawędzi) dowolnego wymiaru
    def wypisz_sciany(self):
        self.lista_sympleksow = self.znajdz_sympleksy()
        zbior_scian = set()
        for sympleks in self.lista_sympleksow:
            liczba_wierzcholkow = len(sympleks)
            for wymiar_sciany in range(liczba_wierzcholkow, 0, -1):
                for sciana in combinations(sympleks, wymiar_sciany):
                    zbior_scian.add(sciana)
        return tuple(zbior_scian)

    # Metoda wykorzystuje powyższą metodę w celu zwrócenia ścian o danym wymiarze
    def wypisz_sciany_danego_wymiaru(self, szukany_wymiar):
        zbior_scian = self.wypisz_sciany()
        print(tuple(filter(lambda sciana: len(sciana)==szukany_wymiar + 1, zbior_scian)))
        return tuple(filter(lambda sciana: len(sciana)==szukany_wymiar + 1, zbior_scian))
        # return tuple(filter(filtr_scian, zbior_scian))

    # Metoda zmienia wartość epsilona i jednocześnie aktualizuje krawędzie w grafie
    def zmien_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.usun_krawedzie()
        self.utworz_krawedzie()

# def filtr_scian(sciana, szukany_wymiar):
#     if len(sciana) == szukany_wymiar + 1:
#         return True
#     else:
#         return False

# Funkcja wypisuje komendy przydatne po utworzeniu obiektu kompleksu
def wypisz_komendy():
    print('W celu wypisania sympleksów, napisz "wypisz".')
    print('W celu wypisania sympleksów danego stopnia, napisz "wypisz danego wymiaru".')
    print('W celu wypisania sympleksów z wyjątkiem tych, które nie będą się zawierać w innych, napisz "wypisz bez powtórek"')
    print('W celu zmiany epsilona, napisz "epsilon".')
    print('W celu wyłączenia programu, napisz "koniec".')

# Tutaj zaczyna się właściwy program
if __name__ == "__main__":

    # Krótka informacja o programie
    print('Program służy do obliczania kompleksu Vietorigo-Ripsa w przestrzeni euklidesowej R^n.')
    print('Autorami projektu są Alex Gibała oraz Piotr Musielak.')
    print('Postępuj zgodnie ze wskazówkami!')
    print('Zacznijmy od utworzenia grafu.')
    
    # Tutaj użytkownik oznajmia czy zamierza stosować własne oznaczenia punktów
    # Pętla została umieszczona w celu upewnienia się, że podano poprawną odpowiedź
    # W przypadku braku chęci progra samemu będzie numerować punkty
    while True:
        print('Czy zamierzasz stosować własne oznaczenia punktów?')
        wlasne_oznaczenia = input('Wpisz tutaj [tak/NIE]: ')
        if wlasne_oznaczenia.lower() == 'tak' or wlasne_oznaczenia.lower() == 't':
            wlasne_oznaczenia = True
            lista_oznaczen = list()
            break
        elif wlasne_oznaczenia.lower() == 'nie' or wlasne_oznaczenia.lower() == 'n' or wlasne_oznaczenia == '':
            wlasne_oznaczenia = False
            break
        else:
            print('Niepoprawna odpowiedź!')
            print('Napisz "Tak" lub "Nie".')
        
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

    # Tutaj użytkownik oznajmia wymiar przestrzeni euklidesowej R^n, do której należą punkty
    # Pętla została umieszczona w celu upewnienia się, że podano liczbę oraz czy jest ona poprawna
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
    # danych, bez potrzeby restartowania aplikacji
    if wlasne_oznaczenia == True:
        print('Teraz wypisz nazwy punktów wraz z współrzędnymi.')
    else:
        print('Teraz wypisz współrzędne wszystkich punktów.')

    lista_punktow = list()

    # Zaczynamy odliczanie punktów od 1 z przyjętego standardu
    for indeks_punktu in range(1,liczba_punktow+1):
        print('Wypisz dane o punkcie numer {}.'.format(indeks_punktu))

        # Tutaj użytkownik wpisuje własne oznaczenie punktu
        if wlasne_oznaczenia == True:
            while True:
                nazwa_punktu = str(input('Wpisz nazwę punktu: '))
                if isinstance(nazwa_punktu, Punkt) or nazwa_punktu in lista_oznaczen:
                    print('Niepoprawna odpowiedź!')
                    print('Oznaczenia nie mogą się powtarzać!')
                else:
                    lista_oznaczen.append(nazwa_punktu)
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
        lista_punktow.append(lista_wspolrzednych)
        if wlasne_oznaczenia == True:
            Punkt(nazwa_punktu, lista_wspolrzednych)
            print('Utworzono punkt {}.'.format(nazwa_punktu))
        else:
            Punkt(indeks_punktu, lista_wspolrzednych)
            print('Utworzono punkt numer {}.'.format(indeks_punktu))
    

    # Tutaj użytkownik podaje maksymalną długość pozwalającą
    # na powstanie krawędzi pomiędzy dwoma wierzchołkami
    while True:
        try:
            print('Epsilon to maksymalna możliwa odległość pozwalająca na połączenie punktów krawędzią.')
            print('Ile wynosi epsilon?')
            epsilon = float(input('Wpisz tutaj: '))
            if epsilon <= 0:
                print('Epsilon musi być dodatnie!')
            else:
                break
        except:
            print('Niepoprawna odpowiedź!')
            print('Podaj dodatnią liczbę rzeczywistą!')

    # Utworzenie obiektu kompleksu
    print('Kompleks się tworzy...')
    if wlasne_oznaczenia == True:
        kompleks = Kompleks_Vietorigo_Ripsa(lista_punktow, epsilon, lista_oznaczen)
    else:
        kompleks = Kompleks_Vietorigo_Ripsa(lista_punktow, epsilon)
    print('Kompleks utworzony!')

    # Pętla w celu zapobiegnięcia potrzeby uruchamiania programu parę razy
    while True:
        wypisz_komendy()
        odpowiedz = input('Wpisz tutaj: ')

        if odpowiedz.lower() == 'wypisz':
            print('Sympleksy:')
            print(kompleks.wypisz_sciany())

        elif odpowiedz.lower() == 'wypisz danego wymiaru':
            print('Podaj wymiar szukanych sympleksów.')
            while True:
                try:
                    print('Jaki jest wymiar szukanych sympleksów?')
                    szukany_wymiar = int(input('Wpisz tutaj: '))
                    if szukany_wymiar < 0:
                        print('Wymiar musi być nieujemny!')
                    else:
                        break
                except:
                    print('Niepoprawna odpowiedź!')
                    print('Podaj liczbę naturalną!')
                
                print('Sympleksy:')
                print(kompleks.wypisz_sciany_danego_wymiaru(szukany_wymiar))

        elif odpowiedz.lower() == 'wypisz bez powtórek':
            print('Sympleksy:')
            print(kompleks.lista_sympleksow)

        elif odpowiedz.lower() == 'epsilon':
            while True:
                try:
                    print('Podaj nową wartość epsilon.')
                    epsilon = float(input('Wpisz tutaj: '))
                    if epsilon <= 0:
                       print('Epsilon musi być dodatnie!')
                    else:
                        break
                except:
                    print('Niepoprawna odpowiedź!')
                    print('Podaj niezerową liczbę rzeczywistą!')
            kompleks.zmien_epsilon(epsilon)

        elif odpowiedz.lower() == 'koniec':
            break

        else:
            print('Niepoprawna komenda!')
            print('Napisz jeszcze raz!')