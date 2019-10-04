#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019.10.4
# @Author  : JohnReese
# @FileName: state.py


from config import *
from state import TypeToken, DfaState
import logging


"""
Initial the logging config
"""
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

"""
global variables
"""
currentState = DfaState.Initial
wordList = []
contentList = []
# record the if & else & endif position
ifSegment = {}
# whether in the if-else code segment
inIf = False
# counter of sentences between if & else
countIfToElse = 0
# record the while & endwhile position
whileSegment = {}
# whether in the while-do code segment
inWhile = False
# counter of sentences between while & endwhile
countWhileToEnd = 0
# record the variables
varList = []


"""
some functions
"""
def initializeGlobalVariable():
    global currentState, wordList, contentList, ifSegment, inIf, countIfToElse, whileSegment, inWhile, countWhileToEnd

    currentState = DfaState.Initial
    wordList = []
    contentList = []
    ifSegment = {}
    whileSegment = {}
    inIf = False
    inWhile = False
    countIfToElse = 0
    countWhileToEnd = 0


def getWhilePosition(startPostion, whileCount):
    global whileSegment, inWhile, countWhileToEnd
    whileToEnd = 0
    localLength = len(wordList)
    whileSegment["startCount"] = whileCount
    
    while startPostion < localLength:
        if wordList[startPostion] == TypeToken.Endwhile:
            break
        if wordList[startPostion] == TypeToken.SemiColon or wordList[startPostion] == TypeToken.If:
            whileToEnd += 1
        startPostion += 1
    whileSegment[whileToEndCount] = whileToEnd

    inWhile = True
    countWhileToEnd = 0


def getIfPosition(startPostion):
    global ifSegment, inIf, countIfToElse
    ifToElse = elseToEnd = 0
    localLength = len(wordList)

    while startPostion < localLength:
        if wordList[startPostion] == TypeToken.Else:
            break
        if wordList[startPostion] == TypeToken.SemiColon:
            ifToElse += 1
        startPostion += 1
    ifSegment[ifToElseCount] = ifToElse

    while startPostion < localLength:
        if wordList[startPostion] == TypeToken.SemiColon:
            elseToEnd += 1
        if wordList[startPostion] == TypeToken.Endif:
            break
        startPostion += 1
    ifSegment[elseToEndCount] = elseToEnd
    
    inIf = True
    countIfToElse = 0


def handleInitialState(char):
    localState = DfaState.Initial
    
    if char.isalpha():
        if char == 'i':
            localState = DfaState.Id_if1
        elif char == 'e':
            localState = DfaState.Id_e1
        elif char == 'a':
            localState = DfaState.Id_and1
        elif char == 'o':
            localState = DfaState.Id_or1
        elif char == 's':
            localState = DfaState.Id_skip1
        elif char == 't':
            localState = DfaState.Id_t1
        elif char == 'w':
            localState = DfaState.Id_w1
        elif char == 'd':
            localState = DfaState.Id_do1
        elif char == 'f':
            localState = DfaState.Id_false1
        elif char == 'n':
            localState = DfaState.Id_not1
        elif char == 'c':
            localState = DfaState.Id_c1
        else:
            wordList.append(TypeToken.Identifier)
            contentList.append(char)
            # localState = DfaState.Initial
    elif char.isdigit():
        wordList.append(TypeToken.IntLiteral)
        contentList.append(char)
        # localState = DfaState.Initial
    elif char == '>':
        localState = DfaState.GT
    elif char == '<':
        localState = DfaState.LT
    elif char == '+':
        wordList.append(TypeToken.Plus)
        contentList.append("+")
        # localState = DfaState.Initial
    elif char == '-':
        wordList.append(TypeToken.Minus)
        contentList.append("-")
        # localState = DfaState.Initial
    elif char == ';':
        wordList.append(TypeToken.SemiColon)
        contentList.append(";")
        # localState = DfaState.Initial
    elif char == '*':
        wordList.append(TypeToken.Star)
        contentList.append("*")
        # localState = DfaState.Initial
    elif char == '(':
        wordList.append(TypeToken.LeftParen)
        contentList.append("(")
        # localState = DfaState.Initial
    elif char == ')':
        wordList.append(TypeToken.RightParen)
        contentList.append(")")
        # localState = DfaState.Initial
    elif char == '=':
        localState = DfaState.Assignment
    else:
        logging.debug("something unexpected has happend!")
    
    return localState

