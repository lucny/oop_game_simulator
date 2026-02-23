# Infografické prompty pro generování prezentací

Tato složka obsahuje čtyři profesionální prompty ve formátu pro AI generátor obrázků Nano Banana Pro (nebo kompatibilní modely). Prompty popisují čtyřsnímkové infografické prezentace zaměřené na různé aspekty OOP a turnajového systému.

## Soubory

### prompt1.txt - OOP Princip: Abstrakce a Polymorfismus
**Téma:** Objektově orientované principy v projektu

Popisuje čtyři panely:
1. **BaseTournament** - Abstraktní třída jako definice rozhraní
2. **Dědičnost a polymorfismus** - RoundRobinTournament a EliminationTournament
3. **Factory pattern** - TournamentFactory pro vytváření instancí
4. **Výhody abstrakce** - Porovnání s podmínkovým kódem

**Didaktický obsah:** Ukazuje, jak abstraktní dědičnost eliminuje potřebu vnořených podmínek a umožňuje jednoduchého přidávání nových typů turnajů.

---

### prompt2.txt - Algoritmy: Turnajové struktury
**Téma:** Matematika a algoritmy turnajů

Popisuje čtyři panely:
1. **Round-robin turnaj** - Rotační algoritmus, N-1 kol
2. **Eliminační turnaj** - Bracket struktura s logaritmickou hloubkou
3. **Bye hráči** - Výpočet nasazených hráčů (příklad 13 hráčů)
4. **Prokládání** - Interleaving nasazených a nenasazených hráčů

**Didaktický obsah:** Demonstruje matematiku za turnajovými algoritmy a specificky vysvětluje problém, který projekt řeší - správné výpočtu bye hráčů a jejich umístění v bracketu.

---

### prompt3.txt - Architektura: Tok dat
**Téma:** Data flow a systémová architektura

Popisuje čtyři panely:
1. **Vstupní data** - players.json a jeho struktura
2. **Tvorba turnaje** - Orchestrace objektů a jejich vztahy
3. **Zpracování turnaje** - Flow dat během běhu
4. **Výstupní data** - tournament_results.json s kompletními výsledky

**Didaktický obsah:** Ukazuje kompletní cestu dat skrz aplikaci od načtení přes zpracování až k uložení, s důrazem na objektové vztahy a separaci odpovědnosti.

---

### prompt4.txt - Kvalita kódu: Best Practices
**Téma:** Softwarové inženýrství a zlepšování kvality

Popisuje čtyři panely:
1. **Eliminace podmínek** - If/Elif anti-pattern vs. polymorfismus
2. **Abstraktní dědičnost** - Moderní OOP řešení
3. **Testovatelnost** - Automatické testy a pokrytí
4. **Rozšiřitelnost** - Přidání nového typu turnaje

**Didaktický obsah:** Demonstruje jak abstraktní dědičnost vede k lepší kódové kvalitě, vyšší testovatelnosti, a jednoduššímu přidávání nových funkcí.

---

## Použití promptů

Tyto prompty jsou navrženy pro generování obrázků v AI modelech s následujícími vlastnostmi:

- **Formát:** 2×2 grid = 4 panel
- **Poměr stran:** 16:9 (Full HD)
- **Kvalita:** Fotorealistické 4K
- **Jazyk:** Čeština
- **Styl:** Minimalistický, profesionální, vzdělávací
- **Bez:** Karikatur, emoji, chyb v gramatice
- **S:** Realistickými diagramy, UML, kódem, metrikami

### Příklad použití:
1. Zkopíruj obsah z jednoho ze souborů (prompt1.txt, prompt2.txt, atd.)
2. Vlož do AI generátoru obrázků (Midjourney, DALL-E, Stable Diffusion s upřesněním, Nano Banana Pro atd.)
3. Vygeneruj obrázek
4. Obrázek lze použít pro:
   - Přednášky a semináře
   - Studijní materiály
   - Blog články a wiki
   - YouTube thumbnaily
   - Vzdělávací plakáty

---

## Struktura promptu (Template)

Každý prompt má jednotnou strukturu:

```
A photorealistic 4K educational infographic divided into a 2x2 grid...

Top left panel: [Téma 1]. Subheading: „[Podtitul 1]". 
Central scene shows... Labels in Czech: ...

Top right panel: [Téma 2]. Subheading: „[Podtitul 2]". 
Central scene shows... Labels in Czech: ...

Bottom left panel: [Téma 3]. Subheading: „[Podtitul 3]". 
Central scene shows... Labels in Czech: ...

Bottom right panel: [Téma 4]. Subheading: „[Podtitul 4]". 
Central scene shows... Labels in Czech: ...

Overall aesthetic: cohesive educational comparison layout...
```

---

## Barvy a symboly

Prompty využívají konzistentní barvy pro jednotlivé koncepty:

- **Modrá** - Datové toky, vstupní parametry, základní prvky
- **Zelená** - Pozitivní prvky, správný kód, zavedené metody
- **Oranžová** - Výstup, transformace, procesní kroky
- **Purpurová** - Abstraktní prvky, rozhraní
- **Červená** - Anti-patterny, chyby, zastaralé přístupy

---

## Případové studie a rozšíření

Prompty lze snadno adaptovat pro jiné projekty:

1. **Změna tématu** - Uprav "tournament system" na jiný projekt
2. **Rozšíření panelů** - Zvětši na 3×2 grid (6 panelů) upřesněním
3. **Jiný jazyk** - Přepiš všechny "Labels in Czech" na cílový jazyk
4. **Různé aspekty** - Vytvoř prompty zaměřené na nové koncepty

---

## Technické poznámky

- Prompty jsou optimalizovány pro modely s podporou detailních instrukcí
- Obsahují specifické termíny (UML, polymorfismus, ABC modul) pro vyšší relevanci
- Barvy jsou popsány pojmenováním (blue, green, orange) nikoli hex kódy pro lepší generování
- Všechny popisy jsou v češtině pro korektní výstup

---

**Vytvořeno:** 23. února 2026  
**Projekt:** OOP Game Simulator  
**Verze:** 1.0
