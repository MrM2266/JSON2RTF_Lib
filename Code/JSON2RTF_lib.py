import re
import json

class CData:
    def __init__(self):
        self.m_data=""

    def Add(self, add):
        """Gets a string that is added to m_data
	
	    Args:
		add: value that is added to m_data
	    """
        self.m_data += str(add)

    def LoadData(self, data):
        """Takes rtf file as a string and stores it into m_data
	
	    Args:
		    data: rtf as string - from fastAPI
	    """
        self.m_data = data


class CjsonReader:
    def __init__(self):
        self.m_levels = [] #list of individual levels, current is always the last item of the array
        self.m_level = 0
        self.m_indexes = [0] #list of indexes (index 0 contains value 2 -> I'am on an index 2 on level 0

    def LoadData(self, jsonString, decode):
        """Takes JSON as bytes. If decode is 1 JSON is decoded using ANSI and then stored into m_levels.

        Args:
            jsonString: jsonFile as bytes - from fastAPI
            decode: parameter; if 1 -> string is decoded using cp1250; if 0 -> string is stored without decoding
        """
        if (decode == 1):
            self.m_levels.append(json.loads(str(jsonString, 'cp1250')))
        else:
            self.m_levels.append(json.loads(jsonString))

    def Down(self, key):
        """Gets you down a level to entered key or index
        
	    Args:
		    key: Index or key you want to step down to 
	    """
        self.m_levels.append(self.m_levels[self.m_level][key])
        self.m_indexes.append(0)
        self.m_level += 1

    def Up(self):
        """Gets you up a level
	    """
        if self.m_level > 0:
            del self.m_levels[-1]
            del self.m_indexes[-1]
            self.m_level -= 1

    def GetItem(self, key):
        """Returns string from JSON dictionary
	
	    Args:
	        key: JSON dictionary key to find desired string

	    Returns:
		    str: string found under parameter key
        """
        return self.m_levels[self.m_level][key]

    def GetArraySize(self, key):
        """Returns the size of an array
	
	    Args:
            key: Key of an array you want to get the size of

	    Returns:
		    int: Size of an array
        """
        return len(self.m_levels[self.m_level][key])

    def GetRootSize(self):
        """Returns the size of root array

	    Returns:
		    int: Size of root
        """
        return len(self.m_levels[0])

    def GetArrayAsStr(self, key):
        """Returns array as one string - elements are separated with ,
	
	    Args:
            key: Key of an array you want to get as a string

	    Returns:
		    int: Size of anarray
        """
        result = ""
        for i in self.m_levels[self.m_level][key]:
            result = result + str(i) + ", "
        return result[:-2]

    def GetRootAsStr(self):
        """Returns root array as one string - elements are separated with ,
	
	    Args:
            key: Key of an array you want to get as a string

	    Returns:
		    int: Size of root
        """
        result = ""
        for i in self.m_levels[0]:
            result = result + str(i) + ", "
        return result[:-2]

    def NextElement(self):
        """Moves you one item forward in current level (only in array)
        """
        self.m_indexes[self.m_level] += 1

    def GetIndex(self):
        """Returns index of processing element on current level

        Returns:
            int: index of an element
        """
        return self.m_indexes[self.m_level]



 
def FlagStart(data):
     """Finds the first flag in a string of data and finds out information  
     
     Information: What flag is it, it's key, beginning and end
	  
     Args:
         data: String of data you want to find the information about
     
     Returns:
         [flag, key, match.start(), match.end()]: if the functions finds out the information
         None: if the function doesn't find out any information  
     """
     match = re.search("\[{2}((A:[a-zA-Z0-9]+)|(O:[a-zA-Z0-9]+)|(I:[a-zA-Z0-9]+))\]{2}", data)
     if match:
         flag = data[match.start() + 2 : match.start() + 3]
         key = data[match.start() + 4 : match.end() - 2]
         return [flag, key, match.start(), match.end()]
     else:
         return None


def FlagEnd(data, key):
    """Returns the positon of the ending tag
	
    Args:
        data: String of data in which you want to find the position of the ending tag
        key: Value of the ending tag

    Returns:
        Positon of the ending tag
        Beginning and ending of the tag
    """
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
    """Takes string data and finds the first tag from the beginning (start tag) and corresponding end tag
    Text that is before start flag is added to output
    Text that is after end flag is left for another loop
    The code between the start flag and the end flag is passed into Process function again

    Args:
        data: string to process

    Returns:
        str: text that is after the end flag - code for another loop
    """

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
        return ""

def Array(data, key):
    """Function to process the code of an array

    Args:
        data: code of an array to process
        key: name of the array
    """
    if data != "":
        if (key == "root"): ##root array
            pocet_prvku = jsonData.GetRootSize()
        elif (key == "null"): ##array in array
            pocet_prvku = jsonData.GetArraySize(jsonData.GetIndex())
            jsonData.Down(jsonData.GetIndex())
        else: ##array in object
            pocet_prvku = jsonData.GetArraySize(key)
            jsonData.Down(key)

        for i in range(0, pocet_prvku):
            temp = data
            while (temp != ""):
                temp = Process(temp)
            jsonData.NextElement()

        if (key != "root"):
            jsonData.Up()

    else:
        if (key == "null"):
            output.Add(jsonData.GetArrayAsStr(jsonData.GetIndex()))
        elif (key == "root"):
            output.Add(jsonData.GetRootAsStr())
        else:
            output.Add(jsonData.GetArrayAsStr(key))

    

def Object(data, key):
    """Function to process the code of an object

    Args:
        data: code of an object to process
        key: name of the object
    """
    if (key == "null"):
        jsonData.Down(jsonData.GetIndex())
    elif (key != "root"):
        jsonData.Down(key)

    while (data != ""):
        data = Process(data)

    if (key != "root"):
        jsonData.Up()


def Item(key):
    """Function to get string from JSON dictionary

    Args:
        key: name of the string
    """
    output.Add(jsonData.GetItem(key))




def Init():
    """Creates all necesary variables
    """
    global input
    input = CData()
    global output
    output = CData()
    global jsonData
    jsonData=CjsonReader()

def LoadJson(jsonString, decode):
    """Passes data into jsonReader

    Args:
        str jsonString: json file as a string
        decode: parameter if 1 -> string is decoded using cp1250; if 0 -> string is stored without decoding
    """
    jsonData.LoadData(jsonString, decode)

def LoadRTF(string):
    """Passes data into input

    Args:
        str string: rtf input file as a string
    """
    input.LoadData(string)

def ProcessRTF():
    """Function to process rtf
    """
    while(input.m_data != ""):
        input.m_data = Process(input.m_data)

def GetOutput():
    """Returns output rtf

    Returns:
        output.m_data: output rtf file
    """
    return output.m_data