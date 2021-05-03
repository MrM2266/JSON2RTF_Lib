# JSON2RTF_Lib
=================================================
Script pro vytváření dokumentů na základě šablon a dat uložených v JSON
Program by měl být schopný pracovat s rtf dokumenty a podle JSON struktury je vyplňovat


Update 20.4.
=================================================
- první pokus o dosažení základní funkcionality programu


Update 21.4.
=================================================
- definována třída CData - instance input a output - třída poskytuje metody pro čtení dat
  ze souboru a pro zápis
- funkce Process přijímá jako parametr string - hledá v něm flag - ten musí mít daný tvar
- flagy se hledají pomocí regex a jsou rozděleny do skupin:
  - start flag - je na začátku struktury
  - end flag - ukončuje danou strukturu
  - item flag - pro konkrétní položku

  - start flag: [[A:klic]] [[O:klic]]
  - end flag: [[E:klic]]
  - item flag: [[I:klic]]

  - kliče jsou zatím nutné - každá položka musí mít název -> flag [[A]] je ignorován

Funkce Process
================
- přijme string data
- vyhledá první start flag
- to co je před flagem předá do output
- najde odpovídající koncový flag např. [[A:osoby]] zde jsou v poli vypsané osoby [[E:osoby]]
- určí o jakou strukturu se jedná - array, object, item a obsah mezi flagy odešle do přísl. fce
- vstupní string data si zkrátí o zpracované části (vymaže z něj to, co je vyřešené) a 
  opakuje celý proces, dokud není str data celý zpracovaný - tzn, je prázdný

- dále jsou ve scriptu fce Array, Object a Item
- ty jako parametry přijímají str data a str key


Update 3.5.
=================================================
- doplněny funkce Array, object a Item
- pokrytí některých mezních případů v RTF

Item
=========
- značka pro označení místa, který má být nahrazeno daty z json
- při použití [[I:klíč]] očekáváme, že v json je "klíč":"string nebo číslo, které se vypíše"
- rtf kód [[I:jmeno]] se nahradí pomocí json "jmeno":"Pavel" na Pavel


Array
========
- [[A:osoby]] označuje pole, které odpovídá klíči osoby tzn. json "osoby":["jmeno":"Petr","jmeno":"Pavel"]
- rtf kód, který je mezi [[A:osoby]] [[E:osoby]] popisuje, co se má dělat s jedním prvkem pole - kód se zopakuje tolikrát, kolik má pole v json prvků - zde dvakrát - pro každý prvek pole jednou
- rtf kód [[A:auta]][[E:auta]] odpovídá json "auta":[ "Ford", "BMW", "Fiat" ] - výstupem jsou vypsané prvky pole auta; zavolá se fce ArrayAsStr - očekáváme, že pole obsahuje stringy nebo čísla, která se pouze vypíšou
- sytax: [[A:key]]popis jednoho prvku pole[[E:key]]

Object
========
- rtf kód [[O:osoba]] zavolá fci jsonReader.Object(osoba) - reader ví, že jsme v objektu "osoba":{"jmeno":Petr, "pratele":["Jan", "Helena"]}
- rtf kód [[O:null]] označuje objekt bez jména: v json {"jmeno":Petr, "pratele":["Jan", "Helena"]} - zavolá fci jsonReader.Object(none) ?? - reader ví, že má vzít první objekt v pořadí
- [[E:null]] ukončuje čtení objektu 


TODO:
================
- čtení z JSON
- ujasnit si, co má program dělat v object
- vytvořit key null - JSON Reader bude brát prvky postupně - díky A:employees ví, že je v poli employees a tam jde postupně - objekt po objektu
- doplnit boolean flag [[B:pritomen]]