# ----------------------------------------------
# The entrance function
# ----------------------------------------------
def translateToKripke(codeContent, upToNowCount, flag=0):
    global currentState
    newCodeContent = codeContent + "^"
    # print(newCodeContent)
    for char in newCodeContent:
        # skip the useless character ' ' & '\n'
        if char == '\n' or char == ' ':
            continue
        # >
        if currentState == DfaState.GT:
            if char == '=':
                # >=
                wordList.append(TypeToken.GE)
                contentList.append(">=")
                currentState = DfaState.Initial
            else:
                # >
                wordList.append(TypeToken.GT)
                contentList.append(">")
                currentState = handleInitialState(char)
        # <
        elif currentState == DfaState.LT:
            if char == '=':
                # <=
                wordList.append(TypeToken.LE)
                contentList.append("<=")
                currentState = DfaState.Initial
            else:
                # <
                wordList.append(TypeToken.LT)
                contentList.append("<")
                currentState = handleInitialState(char)
        # =
        elif currentState == DfaState.Assignment:
            if char == '=':
                # ==
                wordList.append(TypeToken.EQ)
                contentList.append("==")
                currentState = DfaState.Initial
            else:
                # = 
                wordList.append(TypeToken.Assignment)
                contentList.append("=")
                currentState = handleInitialState(char)
        # c
        elif currentState == DfaState.Id_c1:
            if char == 'o':
                # co
                currentState = DfaState.Id_c2
            else:
                # c
                wordList.append(TypeToken.Identifier)
                contentList.append('c')
                currentState = handleInitialState(char)
        # co
        elif currentState == DfaState.Id_c2:
            # cob
            if char == 'b':
                currentState = DfaState.Id_cobegin3
            # coe
            elif char == 'e':
                currentState = DfaState.Id_coend3
            else:
                logging.debug("something unexpected has happened near co")
        # cob
        elif currentState == DfaState.Id_cobegin3:
            # cobe
            if char == 'e':
                currentState = DfaState.Id_cobegin4
            else:
                logging.debug("something unexpected has happened near cob")
        # cobe
        elif currentState == DfaState.Id_cobegin4:
            # cobeg
            if char == 'g':
                currentState = DfaState.Id_cobegin5
            else:
                logging.debug("something unexpected has happened near cobe")
        # cobeg
        elif currentState == DfaState.Id_cobegin5:
            # cobegi
            if char == 'i':
                currentState = DfaState.Id_cobegin6
            else:
                logging.debug("something unexpected has happened near cobeg")
        # cobegi
        elif currentState == DfaState.Id_cobegin6:
            # cobegin
            if char == 'n':
                currentState = DfaState.Id_cobegin7
                wordList.append(TypeToken.Cobegin)
                contentList.append("cobegin")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near cobegi")
        # coe
        elif currentState == DfaState.Id_coend3:
            # coen
            if char == 'n':
                currentState = DfaState.Id_coend4
            else:
                logging.debug("something unexpected has happened near coe")
        # coen
        elif currentState == DfaState.Id_coend4:
            # coend
            if char == 'd':
                currentState = DfaState.Id_cobegin5
                wordList.append(TypeToken.Coend)
                contentList.append("coend")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near coen")
        # i
        elif currentState == DfaState.Id_if1:
            # if
            if char == 'f':
                currentState = DfaState.Id_if2
                wordList.append(TypeToken.If)
                contentList.append("if")
                currentState = DfaState.Initial
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("i")
                currentState = handleInitialState(char)
        # e
        elif currentState == DfaState.Id_e1:
            # el
            if char == 'l':
                currentState = DfaState.Id_else2
            # en
            elif char == 'n':
                currentState = DfaState.Id_end2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("e")
                currentState = handleInitialState(char)
        # el
        elif currentState == DfaState.Id_else2:
            # els
            if char == 's':
                currentState = DfaState.Id_else3
            else:
                logging.debug("something unexpected has happened near el")
        # els
        elif currentState == DfaState.Id_else3:
            # else 
            if char == 'e':
                currentState = DfaState.Id_else4
                wordList.append(TypeToken.Else)
                contentList.append("else")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near els")
        # en
        elif currentState == DfaState.Id_end2:
            # end
            if char == 'd':
                currentState = DfaState.Id_end3
            else:
                logging.debug("something unexpected has happened near en")
        # end
        elif currentState == DfaState.Id_end3:
            # endw
            if char == 'w':
                currentState = DfaState.Id_endwhile4
            # endi
            elif char == 'i':
                currentState = DfaState.Id_endif4
            else:
                logging.debug("something unexpected has happened near end")
        # endw
        elif currentState == DfaState.Id_endwhile4:
            # endwh
            if char == 'h':
                currentState = DfaState.Id_endwhile5
            else:
                logging.debug("something unexpected has happened near endw")
        # endwh
        elif currentState == DfaState.Id_endwhile5:
            # endwhi
            if char == 'i':
                currentState = DfaState.Id_endwhile6
            else:
                logging.debug("something unexpected has happened near endwh")
        # endwhi
        elif currentState == DfaState.Id_endwhile6:
            # endwhil
            if char == 'l':
                currentState = DfaState.Id_endwhile7
            else:
                logging.debug("something unexpected has happened near endwhi")
        # endwhil
        elif currentState == DfaState.Id_endwhile7:
            # endwhile
            if char == 'e':
                currentState = DfaState.Id_endwhile8
                wordList.append(TypeToken.Endwhile)
                contentList.append("endwhile")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near endwhil")
        # endi
        elif currentState == DfaState.Id_endif4:
            # endif
            if char == 'f':
                currentState = DfaState.Id_endif5
                wordList.append(TypeToken.Endif)
                contentList.append("endif")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near endi")
        # a
        elif currentState == DfaState.Id_and1:
            if char == 'n':
                currentState = DfaState.Id_and2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("a")
                currentState = handleInitialState(char)
        # an
        elif currentState == DfaState.Id_and2:
            if char == 'd':
                currentState = DfaState.Id_and3
                wordList.append(TypeToken.And)
                contentList.append("and")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near an")
        # o
        elif currentState == DfaState.Id_or1:
            # or
            if char == 'r':
                currentState = DfaState.Id_or2
                wordList.append(TypeToken.Or)
                contentList.append("or")
                currentState = DfaState.Initial
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("o")
                currentState = handleInitialState(char)
        # n
        elif currentState == DfaState.Id_not1:
            # no
            if char == 'o':
                currentState = DfaState.Id_not2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("n")
                currentState = handleInitialState(char)
        # no
        elif currentState == DfaState.Id_not2:
            # not
            if char == 't':
                currentState = DfaState.Id_not3
                wordList.append(TypeToken.Not)
                contentList.append("not")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near no")
        # s
        elif currentState == DfaState.Id_skip1:
            # sk
            if char == 'k':
                currentState = DfaState.Id_skip2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("s")
                currentState = handleInitialState(char)
        # sk
        elif currentState == DfaState.Id_skip2:
            # ski
            if char == 'i':
                currentState = DfaState.Id_skip3
            else:
                logging.debug("something unexpected has happened near sk")
        # ski
        elif currentState == DfaState.Id_skip3:
            # skip
            if char == 'p':
                currentState = DfaState.Id_skip4
                wordList.append(TypeToken.Skip)
                contentList.append("skip")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near ski")
        # t
        elif currentState == DfaState.Id_t1:
            # tr
            if char == 'r':
                currentState = DfaState.Id_true2
            elif char == 'h':
                currentState = DfaState.Id_then2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("t")
                currentState = handleInitialState(char)
        # tr
        elif currentState == DfaState.Id_true2:
            # tru
            if char == 'u':
                currentState = DfaState.Id_true3
            else:
                logging.debug("something unexpected has happened near tr")
        # tru
        elif currentState == DfaState.Id_true3:
            # true
            if char == 'e':
                currentState = DfaState.Id_true4
                wordList.append(TypeToken.true)
                contentList.append("true")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near tru")
        # th
        elif currentState == DfaState.Id_then2:
            # the
            if char == 'e':
                currentState = DfaState.Id_then3
            else:
                logging.debug("something unexpected has happened near th")
        # the
        elif currentState == DfaState.Id_then3:
            # then
            if char == 'n':
                currentState = DfaState.Id_then4
                wordList.append(TypeToken.Then)
                contentList.append("then")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near the")
        # w
        elif currentState == DfaState.Id_w1:
            # wh
            if char == 'h':
                currentState = DfaState.Id_while2
            elif char == 'a':
                currentState = DfaState.Id_wait2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("w")
                currentState = handleInitialState(char)
        # wh
        elif currentState == DfaState.Id_while2:
            # whi
            if char == 'i':
                currentState = DfaState.Id_while3
            else:
                logging.debug("something unexpected has happened near wh")
        # whi
        elif currentState == DfaState.Id_while3:
            # whil
            if char == 'l':
                currentState = DfaState.Id_while4
            else:
                logging.debug("something unexpected has happened near whi")
        # whil
        elif currentState == DfaState.Id_while4:
            # while
            if char == 'e':
                currentState = DfaState.Id_while5
                wordList.append(TypeToken.While)
                contentList.append("while")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near whil")
        # wa
        elif currentState == DfaState.Id_wait2:
            # wai
            if char == 'i':
                currentState = DfaState.Id_wait3
            else:
                logging.debug("something unexpected has happened near wa")
        # wai
        elif currentState == DfaState.Id_wait3:
            # wait
            if char == 't':
                currentState = DfaState.Id_wait4
                wordList.append(TypeToken.Wait)
                contentList.append("wait")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near wai")
        # d
        elif currentState == DfaState.Id_do1:
            if char == 'o':
                currentState = DfaState.Id_do2
                wordList.append(TypeToken.Do)
                contentList.append("do")
                currentState = DfaState.Initial
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("d")
                currentState = handleInitialState(char)
        # f
        elif currentState == DfaState.Id_false1:
            if char == 'a':
                currentState = DfaState.Id_false2
            else:
                wordList.append(TypeToken.Identifier)
                contentList.append("f")
                currentState = handleInitialState(char)
        # fa
        elif currentState == DfaState.Id_false2:
            if char == 'l':
                currentState = DfaState.Id_false3
            else:
                logging.debug("something unexpected has happened near fa")
        # fal
        elif currentState == DfaState.Id_false3:
            if char == 's':
                currentState = DfaState.Id_false4
            else:
                logging.debug("something unexpected has happened near fal")
        # fals
        elif currentState == DfaState.Id_false4:
            if char == 'e':
                currentState = DfaState.Id_false5
                wordList.append(TypeToken.false)
                contentList.append("false")
                currentState = DfaState.Initial
            else:
                logging.debug("something unexpected has happened near fals")
        elif currentState == DfaState.Initial:
            currentState = handleInitialState(char=char)

    #print(wordList)
    #print(contentList)
    if flag == 1:
        return wordList, contentList

    labelProgram, upToNowCount = mergeToDict(upToNowCount)

    return labelProgram, upToNowCount



