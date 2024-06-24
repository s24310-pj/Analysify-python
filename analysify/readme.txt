Rozwiązania programistyczne:
    aplikacja oparta jest mniej więcej na modelu MVC,
    rolę Modelu spełnia data_analyzer.py gdzie są wykonywane operacje na danych, między innymi takie jak ładowanie, filtowanie, przekształcanie i generowanie wykresów.
    rolę Viev spełnia gui.py który wyświetla interfejs oraz dane użytkownikowi
    rolę Controllera spełnia również gui.py, który zawiera obsługę zdarzeń użytkownika - przyciski oraz funkcje zwrotne w odpowiedzi na interakcje użytkownika
    Wykorzystanie takiego wzorca pozwala na rozdzielenie operacji na danych i interfejsu użytkownika co ułatwia testowanie, oraz dalszy rozwój aplikacji i poprawia czytelność kodu
    Aplikacja w głównej mierze wykorzystuje podejście obiektowe, jedynie interakcje z interfejsem użytkownika są zaprogamowane w sposób proceduralny ze względu na wykorzystanie narzędznia Tkinter

Zastosowane metody:
    meotda do wczytywania danych - podstawowa metoda na której bazuje aplikacja - bez załadowania pliku reszta aplikacji jest nieaktywna
    metoda wyświetlająca podsumowanie danych - wyświetla średnią, minimalną oraz maksymalną wartość z każdej kolumny dla szybkiego przeglądu i statystyki
    metoda wyświetlająca dane - umożliwia eksplorację zbioru danych w formie tabeli - po kliknięciu w nazwę kolumny dane przefiltrują się rosnąco lub malejąco
    metoda filtrująca dane - wybieramy z dostępnych kolmn jedną a następnie wpisujemy wartośc po której chcemy filtrować - pozwala to na znalezienie tego co chcemy
    metoda do przekształcania danych na numeryczne - wybieramy kolumnę którą chcemy przekształcić - umożliwia to dalsze i łatwiejsze manipulacje oraz czytelniejsze wykresy
    metoda do generowania wykresów - umożliwia generowanie 4 typów wykresów: liniowy, słupkowy, punktowy oraz kołowy - użytkownik może wybrać dowlne dane dla 1 i 2 kolumny (dla kołowego tylko 1 kolumna) co nie zawsze będzie miało sens, ale wybór jest pozostawiony użytkownikowi, aby dostosować aplikację do różnych zbiorów danych
    metoda generowania predefiniowanych wykresów - pozwala na wygenerowanie wykresu jednym kliknięciem - wykresu który będzie miał sens i jego typ jest dopasowany do konretnych danych z tego zbioru danych

