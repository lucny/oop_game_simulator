# Simulace hry s využitím OOP v Pythonu

Tento projekt demonstruje použití objektově orientovaného programování (OOP) v Pythonu na příkladu jednoduché simulace hry, kde se dva hráči utkají v hodu kostkou.

## Struktura projektu

- **`optimized_game.py`** – obsahuje definice tříd pro hráče (`Player`), zápas (`Match`), osobu (`Person`), výčtový typ pro pohlaví (`Gender`) a třídu kostky (`Dice`).
- **`main.py`** – hlavní soubor pro spuštění simulace zápasu mezi dvěma hráči.
- **`players.json`** – soubor s daty hráčů, kteří se mohou účastnit zápasu.
- **`results.json`** – soubor, do kterého se ukládají výsledky zápasů.
- **`files.py`** – pomocné funkce pro práci se soubory (`json` a `csv`).

## Požadavky

- Python 3.8+

## Instalace

1. Naklonujte tento repozitář nebo stáhněte soubory.
2. Ujistěte se, že máte nainstalovaný Python 3.8 nebo novější.
3. V prostředí terminálu/spuštěcího okna přejděte do složky s projektem.

## Spuštění hry

Spusťte simulaci zápasu pomocí příkazu:

```sh
python main.py
```

## Pravidla hry

1. Každý zápas se hraje do **10 bodů**.
2. Hráči se střídají v hodu kostkou.
3. Vyhrává ten hráč, který jako první dosáhne 10 bodů.
4. Výsledky zápasu se ukládají do `results.json`.

## Možné úpravy

- **Nastavení délky zápasu** – lze změnit parametr `winning_score` v třídě `Match`.
- **Změna rozsahu kostky** – výchozí je hod **od 1 do 6**, ale lze nastavit hodnoty mezi **4 až 9**.
- **Přidání dalších hráčů** – lze rozšířit `players.json` o nové hráče.

## Autor
Projekt vytvořen jako výukový materiál pro demonstraci OOP v Pythonu.

