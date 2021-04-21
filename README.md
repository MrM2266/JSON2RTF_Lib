# JSON2RTF_Lib
=================================================

Script pro vytváření dokumentů na základě šablon a dat uložených v JSON.
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

TODO:
================
- fce Array, Object a Item odešlou key do JSONReader a ten vrátí data z JSON
- zde se bude zpracovávat obsah jednotlivých struktrur a bude se procházet str data pomocí fce
  Process - ta opět najde případné flagy a odešle danou část do příslušné fce - rtf se takto bude rozbalovat
- čtení z JSON
- ujasnit si, co má program dělat v array a object
- struktury bez klíčů - podpora pro [[A]] a [[A_E]]
