import re
import json

class CData:
    def __init__(self):
        self.m_data=""
        self.m_filename=""

    def Add(self, add): ##prijme string, ktery si prida do m_data
        self.m_data += str(add)

    def Print(self):
        print(self.m_data)

    def WriteToFile(self): ##zapíše m_data do zadaného souboru
        file = open(self.m_filename, "w")
        file.write(self.m_data)
        file.close();

    def LoadFile(self, path): ##načte do m_data ze zadaného souboru
        file = open(path, "r")
        self.m_data = file.read() ##toto je string print(type(data))
        file.close()

    def SetFilename(self, filename):
        self.m_filename = filename


class CjsonReader:
    def __init__(self):
        self.m_levels = [] ##list jednotlivých levelů ## current je vždy poslední prvek pole ##co jeden prvek, to jeden level
        self.m_level = 0
        self.m_indexes = [0] ##list indexů - index 0 obsahuje hodnotu 2 -> na levelu 0 jsem na indexu 2

    def LoadFile(self, filename):
        with open(filename) as file:
            self.m_levels.append(json.load(file))

    def Down(self, key): ##půjde o úroveň dolů - na zadaný key nebo index ->vstup je index nebo key
        self.m_levels.append(self.m_levels[self.m_level][key])
        self.m_indexes.append(0)
        self.m_level += 1

    def Up(self): ##půjde o úroveň nahoru
        if self.m_level > 0:
            del self.m_levels[-1]
            del self.m_indexes[-1]
            self.m_level -= 1
        else:
            print("\nERROR: Up was blocked\n")

    def GetItem(self, key): ##vrátí položku podle klíče z aktuálního levelu - vrací pole i objekty
        return self.m_levels[self.m_level][key]

    def GetArraySize(self, key):
        return len(self.m_levels[self.m_level][key])

    def GetRootSize(self):
        return len(self.m_levels[0])

    def GetArrayAsStr(self, key):
        result = ""
        for i in self.m_levels[self.m_level][key]:
            result = result + str(i) + ", "
        return result[:-2]

    def PrintLast(self): ##vypíše poslední položku m_levels tzn. aktuálně zpracovávaný level
        print("Level: " + str(self.m_level) + " || " + str(self.m_levels[-1]) + "\n")

    def NextElement(self): ##v aktuálním levelu (pouze array) se posune o jeden prvek dopředu
        self.m_indexes[self.m_level] += 1

    def GetIndex(self):
        return self.m_indexes[self.m_level]


 
def FlagStart(data):
    ## najde ve str data první flag a zjistí informace - jaký to je flag, jeho klíč, začátek a konec - vše vrátí
    ## pokud nenajde - vrací none
     match = re.search("\[{2}((A:[a-zA-Z0-9]+)|(O:[a-zA-Z0-9]+)|(I:[a-zA-Z0-9]+))\]{2}", data)
     if match:
         flag = data[match.start() + 2 : match.start() + 3]
         key = data[match.start() + 4 : match.end() - 2]
         return [flag, key, match.start(), match.end()]
     else:
         return None


def FlagEnd(data, key):
    ## vrací pozici koncového tagu zadaného klíče
    ## vrací začátek a konec tagu
    if (key == "null"):
        list = []
        start=[]
        end=[]

        for match in re.finditer("\[{2}(A|O):null\]{2}", data):
            s = match.start()
            list.append(s)
            start.append(s)
        for match in re.finditer("\[{2}E:null\]{2}", data):
            s = match.start()
            list.append(s)
            end.append(s)

        list.sort()
        count=0

        for i in list:
            if i in start:
                count += 1
            if i in end:
                count -= 1
            if (count == 0):
                return [i,i+10]
    else:
        str = "[[E:" + key + "]]"
        return [data.find(str), data.find(str) + len(str)]

def Process(data):
    ## přijme str data a zpracuje ho - najde první flag a k němu koncový flag - to co je před ním dá to output
    ## obsah flagu pošle do fce a to za end flagem vrátí - usekne první flag a nechá ho zpracovat
    start = FlagStart(data)
    if start != None:
        output.Add(data[0:start[2]])
    
        if start[0] != "I":
            end = FlagEnd(data, start[1])
            if start[0] == "A":
                Array(data[start[3]:end[0]], start[1])
            if start[0] == "O":
                Object(data[start[3]:end[0]], start[1])
            return data[end[1]:]
        else:
            Item(start[1])
            return data[start[3]:]
    else:
        output.Add(data)
        output.WriteToFile()
        return ""

def Array(data, key):
    ##jsme v poli key - vrátí počet prvků v poli
    if data != "":
        if (key == "root"):
            pocet_prvku = jsonData.GetRootSize()
        if (key == "null"):
            pocet_prvku = jsonData.GetArraySize(jsonData.GetIndex())
            jsonData.Down(jsonData.GetIndex()) ##do rootu se dostanu otevřením souboru - zde musím udělat krok sám
        if (key != "null" and key != "root"): ##je to pole v objektu
            pocet_prvku = jsonData.GetArraySize(key)
            jsonData.Down(key)

        for i in range(0, pocet_prvku):
            temp = data
            while (temp != ""):
                temp = Process(temp)
                jsonData.NextElement()

        if (key != "root"):
            jsonData.Up() ##pole je vyřešené -> lezeme nahoru o jednu úroveň

    else:
        output.Add(jsonData.GetArrayAsStr(key))

    

def Object(data, key):
    if (key == "root"):
        pass
    if (key == "null"):
        jsonData.Down(jsonData.GetIndex()) ##do rootu se dostanu otevřením souboru - zde musím udělat krok sám
    if (key != "null" and key != "root"):
        jsonData.Down(key)

    while (data != ""):
        data = Process(data)

    if (key != "root"):
        jsonData.Up()


def Item(key):
    output.Add(jsonData.GetItem(key))





input = CData()
output = CData()
jsonData = CjsonReader()

input.LoadFile("kartaZamestnancu.rtf")
output.SetFilename("output.rtf")
jsonData.LoadFile("data1.json")

while(input.m_data != ""):
    input.m_data = Process(input.m_data)


##print("\n\n\nInput\n======================")
##input.Print()
##print("\n\n\nOutput\n=====================")
##output.Print()
