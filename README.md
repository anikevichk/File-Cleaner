# File Cleaner

Projekt zawiera skrypt w Pythonie służący do porządkowania plików w katalogach.

Skrypt sprawdza katalog główny `X` oraz dodatkowe katalogi `Y1`, `Y2` itd.  
Wyszukuje puste pliki, pliki tymczasowe, duplikaty, pliki o tej samej nazwie, niepoprawne uprawnienia, problematyczne nazwy plików oraz pliki brakujące w katalogu głównym `X`.

## Pliki projektu

```text
File-Cleaner/
├── clean_files.py
├── create_test_data.sh
├── create_expected_final_data.sh
├── README.md
└── cleaner/
    ├── actions.py
    ├── config.py
    ├── file_utils.py
    ├── output.py
    └── checks.py
```

### Opis plików

| Plik | Opis |
|---|---|
| `clean_files.py` | Główny plik programu. Odczytuje argumenty z linii komend, wybiera tryb działania i uruchamia odpowiednie sprawdzenia. |
| `create_test_data.sh` | Skrypt Bash tworzący przykładowe katalogi `X`, `Y1`, `Y2` oraz pliki testowe. |
| `create_expected_final_data.sh` | Skrypt Bash tworzący oczekiwany wynik końcowy po uruchomieniu programu z opcją `--apply`. |
| `README.md` | Dokumentacja projektu: opis, sposób uruchomienia, tryby działania i konfiguracja. |
| `cleaner/actions.py` | Obsługuje wybór akcji w trybie interaktywnym, np. wykonanie jednej akcji, pominięcie jej albo zastosowanie tej samej decyzji dla kolejnych plików. |
| `cleaner/config.py` | Odczytuje ustawienia z pliku konfiguracyjnego `.clean_files`. |
| `cleaner/file_utils.py` | Zawiera funkcje pomocnicze, np. obliczanie hashy, sprawdzanie uprawnień, nazw plików i zbieranie listy plików. |
| `cleaner/output.py` | Odpowiada za formatowanie i wypisywanie wyników działania programu. |
| `cleaner/checks.py` | Zawiera główne sprawdzenia: puste pliki, pliki tymczasowe, duplikaty, wersje plików, uprawnienia, nazwy i brakujące pliki w katalogu `X`. |

## Uruchomienie

### 1. Utworzenie danych testowych

```bash
chmod +x create_test_data.sh
./create_test_data.sh
```

Skrypt utworzy:

```text
test_data/
├── X
├── Y1
├── Y2
└── .clean_files
```

### 2. Uruchomienie bez wprowadzania zmian

```bash
python3 clean_files.py --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2
```

Domyślnie skrypt tylko wypisuje sugerowane akcje i nie zmienia plików.

### 3. Uruchomienie z zastosowaniem zmian

```bash
python3 clean_files.py --apply --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2
```

Opcja `--apply` automatycznie wykonuje wszystkie sugerowane akcje.

### 4. Uruchomienie w trybie interaktywnym

```bash
python3 clean_files.py --interactive --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2
```

W trybie interaktywnym program pyta przed wykonaniem każdej znalezionej akcji. Dostępne odpowiedzi:

| Odpowiedź | Znaczenie |
|---|---|
| `y` | wykonaj tę jedną akcję |
| `n` | pomiń tę jedną akcję |
| `a` | wykonuj automatycznie kolejne akcje tego samego typu |
| `s` | pomijaj kolejne akcje tego samego typu |

Dzięki temu można wybrać akcję osobno dla konkretnego pliku albo zastosować jedną decyzję dla całej grupy podobnych problemów.

### 5. Utworzenie oczekiwanego wyniku końcowego

Można również uruchomić skrypt tworzący katalog z oczekiwanym stanem plików po zastosowaniu opcji `--apply`.

```bash
chmod +x create_expected_final_data.sh
./create_expected_final_data.sh
```
Katalog ten reprezentuje poprawny wynik końcowy: wszystkie potrzebne pliki znajdują się w katalogu X, duplikaty, pliki puste i tymczasowe są usunięte, nazwy oraz uprawnienia są poprawione.

### 6. Porównanie wyniku

Po uruchomieniu programu z opcją --apply można porównać otrzymany wynik z oczekiwanym wynikiem końcowym:
```bash
diff -r test_data expected_final_data
```
Jeżeli polecenie diff nic nie wypisze, oznacza to, że wynik działania programu jest zgodny z oczekiwanym wynikiem.

## Dostępne tryby

| Tryb | Opis |
|---|---|
| `all` | Uruchamia wszystkie sprawdzenia |
| `empty` | Wyszukuje puste pliki |
| `temp` | Wyszukuje pliki tymczasowe |
| `duplicates` | Wyszukuje pliki o identycznej zawartości |
| `versions` | Wyszukuje pliki o tej samej nazwie, ale różnej zawartości |
| `names` | Wyszukuje pliki z problematycznymi znakami w nazwie |
| `permissions` | Wyszukuje pliki z niepoprawnymi uprawnieniami |
| `missing` | Wyszukuje pliki, których brakuje w katalogu głównym `X`, i przenosi je do odpowiedniego miejsca w `X` |

### Zastosowanie wybranego trybu

Przykład zastosowania usuwania duplikatów:

```bash
python3 clean_files.py --apply --mode duplicates --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2
```

Przykład zastosowania usuwania pustych plików:

```bash
python3 clean_files.py --apply --mode empty --config test_data/.clean_files test_data/X test_data/Y1 test_data/Y2
```

## Plik konfiguracyjny

Skrypt odczytuje ustawienia z pliku `.clean_files`.

Przykład:

```text
permissions=rw-r--r--
bad_chars=:";*?$#`|\
replacement=_
temp_extensions=.tmp,~
```

Znaczenie opcji:

| Opcja | Opis |
|---|---|
| `permissions` | Oczekiwane uprawnienia plików |
| `bad_chars` | Znaki, które nie powinny występować w nazwach plików |
| `replacement` | Znak używany do zastępowania problematycznych znaków |
| `temp_extensions` | Rozszerzenia traktowane jako pliki tymczasowe |

## Tryby wykonywania akcji

Bez opcji `--apply` i `--interactive` skrypt działa w trybie bezpiecznym: tylko wypisuje sugerowane akcje i nie zmienia plików.

Z opcją `--apply` skrypt wykonuje wszystkie sugerowane akcje automatycznie, np. usuwanie, przenoszenie, kopiowanie, zmianę nazwy oraz zmianę uprawnień.

Z opcją `--interactive` skrypt pyta użytkownika, czy wykonać daną akcję. Użytkownik może podjąć decyzję dla pojedynczego pliku albo wybrać wspólną decyzję dla kolejnych akcji tego samego typu.
