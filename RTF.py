import re

class CData:
    def __init__(self):
        self.m_data=""

    def Add(self, add): ##prijme string, ktery si prida do m_data
        self.m_data += add

    def Print(self):
        print(self.m_data)

    def WriteToFile(self, path): ##zapíše m_data do zadaného souboru
        file = open(path, "w")
        file.write(self.m_data)
        file.close();

    def LoadFile(self, path): ##načte do m_data ze zadaného souboru
        file = open(path, "r")
        self.m_data = file.read() ##toto je string print(type(data))
        file.close()

    def Remove(self, start): ##odstraní část stringu - vše od start zůstane zachováno
        self.m_data=self.m_data[start:]



class CjsonReader:
    def __init__(self):
        m_data = 0

    def Array(self):
        ## tato fce se zavolá, jakmile se v rtf narazí na pole
        ## json a rtf musí navzájem sedět - první prvek v rtf je array -> první prvek v json je taky array
        ## jsonReader načte pole z json
        print("Hledam v poli")

    def Object(self):
        print("Hledam v objektu")

    def Item(self, name):
        print("Hledam polozku {0}", name)

    def LoadFile(self, filename):
        print("Nacitani json souboru")


 
def FlagStart(data):
    ## najde ve str data první flag a zjistí informace - jaký to je flag, jeho klíč, začátek a konec - vše vrátí
    ## pokud nenajde - vrací none
     match = re.search("\[{2}((A:[a-zA-Z0-9]+)|(O:[a-zA-Z0-9]+)|(I:[a-zA-Z0-9]+))\]{2}", data)
     if match:
         flag = data[match.start():match.start() + 3]
         key = data[match.start() + 4 : match.end() - 2]
         return [flag, key, match.start(), match.end()]
     else:
         return None

def FlagEnd(data, key):
    str = "[[E:" + key + "]]"
    return [data.find(str), data.find(str) + len(str)]

def Process(data):
    ## přijme str data a zpracuje ho - najde první flag a k němu koncový flag - to co je před ním dá to output
    ## obsah flagu pošle do fce a to za end flagem vrátí - usekne první flag a nechá ho zpracovat
    start = FlagStart(data)
    if start != None:
        output.Add(data[0:start[2]])
    
        if start[0] != "[[I":
            end = FlagEnd(data, start[1])
            if start[0] == "[[A":
                Array(data[start[3]:end[0]], start[1])
            if start[0] == "[[O":
                Object(data[start[3]:end[0]], start[1])
            return data[end[1]:]
    
        else:
            Item(start[1])
            return data[start[3]:]
    
    else:
        output.Add(data)
        output.WriteToFile("output.rtf")
        return ""

##všechny fce mají jako parametr string
    ## zde se bude procházet string data - podle json se bude opisovat
    ## vyhodnocovací loop pro flagy - najde flag, najde konec a odešle do příslušné fce
    ## zapisuje do output pomocí output.Add - fce má přístup do output
    ## jakmile nějakou část vyřeší - opíše nebo předá do jiné fce, tak si zkrátí string data - vymaže vyřešený text
    ## fce pojede v loopu dokud nebude mít string data prázdný:
    ## data=data[len(data):len(data)]
    ##   if data == "":
    ##   print("1")
    ## loop dokud není string data prázdný
    ## najde si nejbližší flag - to před ním opíše tolikrát, kolik je prvků v json
    ## část textu mezi flagy odešle do dané fce
    ## vyřešený úsek textu si vymaže z str data data=data[start:]
    ## pokud už nemá flagy, opíše to co mu zbylo tolikrát, kolik má prvků v json - tím se vyprázdní str data - fce se ukončí
    ## pokud ještě má flag - loop běží znovu - opíše to před flagem atd.

def Array(data, key):
    cislo_prvku = 1 ##from json
    ## pole má data pro zpracování a ví, jaký má klíč v json - klíč pošle do json, vrátí se mu počet opakování
    ## začne zpracovávat data - pošle je do process - process opíše to co je před prvním flagem, 
    ## for (i=0 ; i < pocet_opakovani_json - 1; i++):
    ##      Process(data)
    ## data = Process(data)
    print(key)
    print("Array\n===============")
    print(data) ##remove
    print("\n\n")
    output.Add("   ===|||KOD Z POLE: ")
    output.Add(key)
    output.Add("|||===    ")
    

def Object(data, key):
    print(key)
    print("Object\n===============")
    print(data) ##remove
    print("\n\n")
    output.Add("   ===|||KOD Z OBJEKTU: ")
    output.Add(key)
    output.Add("|||===    ")

def Item(key):
    print(key)
    print("Item\n===============\n\n")
    output.Add("   ===|||KOD Z POLOZKY: ")
    output.Add(key)
    output.Add("|||===    ")






input = CData()
output = CData()

input.LoadFile("test2.rtf")

while(input.m_data != ""):
    input.m_data = Process(input.m_data)
    break


print("\n\n\nInput\n======================")
input.Print()
print("\n\n\nOutput\n=====================")
output.Print()
