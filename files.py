import json, csv


def textfile_read(path, encoding='utf-8'):
    '''Načtení textového souboru

    Klíčové argumenty:
        path -- cesta k textovému souboru
        encoding -- kódování (výchozí utf-8)
    '''
    try:
        with open(path, encoding=encoding) as file:
            data = file.read()
    except FileNotFoundError:
        print(f'Soubor nebyl nalezen')
        return False
    except Exception as error:
        print(f'Chyba načtení souboru: {error} {type(error)}')
        return False
    finally:
        file.close()
    return data


def textfile_write(path, data='', encoding='utf-8'):
    '''Uložení do textového souboru

    Klíčové argumenty:
        path -- cesta k textovému souboru
        data -- ukládaný text (výchozí '')
        encoding -- kódování (výchozí utf-8)
    '''
    try:
        with open(path, mode='w', encoding=encoding) as file:
            file.write(data)
    except FileNotFoundError:
        print(f'Soubor nebyl nalezen')
        return False
    except Exception as error:
        print(f'Chyba zápisu do souboru: {error} {type(error)}')
        return False
    finally:
        file.close()
    return True


def jsonfile_read(path, encoding='utf-8'):
    try:
        with open(path, encoding=encoding) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f'Soubor nebyl nalezen')
        return False
    except Exception as error:
        print(f'Chyba načtení souboru: {error} {type(error)}')
        return False
    finally:
        json_file.close()
    return data


def jsonfile_write(path, data={}, encoding='utf-8'):
    try:
        with open(path, mode='w', encoding=encoding) as json_file:
            json.dump(data, json_file)
    except FileNotFoundError:
        print(f'Soubor nebyl nalezen')
        return False
    except Exception as error:
        print(f'Chyba zápisu do souboru: {error} {type(error)}')
        return False
    finally:
        json_file.close()
    return True


def csvfile_read(path, encoding='utf-8'):
    try:
        with open(path, encoding=encoding, newline='\n') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
            dict_list = []
            for line in reader:
                dict_list.append(line)
    except FileNotFoundError:
        print(f'Soubor nebyl nalezen')
        return False
    except Exception as error:
            print(f'Chyba načtení souboru: {error} {type(error)}')
            return False
    finally:
        csv_file.close()
    return dict_list


def csvfile_write(path, data = [], encoding='utf-8'):
    try:
        with open(path, mode='w', encoding=encoding, newline='\n') as file:
            writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
            writer.writeheader()
            for row in data:
                writer.writerow(row)


    except FileExistsError as error:
        print(f'Soubor nebyl nalezen: {error}')
        return False
    except Exception as error:
        print(f'Problém při otevírání souboru 2: {error} {type(error)}')
        return False
    finally:
        file.close()
    return True

