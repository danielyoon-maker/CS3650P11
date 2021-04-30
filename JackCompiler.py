import re

inKeyword = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return"
]

isSymbol = [
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '.',
    ',',
    ';', 
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
]

symbolDict = {
        '<': '&lt;',
        '>': '&gt;',
        '\"': '&quot;',
        '&': '&amp;'
    }

class JackAnalyzer():

    def __init__(self, filePath):
        self.file_name = filePath
        j = JackTokenizer(self.file_name)
        c = CompilationEngine(self.file_name)

class JackTokenizer():

    def __init__(self, file_name):
        self.file_name = file_name
        self.f = open(file_name + ".jack", "r")
        self.writer = open(file_name + "T.xml", "w")
        self.inComment = False
        self.startParsing()

    def startParsing(self):
        self.writer.write("<tokens>")
        for x in self.f:
            finished = 0
            x = self.stripComments(x)
            if(self.skipOrStay(x) == False):
                continue
            x = x.strip()
            splitTokenArray = self.splitTokens(x)
            splitTokenArray[:] = [z for z in splitTokenArray if z]
            started = False
            tempList = []
            for y in splitTokenArray:
                if y in inKeyword:
                    self.writer.write("<keyword> " + y + " </keyword>")
                elif (y in isSymbol) or (y in symbolDict.values()):
                    self.writer.write("<symbol> " + y + " </symbol>")
                elif y.isdigit():
                    self.writer.write("<integerConstant> " + y + " </integerConstant>")
                elif '"' in y:
                    started = not started
                    finished += 1
                    tempList.append(y.replace('"',''))
                elif started:
                    tempList.append(y)
                else:
                    self.writer.write("<identifier> " + y + " </identifier>") 
                if(finished == 2):
                    tempString = ""
                    for z in tempList:
                        tempString += (z + " ")
                    self.writer.write("<stringConstant> " + tempString.strip() + " </stringConstant>")
                    finished = 0
                    tempString = ""
        self.writer.write("</tokens>")


    
    def stripComments(self, line):
        if line.find("//") >= 0:
            return line.split("//")[0]
        elif line.find("/**") >= 0:
            self.inComment = True
            tempList = line.split("/**")
            for x in tempList:
                if "*/" in x:
                    self.inComment = False
            return tempList[0]
        elif line.find("*/") >= 0:
            self.inComment = False
            return line.split("*/")[1]
        elif self.inComment == True:
            return ""
        return line

    def skipOrStay(self, line): #checks to see if line is a comment or blank line
        if len(line.strip()) == 0:
            #return "empty"
            return False
        if "//" in line:
            #return "comment"
            return False
        #return "proceed"
        return True

    def splitTokens(self, line):
        newList = []
        tempString = ""
        splitLine = line.split(" ")
        for y in splitLine:
            found = False
            y = y.strip()
            listString = list(y)
            for a in listString:
                unfinishedString = True
                found = False
                for z in isSymbol:
                    if  a == z:
                        found = True
                        unfinishedString = False
                        if (z == "<" or z == ">" or z == '"' or z == "&"):
                            newList.append(symbolDict.get(z))
                            continue
                        newList.append(tempString)
                        tempString = ""
                        newList.append(a)
                if(not found):
                    tempString += a
            if(unfinishedString):
                newList.append(tempString)
                tempString = ""
        return newList

class CompilationEngine():

    def __init__(self, file_name):
        self.file_name = file_name
        self.f = open(file_name + ".jack", "r")
        self.writer = open(file_name + ".xml", "w")
        self.inComment = False
        self.startParsing()
        self.currentStack = []

    def startParsing(self):
        self.writer.write("<class>")
        for x in self.f:
            finished = 0
            x = self.stripComments(x)
            if(self.skipOrStay(x) == False):
                continue
            x = x.strip()
            splitTokenArray = self.splitTokens(x)
            splitTokenArray[:] = [z for z in splitTokenArray if z]
            started = False
            tempList = []
            for y in splitTokenArray:
                if y in inKeyword:
                    self.writer.write("<keyword> " + y + " </keyword>")
                elif (y in isSymbol) or (y in symbolDict.values()):
                    self.writer.write("<symbol> " + y + " </symbol>")
                elif y.isdigit():
                    self.writer.write("<integerConstant> " + y + " </integerConstant>")
                elif '"' in y:
                    started = not started
                    finished += 1
                    tempList.append(y.replace('"',''))
                elif started:
                    tempList.append(y)
                else:
                    self.writer.write("<identifier> " + y + " </identifier>") 
                if(finished == 2):
                    tempString = ""
                    for z in tempList:
                        tempString += (z + " ")
                    self.writer.write("<stringConstant> " + tempString.strip() + " </stringConstant>")
                    finished = 0
                    tempString = ""
        self.writer.write("</class>")


    
    def stripComments(self, line):
        if line.find("//") >= 0:
            return line.split("//")[0]
        elif line.find("/**") >= 0:
            self.inComment = True
            tempList = line.split("/**")
            for x in tempList:
                if "*/" in x:
                    self.inComment = False
            return tempList[0]
        elif line.find("*/") >= 0:
            self.inComment = False
            return line.split("*/")[1]
        elif self.inComment == True:
            return ""
        return line

    def skipOrStay(self, line): #checks to see if line is a comment or blank line
        if len(line.strip()) == 0:
            #return "empty"
            return False
        if "//" in line:
            #return "comment"
            return False
        #return "proceed"
        return True

    def splitTokens(self, line):
        newList = []
        tempString = ""
        splitLine = line.split(" ")
        for y in splitLine:
            found = False
            y = y.strip()
            listString = list(y)
            for a in listString:
                unfinishedString = True
                found = False
                for z in isSymbol:
                    if  a == z:
                        found = True
                        unfinishedString = False
                        if (z == "<" or z == ">" or z == '"' or z == "&"):
                            newList.append(symbolDict.get(z))
                            continue
                        newList.append(tempString)
                        tempString = ""
                        newList.append(a)
                if(not found):
                    tempString += a
            if(unfinishedString):
                newList.append(tempString)
                tempString = ""
        return newList

filetoRead = input("Please enter name of the file(no file extension): \n")
j = JackAnalyzer(filetoRead)