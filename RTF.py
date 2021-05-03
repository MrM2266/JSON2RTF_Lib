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
        self.pocet = 0 ## pro ladeni

    def Array(self, arrayName):
        ## tato fce se zavolá, jakmile se v rtf narazí na pole; key je název pole v json
        ## fce vrací počet prvků v poli
        print("Hledam v poli", arrayName)
        return 2 #vrací počet prvků pole

    def Object(self, objectName):
        print("Hledam v objektu", objectName)

    def Item(self, itemName):
        ## vrací hodnotu z json "itemName":"hodnota_pro_vraceni"
        self.pocet += 1 ##pro ladeni
        return itemName + str(self.pocet)

    def LoadFile(self, filename):
        print("Nacitani json souboru")

    def ArrayAsString(self, arrayName):
        ## vrátí celé pole jako string
        ## pro případ "auta":[ "Ford", "BMW", "Fiat" ] -> vrací string "Ford BMW Fiat"
        return ("Vypsane prvky pole " + arrayName + " ")


 
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
    ## vrací pozici koncového tagu zadaného klíče
    ## vrací začátek a konec tagu
    print(data)
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
        ##output.WriteToFile("output.rtf")
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

def Array(data, key):
    pocet_prvku = json.Array(key) ##jsme v poli key - vrátí počet prvků v poli
        
    if data != "":
        for i in range(0,pocet_prvku):
            temp = data
            while (temp != ""):
                temp = Process(temp)

    else:
        output.Add(json.ArrayAsString(key))

    

def Object(data, key):
    json.Object(key)

    while (data != ""):
        data = Process(data)

def Item(key):
    output.Add(json.Item(key))






input = CData()
output = CData()
json = CjsonReader()

input.LoadFile("test3.rtf")

while(input.m_data != ""):
    input.m_data = Process(input.m_data)
    ##break


print("\n\n\nInput\n======================")
input.Print()
print("\n\n\nOutput\n=====================")
output.Print()
