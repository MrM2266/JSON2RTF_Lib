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


def FindFirstFlag(input, output): ##najde v data první flag - podle něj najde odpovídající koncový flag a odešle do přísl. fce
    match = re.search("\[{2}(A|D|O|(I:[a-zA-Z0-9]*))\]{2}", input.m_data)
    if match:
        flag=input.m_data[match.start():match.start() + 3]
        if flag == "[[A":
            output.Add(input.m_data[0:match.start()])
            Pole(input.m_data[match.end() : re.search("\[{2}A_E\]{2}", input.m_data).start()])
            input.Remove(re.search("\[{2}A_E\]{2}", input.m_data).end())
        if flag == "[[D":
            output.Add(input.m_data[0:match.start()])
            Dictionary(input.m_data[match.end() : re.search("\[{2}D_E\]{2}", input.m_data).start()])
            input.Remove(re.search("\[{2}D_E\]{2}", input.m_data).end())
        if flag == "[[O":
            output.Add(input.m_data[0:match.start()])
            Object(input.m_data[match.end() : re.search("\[{2}O_E\]{2}", input.m_data).start()])
            input.Remove(re.search("\[{2}O_E\]{2}", input.m_data).end())
        if flag == "[[I":
            output.Add(input.m_data[0:match.start()]) ##odešle do fce Item klíč pro hledání v json
            Item(input.m_data[match.start() + 4 : match.end() - 2])
            input.Remove(match.end())

    else:
        print("Nic nenalezeno")
 

##všechny fce mají jako parametr string
def Pole(data):
    ## zde se bude procházet string data - podle json se bude opisovat
    ## vyhodnocovací loop pro flagy - najde flag, najde konec a odešle do příslušné fce
    ## zapisuje do output pomocí output.Add
    ## jakmile nějakou část vyřeší - opíše nebo předá do jiné fce, tak si zkrátí string data - vymaže vyřešený text
    ## fce pojede v loopu dokud nebude mít string data prázdný
    ## loop dokud není string data prázdný
    ## najde si nejbližší flag - to před ním opíše tolikrát, kolik je prvků v json
    ## část textu mezi flagy odešle do dané fce
    ## vyřešený úsek textu si vymaže z str data data=data[start:]
    ## pokud už nemá flagy, opíše to co mu zbylo tolikrát, kolik má prvků v json - tím se vyprázdní str data - fce se ukončí
    ## pokud ještě má flag - loop běží znovu - opíše to před flagem atd.
    print("Pole\n===============")
    print(data) ##remove
    print("\n\n")

def Dictionary(data):
    print("Dictionary\n===============")
    print(data) ##remove
    print("\n\n")

def Object(data):
    print("Object\n===============")
    print(data) ##remove
    print("\n\n")

def Item(data):
    print("Item\n===============")
    print(data) ##remove
    print("\n\n")



input = CData()
output = CData()

input.LoadFile("test2.rtf")
FindFirstFlag(input, output)
print("\n\n\nInput\n======================")
input.Print()
print("\n\n\nOutput\n=====================")
output.Print()