def mergeToDict(upToNowCount):
    global inIf, inWhile, countIfToElse, countWhileToEnd

    '''
    get all the variables
    '''
    for i in range(len(wordList)):
        if wordList[i] == TypeToken.Identifier:
            varList.append(contentList[i])
    #### new add code 2019/10/4 #######

    
    labelStr = 'L'
    # key value
    labelCount = upToNowCount
    # print(labelCount)
    labelProgram = []
    length = len(wordList)
    index = 0

    while index < length:
        segment = {}
        # useless key words
        if wordList[index] == TypeToken.Else or wordList[index] == TypeToken.Endif or wordList[index] == TypeToken.Endwhile:
            if wordList[index] == TypeToken.Else:
                segment["type"] = "else"
            elif wordList[index] == TypeToken.Endif:
                segment["type"] = "endif"
            elif wordList[index] == TypeToken.Endwhile:
                segment["type"] = "endwhile"
            labelProgram.append(segment)
            index += 1
            continue
        # assignment sentence
        if wordList[index] == TypeToken.Identifier or wordList[index] == TypeToken.Skip or wordList[index] == TypeToken.Wait:
            # skip ;
            if wordList[index] == TypeToken.Skip:
                segment[frontLabel] = labelStr + str(labelCount)
                segment[backLabel] = labelStr + str(labelCount + 1)
                segment["type"] = "5"
                index += 1;
            # wait( expe ) ;
            elif wordList[index] == TypeToken.Wait:
                segment[frontLabel] = labelStr + str(labelCount)
                segment[backLabel] = labelStr + str(labelCount + 1)
                segment["type"] = "6"
                index += 1
                expression = ""
                while True:
                    expression += contentList[index]
                    index += 1
                    if contentList[index] == ";":
                        break
                segment[conditionExp] = expression
            else:
                # general case
                segment[frontLabel] = labelStr + str(labelCount)
                segment[backLabel] = labelStr + str(labelCount + 1)
                segment[identifier1] = contentList[index]
                segment[identifier2] = contentList[index + 2]
                index += 3
                # eg: a = 1 / a = b
                if wordList[index] == TypeToken.SemiColon:
                    segment["type"] = "1"
                # eg: a = 2 * b / a = b + c
                else:
                    segment[operator] = contentList[index]
                    segment[identifier3] = contentList[index + 1]
                    index += 2
                    segment["type"] = "2"
            # ----------------------------------
            # special case: modify the backLabel
            # ----------------------------------
            if inIf:
                countIfToElse += 1
                if countIfToElse == ifSegment[ifToElseCount]:
                    segment[backLabel] = labelStr + str(labelCount + ifSegment[elseToEndCount] + 1)
                    inIf = False
                    countIfToElse = 0
            if inWhile:
                countWhileToEnd += 1
                if countWhileToEnd == whileSegment[whileToEndCount]:
                    segment[backLabel] = labelStr + str(whileSegment["startCount"])
                    inWhile = False
                    countWhileToEnd = 0
        # if & else part
        elif wordList[index] == TypeToken.If:
            # if occurs in the while part
            if inWhile:
                countWhileToEnd += 1
            getIfPosition(index)
            segment[frontLabel] = labelStr + str(labelCount)
            segment[ifTrueLabel] = labelStr + str(labelCount + 1)
            segment[ifFalseLabel] = labelStr + str(labelCount + ifSegment[ifToElseCount] + 1)
            expression = "("
            index += 1
            while True:
                if wordList[index] == TypeToken.Then:
                    break
                expression += contentList[index]
                index += 1
            expression += ")"
            segment[conditionExp] = expression
            segment["type"] = "3"
        # while & do part
        elif wordList[index] == TypeToken.While:
            getWhilePosition(index, labelCount)
            segment[frontLabel] = labelStr + str(labelCount)
            segment[whileTrueLabel] = labelStr + str(labelCount + 1)
            segment[whileFalseLabel] = labelStr + str(labelCount + whileSegment[whileToEndCount] + 1)
            expression = "("
            index += 1
            while True:
                if wordList[index] == TypeToken.Do:
                    break
                expression += contentList[index]
                index += 1
            expression += ")"
            segment[conditionExp] = expression
            segment["type"] = "4"

        labelProgram.append(segment)
        labelCount += 1
        index += 1
    
    
    # outputKripkeStructure(labelProgram)
    return labelProgram, labelCount
    


