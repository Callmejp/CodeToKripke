#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019.10.4
# @Author  : 蒋洪剑
# @FileName: core.py


import process
from queue import Queue
from config import *
from state import TypeToken
from graphviz import Digraph
import argparse


def readCodeFromFile(filepath):
    """
    @name: readCodeFromFile
    @description: Read the code from the file.
    @param: 
        filepath{str}: the file path.
    @return: 
        localCodeList{list}: each element is a segment of code.
    """
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


def toString(tempStr):
    """
    @name: toString
    @description: Replace the identifier with its value.
    @param: 
        tempStr{str}: the identifier or IntLiteral
    @return: 
        {str}: IntLiteral.
    """
    if tempStr.isalpha():
        return str(currentNode[tempStr])
    else:
        return tempStr


def isEqual(n1, n2):
    """
    @name: isEqual
    @description: Judge if two dicts without "node" key are equal.
    @param: 
        n1&n2{dict}: the node dict.
    @return: 
        {bool}: 
    """
    n1.pop("node")
    n2.pop("node")
    if n1 == n2:
        return True
    
    return False


def judgeExpression(expression):
    """
    @name: judgeExpression
    @description: Determine whether the expression is true or false.
    @param: 
        expression{str}: the expression string.
    @return: 
        {bool}: 
    """
    process.initializeGlobalVariable()
    wordList, contentList = process.translateToKripke(expression, currentCount, 1)
    localLength = len(wordList)
    newExpe = ""
    for i in range(localLength):
        if wordList[i] == TypeToken.Identifier:
            newExpe += str(currentNode[contentList[i]])
        elif wordList[i] == TypeToken.true:
            newExpe += "True"
        elif wordList[i] == TypeToken.false:
            newExpe += "False"
        else:
            newExpe += contentList[i]
    
    return eval(newExpe)


def drawKripke():
    """
    @name: drawKripke
    @description: Draw the graph according to the edge list.
    @param: 
    @return:  
    """
    dot = Digraph(name="MyPicture", comment="the test", format="png")

    for i in range(nodeCount):
        t = nodeList[i]
        
        label = ""
        for var in allvariableList:
            label += str(t[var]) + ", "
        # print(label)
        label = label + str(t["pc0"]) + ", " + str(t["pc1"])
        
        dot.node(name=str(i+1), label=label, color='black')

    for i in range(1, nodeCount+1):
        for j in edge[i]:
            dot.edge(str(i), str(j), color='black')

    # dot.view(filename="mypicture", directory="D:\MyTest")

    dot.render(filename='MyPicture', directory="D:\MyTest",view=True)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str, help="location of the code-txt you wanna test.")
    parser.add_argument("nodecount", type=int, help="number of the nodes you wanna generate.")
    args = parser.parse_args()

    codeList = readCodeFromFile(args.filepath)
    initialNode = {"pc0": "L1", "pc1": "L1", "node": 1}
    # print(codeList)
    currentCount = 0
    finalResult = []
    for c in codeList:
        process.initializeGlobalVariable()
        initialNode["pc1"] = "L" + str(currentCount + 1)
        _, currentCount = process.translateToKripke(c, currentCount+1)
        for temp in _:
            if len(temp["type"]) > 2:
                continue
            finalResult.append(temp)
    
    # print(finalResult)
    
    # handle the existed variables
    allvariableList = list(set(process.varList))
    
    allvariableList.sort()
    for var in allvariableList:
        initialNode[var] = 0
    print(initialNode)

    # edge lists
    edge = [[] for i in range(args.nodecount+10)]
    nodeCount = 1
    
    # store all nodes
    nodeList = []
    nodeList.append(initialNode)
    q = Queue()
    q.put(initialNode)

    while not q.empty():
        currentNode = q.get()
    
        # print(currentNode)
        for tranCondition in finalResult:
            if currentNode["pc0"] != tranCondition[frontLabel] and currentNode["pc1"] != tranCondition[frontLabel]:
                continue

            newNode = currentNode.copy()
            # wait
            if tranCondition["type"] == "6":
                if judgeExpression(tranCondition[conditionExp]):
                    if currentNode["pc0"] == tranCondition[frontLabel]:
                        newNode["pc0"] = tranCondition[backLabel]
                    else:
                        newNode["pc1"] = tranCondition[backLabel]
            # if else
            elif tranCondition["type"] == "3":
                if judgeExpression(tranCondition[conditionExp]):
                    if currentNode["pc0"] == tranCondition[frontLabel]:
                        newNode["pc0"] = tranCondition[ifTrueLabel]
                    else:
                        newNode["pc1"] = tranCondition[ifTrueLabel]
                else:
                    if currentNode["pc0"] == tranCondition[frontLabel]:
                        newNode["pc0"] = tranCondition[ifFalseLabel]
                    else:
                        newNode["pc1"] = tranCondition[ifFalseLabel]
            # while
            elif tranCondition["type"] == "4":
                if judgeExpression(tranCondition[conditionExp]):
                    if currentNode["pc0"] == tranCondition[frontLabel]:
                        newNode["pc0"] = tranCondition[whileTrueLabel]
                    else:
                        newNode["pc1"] = tranCondition[whileTrueLabel]
                else:
                    if currentNode["pc0"] == tranCondition[frontLabel]:
                        newNode["pc0"] = tranCondition[whileFalseLabel]
                    else:
                        newNode["pc1"] = tranCondition[whileFalseLabel]
            # simple cases
            else:
                # b = a / b = 1
                if tranCondition["type"] == "1":
                    # b
                    modifyVariable = tranCondition[identifier1]
                    # eval("1")
                    newNode[modifyVariable] =  eval(toString(tranCondition[identifier2]))
                # b = a * 2
                elif tranCondition["type"] == "2":
                    # b
                    modifyVariable = tranCondition[identifier1]
                    # eval("1 * 2")
                    exper = toString(tranCondition[identifier2]) + tranCondition[operator] + toString(tranCondition[identifier3])
                    newNode[modifyVariable] = eval(exper)
                # skip
                elif tranCondition["type"] == "5":
                    pass
                

                if currentNode["pc0"] == tranCondition[frontLabel]:
                    newNode["pc0"] = tranCondition[backLabel]
                else:
                    newNode["pc1"] = tranCondition[backLabel]

            
            flag = 1
            for n in nodeList:
                if isEqual(n.copy(), newNode.copy()):
                    edge[currentNode["node"]].append(n["node"])
                    flag = 0
            if flag:
                nodeCount += 1
                newNode["node"] = nodeCount
                edge[currentNode["node"]].append(nodeCount)
                nodeList.append(newNode)
                q.put(newNode)

        if nodeCount >= args.nodecount:
            break
    # print(nodeList)
    # print(edge)
    drawKripke()
            
            

            








    
