from config import FileName
from process import translateToKripke, initializeGlobalVariable


"""
Read the code from the file
"""
def readCodeFromFile(filepath):
    localCodeList = []
    codePart = ""
          
    with open(filepath, "r") as f:
        line = "code content"
        while line:   
            line = f.readline()
            if ":" in line:
                localCodeList.append(codePart)
                codePart = ""
                continue
            codePart += line
        localCodeList.append(codePart)
    localCodeList.pop(0)
    return localCodeList


if __name__ == "__main__":
    codeList = readCodeFromFile(FileName)
    # print(codeList)
    currentCount = 1
    for c in codeList:
        initializeGlobalVariable()
        currentCount = translateToKripke(c, currentCount)