def outputKripkeStructure(labelProgram):
    # print(labelProgram)
    print("*********************Label Program***************************")
    for currentPart in labelProgram:
        if currentPart["type"] == "1":   
            print('%s: %s = %s' % (currentPart[frontLabel], currentPart[identifier1], currentPart[identifier2]))
        elif currentPart["type"] == "2":
            print('%s: %s = %s %s %s' % (currentPart[frontLabel], currentPart[identifier1], currentPart[identifier2], currentPart[operator], currentPart[identifier3]))
        elif currentPart["type"] == "3":
            print('%s: if %s then' % (currentPart[frontLabel], currentPart[conditionExp]))
        elif currentPart["type"] == "4":
            print('%s: while %s do' % (currentPart[frontLabel], currentPart[conditionExp]))  
        elif currentPart["type"] == "5":
            print('%s: skip' % (currentPart[frontLabel]))
        elif currentPart["type"] == "6":
            print('%s: wait %s' % (currentPart[frontLabel], currentPart[conditionExp])) 
        else:
            print(currentPart["type"])

    print("*********************Label Formula***************************")
    for currentPart in labelProgram:
        if currentPart["type"] == "1":   
            print("pc = %s ^ pc' = %s ^ %s' = %s" % (currentPart[frontLabel], currentPart[backLabel], currentPart[identifier1], currentPart[identifier2]))
        elif currentPart["type"] == "2":
            print("pc = %s ^ pc' = %s ^ %s' = %s %s %s" % (currentPart[frontLabel], currentPart[backLabel], currentPart[identifier1], currentPart[identifier2], currentPart[operator], currentPart[identifier3]))
        elif currentPart["type"] == "3":
            print("pc = %s ^ pc' = %s ^ %s" % (currentPart[frontLabel], currentPart[ifTrueLabel], currentPart[conditionExp]))
            print("pc = %s ^ pc' = %s ^ ¬%s" % (currentPart[frontLabel], currentPart[ifFalseLabel], currentPart[conditionExp]))
        elif currentPart["type"] == "4":
            print("pc = %s ^ pc' = %s ^ %s" % (currentPart[frontLabel], currentPart[whileTrueLabel], currentPart[conditionExp])) 
            print("pc = %s ^ pc' = %s ^ ¬%s" % (currentPart[frontLabel], currentPart[whileFalseLabel], currentPart[conditionExp]))  
        elif currentPart["type"] == "5":
            print("pc = %s ^ pc' = %s ^ Same(U)" % (currentPart[frontLabel], currentPart[backLabel]))
        elif currentPart["type"] == "6":
            print("pc = %s ^ pc' = %s ^ %s" % (currentPart[frontLabel], currentPart[backLabel], currentPart[conditionExp]))
            print("pc = %s ^ pc' = %s ^ ¬%s" % (currentPart[frontLabel], currentPart[frontLabel], currentPart[conditionExp]))
        else:
            pass





