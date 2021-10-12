# Autorami programu jest Alex Gibała 
# Jesteśmy studentami matematyki stosowanej na Politechnice Krakowskiej

# Program służy do szukania sympleksów w kompleksie Vietorigo-Ripsa
# Program zostanie w przyszłości rozbudowany o kolejne funkcje

# Biblioteka z kombinatoryki została wykorzystana za pomocą funkcji combinations()
from itertools import combinations

# Biblioteka umożliwia dodawanie w miejscach wcześniech niemożliwych
from operator import add

# Biblioteka networkx jest wykorzystana w celu stworzenia grafu oraz rozwiązania problemu znalezienia
# kliki, czyli takiego podzbioru wierzchołków, że dwa dowolne i różne od siebie wierzchołki są sąsiednie
import networkx

# Z bliblioteki scipy.spatial wykorzystujemy metrykę euklidesową distance.euclidean()
from scipy.spatial import distance

# Funkcja product() jest wykorzystana w celu zastąpienia zagnieżdżonych pętel
from itertools import product

# Klasa punktów leżących na przestrzeni euklidesowej R^n
# Klasa najprawdopodobniej niepotrzebna


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
    def __init__(self, punkty, liczba_punktow, epsilon, oznaczenia=None, metryka=distance.euclidean):
        self.punkty = punkty
        self.liczba_punktow = liczba_punktow
        self.epsilon = epsilon

        # Jeśli nie podano oznaczeń funkcja sama ponumeruje (zaczynając od 1 z powodu przyjętego standardu)
        self.oznaczenia = range(1, len(self.punkty)+1) if oznaczenia == None or len(
            oznaczenia) != len(self.punkty) else oznaczenia
        self.metryka = metryka

        # Utworzenie grafu
        self.utworz_graf()

        # Obliczenie liczb Betti'ego
        self.oblicz_liczby_Bettiego_grafu()

        # Szukanie sympleksów
        self.lista_sympleksow = self.znajdz_sympleksy()



        # # Szukanie sympleksów (bez zewnętrznej metody)
        # lista_sympleksow = map(tuple, list(networkx.find_cliques(self.graf)))
        # self.lista_sympleksow = map(lambda sympleks: tuple(sorted(sympleks)), lista_sympleksow)

    # Metoda tworzy graf nieskierowany
    def utworz_graf(self):

        # Utworzenie obiektu grafu nieskierowanego
        self.graf = networkx.Graph()

        # Utworzenie wierzchołków z oznaczeń,
        # każdej nazwie przyporządkowany jest wierzchołek
        self.graf.add_nodes_from(self.oznaczenia)

        # Utworzenie krawędzi w grafie
        self.utworz_krawedzie()

        # # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        # lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        # #   jeśli oznaczenia wierzchołków są różne
        # #       oblicz odległość pomiędzy punktami,
        # #       jeśli odległość jest mniejsza niż przyjęte epsilon
        # #           utwórz bok prowadzący z jednego wierzchołka do drugiego
        # for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
        #     if para[0][1] != para[1][1]:
        #         odleglosc = self.metryka(para[0][0], para[1][0])
        #         if odleglosc < self.epsilon:
        #             graf.add_edge(para[0][1], para[1][1])

        return self.graf

    # Metoda tworzy nowe krawędzie w grafie
    def utworz_krawedzie(self):
        self.liczba_krawedzi = 0

        # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        #   jeśli oznaczenia wierzchołków są różne
        #       oblicz odległość pomiędzy punktami,
        #       jeśli odległość jest mniejsza niż przyjęte epsilon
        #           utwórz bok prowadzący z jednego wierzchołka do drugiego
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1] != para[1][1]:
                odleglosc = self.metryka(para[0][0], para[1][0])
                if odleglosc < self.epsilon:
                    self.graf.add_edge(para[0][1], para[1][1])
                    self.liczba_krawedzi += 1

    # Metoda podobna do powyższej, tylko usuwa wszystkie pozostałe krawędzie zamiast dodawać nowych
    def usun_krawedzie(self):
        # Przyporządkowanie wierzchołkom właściwe punkty (a dokładniej ich współrzędne)
        lista_punktów_z_oznaczeniami = tuple(zip(self.punkty, self.oznaczenia))

        # Za każdą parę dwóch wierzchołków (product() można zastąpić zagnieżdżoną pętlą)
        #   jeśli oznaczenia wierzchołków są różne
        #       spróbuj usunąć krawędź
        #       jeśli krawędź nie istnieje zignoruj błąd (wymagane by ta metoda działała)
        for para in product(lista_punktów_z_oznaczeniami, lista_punktów_z_oznaczeniami):
            if para[0][1] != para[1][1]:
                try:
                    self.graf.remove_edge(para[0][1], para[1][1])
                # Funkcja remove_edge() zwróci ten błąd jak nie istnieje krawędź łącząca daną parę wierzchołków
                except networkx.exception.NetworkXError:
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
        lista_sympleksow = map(lambda sympleks: tuple(
            sorted(sympleks)), lista_sympleksow)

        # Zwracamy zbiór sympleksów
        return tuple(lista_sympleksow)

    # Metoda wykorzystuje powyższą metodę w celu zwrócenia wszystkich ścian (krawędzi) dowolnego wymiaru
    def wypisz_sciany(self):
        zbior_scian = set()

        # Za każdy sympleks ze zbioru sympleksów (bez powtórek)
        #   sprawdźmy ile wierzchołków zawiera sympleks
        #   za każdy możliwy wymiar ściany (liczony od największego do 0 wymiaru)
        #       liczymy możliwe kombinacje n-elementowe ścian, gdzie n to wymiar ściany
        #           dodajemy każdą ścianę do zbioru
        for sympleks in self.lista_sympleksow:
            liczba_wierzcholkow = len(sympleks)
            for wymiar_sciany in range(liczba_wierzcholkow, 0, -1):
                for sciana in combinations(sympleks, wymiar_sciany):
                    zbior_scian.add(sciana)

        # Zwracamy zbiór wszystkich możliwych ścian
        return tuple(zbior_scian)

    # Metoda wykorzystuje powyższą metodę w celu zwrócenia ścian o danym wymiarze
    def wypisz_sciany_danego_wymiaru(self, szukany_wymiar):
        zbior_scian = self.wypisz_sciany()

        # Tutaj filtrujemy zbiór ścian z poprzedniej funkcji szukając ścian o porządanym wymiarze
        return tuple(filter(lambda sciana: len(sciana) == szukany_wymiar + 1, zbior_scian))

    # Metoda zwraca wymiar kompleksu (czyli wymiar maksymalnego sympleksu)
    def podaj_wymiar_kompleksu(self):
        maksymalny_wymiar = 0
        for sympleks in self.lista_sympleksow:
            maksymalny_wymiar = max(maksymalny_wymiar, len(sympleks)-1)
        return maksymalny_wymiar

    # Metoda zmienia wartość epsilona i jednocześnie aktualizuje krawędzie w grafie
    def zmien_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.usun_krawedzie()
        self.utworz_krawedzie()
        self.lista_sympleksow = self.znajdz_sympleksy()

    # Metoda oblicza liczby Betti'ego grafu
    def oblicz_liczby_Bettiego_grafu(self):
        # Nieformalnie, k-ta liczba Betti'ego odpowiada za liczbę 
        # k-wymiarowych dziur na topologicznej przestrzeni

        # Zerowa liczba Betti'ego grafu nieskierowanego to liczba spójnych składowych
        # Spójna składowa to maksymalny spójny podgraf grafu nieskierowanego
        self.zerowa_liczba_Bettiego_grafu = networkx.number_connected_componets(self.graf)

        # Pierwsza liczba Betti'ego grafu nieskierowanego równa się liczbie cyklomatrycznej
        # Liczba cyklomatryczna = liczba spójnych składowych + liczba krawędzi - liczba wierzchołków
        self.pierwsza_liczba_Bettiego_grafu = self.zerowa_liczba_Bettiego_grafu + self.liczba_krawedzi - self.liczba_punktow

        # Pozostałe liczby Betti'ego grafu są równe 0
        self.pozostała_liczba_Bettiego_grafu = 0

    # Metoda oblicza liczby Betti'ego sympleksu
    # Funkcja oczywiście niedokończona
    def oblicz_liczby_Bettiego_sympleksu(self, sympleks):
        return None

    # # Metoda najprawdopodobniej niepotrzebna
    # def oblicz_liczbe_cyklomatryczna(self):
    #     liczba_spojnych_skladowych = networkx.number_connected_componets(self.graf)
    #     return self.liczba_krawedzi - self.liczba_punktow + liczba_spojnych_skladowych

