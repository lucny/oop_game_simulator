"""Modul pro práci se soubory (textové, JSON, CSV).

Obsahuje funkce pro načítání a ukládání dat do různých formátů souborů:
- textové soubory
- JSON
- CSV
"""

import json
import csv


def textfile_read(path, encoding='utf-8'):
    """Načte obsah textového souboru.

    Args:
        path (str): Cesta k textovému souboru.
        encoding (str): Kódování souboru (výchozí: utf-8).

    Returns:
        str: Obsah souboru.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
        Exception: Pokud došlo k chybě při čtení.
    """
    with open(path, encoding=encoding) as file:
        return file.read()


def textfile_write(path, data='', encoding='utf-8'):
    """Uloží text do textového souboru.

    Args:
        path (str): Cesta k textovému souboru.
        data (str): Text k uložení (výchozí: '').
        encoding (str): Kódování souboru (výchozí: utf-8).

    Raises:
        FileNotFoundError: Pokud není cesta platná.
        Exception: Pokud došlo k chybě při zápisu.
    """
    with open(path, mode='w', encoding=encoding) as file:
        file.write(data)


def jsonfile_read(path, encoding='utf-8'):
    """Načte data z JSON souboru.

    Args:
        path (str): Cesta k JSON souboru.
        encoding (str): Kódování souboru (výchozí: utf-8).

    Returns:
        dict|list: Data z JSON souboru.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
        json.JSONDecodeError: Pokud soubor není validní JSON.
        Exception: Pokud došlo k chybě při čtení.
    """
    with open(path, encoding=encoding) as json_file:
        return json.load(json_file)


def jsonfile_write(path, data=None, encoding='utf-8'):
    """Uloží data do JSON souboru.

    Args:
        path (str): Cesta k JSON souboru.
        data (dict|list): Data k uložení (výchozí: prázdný slovník).
        encoding (str): Kódování souboru (výchozí: utf-8).

    Raises:
        FileNotFoundError: Pokud není cesta platná.
        TypeError: Pokud data nejsou JSON serializovatelná.
        Exception: Pokud došlo k chybě při zápisu.
    """
    if data is None:
        data = {}
    with open(path, mode='w', encoding=encoding) as json_file:
        json.dump(data, json_file)


def csvfile_read(path, encoding='utf-8'):
    """Načte data z CSV souboru.

    Args:
        path (str): Cesta k CSV souboru.
        encoding (str): Kódování souboru (výchozí: utf-8).

    Returns:
        list: Seznam slovníků reprezentujících řádky CSV.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
        Exception: Pokud došlo k chybě při čtení.
    """
    with open(path, encoding=encoding, newline='\n') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
        return [line for line in reader]


def csvfile_write(path, data=None, encoding='utf-8'):
    """Uloží data do CSV souboru.

    Args:
        path (str): Cesta k CSV souboru.
        data (list): Seznam slovníků reprezentujících řádky CSV (výchozí: prázdný seznam).
        encoding (str): Kódování souboru (výchozí: utf-8).

    Raises:
        FileNotFoundError: Pokud není cesta platná.
        IndexError: Pokud je seznam dat prázdný.
        ValueError: Pokud data nejsou validní seznamem slovníků.
        Exception: Pokud došlo k chybě při zápisu.
    """
    if data is None:
        data = []
    
    if not data:
        raise ValueError("Data nesmí být prázdné.")
    
    if not isinstance(data, list):
        raise ValueError("Data musí být seznam slovníků.")
    
    if not isinstance(data[0], dict):
        raise ValueError("Každý prvek dat musí být slovník.")
    
    with open(path, mode='w', encoding=encoding, newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for row in data:
            writer.writerow(row)

