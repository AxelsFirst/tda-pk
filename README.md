# Vietoris-Rips_complex
Program wypisujący sympleksy Vietorigo-Ripsa.

## O programie

### Sposób działania
Ponieważ program operuje na przestrzeniach euklidesowych R^n z metryką euklidesową, należy zacząć od podania wymiaru danych, po czym zaleca się wypisać punkty o współczynnikach będącymi liczbami rzeczywistymi. Po wypisaniu wszystkich informacji program zwróci wszystkie istniejące sympleksy złożone z punktów danych.

### Informacja o sposobie odczytywania wyniku
Jeśli {a_1, a_2, a_3, ..., a_n, a_(n+1)} będzie sympleksem n-tego stopnia, to istnieje n+1 sympleksów stopnia n-1 złożonych z punktów danych należących do {a_1, a_2, a_3, ..., a_n, a_(n+1)}.

Korzystając z powyższej zależności, to jeśli istnieje sympleks S n-tego stopnia program nie będzie zwracał sympleksów o stopniu mniejszym niż n, jeśli będą się one składać tylko i wyłącznie z wierzchołków zawierających się w S. Ten sposób wypisania wyniku obliczeń programu jest umotywowany próbą zachowania czytelności.

### Informacja o złożoności obliczeniowej
Ze względu na złożoność obliczeniową w celu testowania programu zaleca się użycia dostatecznie małej ilości punktów.