# Funkcja wypisuje komendy przydatne po utworzeniu obiektu kompleksu


def wypisz_komendy():
    print('W celu:')
    print('-otrzymania instrukcji odczytania wyników, napisz "instrukcja",')
    print('-wypisania wszystkich sympleksów, napisz "wszystko",')
    print('-wypisania sympleksów danego wymiaru, napisz "tylko",')
    print('-wypisania sympleksów z wyjątkiem tych, które nie będą się zawierać w innych, napisz "maksymalne",')
    print('-wypisania wymiaru kompleksu, napisz "kompleks",')
    print('-zmiany epsilona, napisz "epsilon",')
    print('-wyłączenia programu, napisz "koniec",')
    print('-ponownego wypisania komend, napisz "komendy".')


# Tutaj zaczyna się właściwy program
if __name__ == "__main__":

    # Krótka informacja o programie
    print('Program służy do obliczania kompleksu Vietorigo-Ripsa w przestrzeni euklidesowej R^n.')
    print('Autorami projektu jest Alex Gibała')
    print('Postępuj zgodnie ze wskazówkami!')
    print('Zacznijmy od utworzenia grafu.')

    # Tutaj użytkownik oznajmia czy zamierza stosować własne oznaczenia punktów
    # Pętla została umieszczona w celu upewnienia się, że podano poprawną odpowiedź
    # W przypadku braku chęci progra samemu będzie numerować punkty
    while True:
        print('Czy zamierzasz stosować własne oznaczenia punktów?')
        wlasne_oznaczenia = input('Wpisz tutaj [tak/NIE]: ')
        if wlasne_oznaczenia.lower() in ['tak', 't']:
            wlasne_oznaczenia = True
            lista_oznaczen = []
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
        except Exception:
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
        except Exception:
            print('Niepoprawna odpowiedź!')
            print('Podaj niezerową liczbę naturalną!')

    # Tutaj użytkownik wypisuje wszystkie punkty
    # W przypadku, gdy użytkownik pomyli się, to program poprosi o ponownie wpisanie
    # danych, bez potrzeby restartowania aplikacji
    if wlasne_oznaczenia == True:
        print('Teraz wypisz nazwy punktów wraz z współrzędnymi.')
    else:
        print('Teraz wypisz współrzędne wszystkich punktów.')

    lista_punktow = []

    # Zaczynamy odliczanie punktów od 1 z przyjętego standardu
    for indeks_punktu in range(1, liczba_punktow+1):
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
        lista_wspolrzednych = []
        for indeks_wspolrzednej in range(1, wymiar+1):
            while True:
                try:
                    lista_wspolrzednych.append(
                        float(input('Wpisz współrzędną x{}: '.format(indeks_wspolrzednej))))
                    break
                except Exception:
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
            print(
                'Epsilon to maksymalna możliwa odległość pozwalająca na połączenie punktów krawędzią.')
            print('Ile wynosi epsilon?')
            epsilon = float(input('Wpisz tutaj: '))
            if epsilon <= 0:
                print('Epsilon musi być dodatnie!')
            else:
                break
        except Exception:
            print('Niepoprawna odpowiedź!')
            print('Podaj dodatnią liczbę rzeczywistą!')

    # Utworzenie obiektu kompleksu
    print('Kompleks się tworzy...')
    if wlasne_oznaczenia == True:
        kompleks = Kompleks_Vietorigo_Ripsa(
            lista_punktow, liczba_punktow, epsilon, lista_oznaczen)
    else:
        kompleks = Kompleks_Vietorigo_Ripsa(lista_punktow, liczba_punktow, epsilon)
    print('Kompleks utworzony!')

    # Pętla w celu zapobiegnięcia potrzeby uruchamiania programu parę razy
    wypisz_komendy()
    while True:
        odpowiedz = input('Wpisz komendę tutaj: ')

        if odpowiedz.lower() == 'instrukcja':
            print(
                'Niech 1, 2 oraz 3 będą kolejnymi wierzchołkami w grafie połączonymi krawędziami.')
            print(
                'Poprzez (1,) rozumiemy sympleks zerowego wymiaru składający się z pierwszego wierzchołka.')
            print(
                'Poprzez (1,2) rozumiemy sympleks drugiego wymiaru łączący pierwsze dwa wierzchołki.')
            print(
                'Poprzez (1,2,3) rozumiemy sympleks trzeciego wymiaru, który zawiera wszystkie wierzchołki.')
            print(
                'Reguła odczytywania także zachodzi odpowiednio dla większych wymiarów.')

        elif odpowiedz.lower() == 'wszystko':
            print('Sympleksy: {}'.format(kompleks.wypisz_sciany()))

        elif odpowiedz.lower() == 'tylko':
            while True:
                try:
                    print('Jaki jest wymiar szukanych sympleksów?')
                    szukany_wymiar = int(input('Wpisz tutaj: '))
                    if szukany_wymiar < 0:
                        print('Wymiar musi być nieujemny!')
                    else:
                        print('Sympleksy: {}'.format(
                            kompleks.wypisz_sciany_danego_wymiaru(szukany_wymiar)))
                        break
                except Exception:
                    print('Niepoprawna odpowiedź!')
                    print('Podaj liczbę naturalną!')

        elif odpowiedz.lower() == 'maksymalne':
            print('Sympleksy: {}'.format(kompleks.lista_sympleksow))

        elif odpowiedz.lower() == 'kompleks':
            print('Wymiar kompleksu wynosi {}.'.format(
                kompleks.podaj_wymiar_kompleksu()))

        elif odpowiedz.lower() == 'epsilon':
            while True:
                try:
                    print('Podaj nową wartość epsilon.')
                    epsilon = float(input('Wpisz tutaj: '))
                    if epsilon <= 0:
                        print('Epsilon musi być dodatnie!')
                    else:
                        break
                except Exception:
                    print('Niepoprawna odpowiedź!')
                    print('Podaj niezerową liczbę rzeczywistą!')
            kompleks.zmien_epsilon(epsilon)
            print('Zmieniono wartość epsilon!')

        elif odpowiedz.lower() == 'koniec':
            break

        elif odpowiedz.lower() == 'komendy':
            wypisz_komendy()

        else:
            print('Niepoprawna komenda!')
            print('Napisz jeszcze raz!')
            print(
                'W razie potrzeby, napisz "komendy" w celu ponownego wyświetlenia dostępnych komend.')
