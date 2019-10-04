#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019.9.30
# @Author  : 傅剑铃
# @FileName: state.py


from enum import Enum, unique

@unique
class TypeToken(Enum):
    Plus = 1 
    Minus = 2 
    Star = 3
    GE = 4  # >=
    GT = 5  # >
    EQ = 6  # ==
    LE = 7  # <=
    LT = 8  # <
    # ;
    SemiColon = 9
    # ()
    LeftParen = 10
    RightParen = 11
    Assignment = 12
    If = 14
    Else = 15
    # C: && || !
    And = 16
    Or = 17
    Not = 25
    Skip = 18
    Wait = 19
    Then = 20
    While = 21
    Do = 22
    # avoid key word by using lowercase
    true = 23
    false = 24
    # cobegin & coend
    Cobegin = 26
    Coend = 27
    # a~z
    Identifier = 28
    # 0,1,2
    IntLiteral = 29
    # sth forget
    Endwhile = 30
    Endif = 31

@unique
class DfaState(Enum):
    Initial = 1
    If = 2
    Id_if1 = 3
    Id_if2 = 4
    And = 10
    Id_and1 = 11
    Id_and2 = 12
    Id_and3 = 13
    Or = 14
    Id_or1 = 15
    Id_or2 =  16
    Skip = 17
    Id_skip1 = 18
    Id_skip2 = 19
    Id_skip3 = 20
    Id_skip4 = 21
    # then & true share the first 't'
    Id_t1 = 22
    Id_then2 = 23
    Id_then3 = 24
    Id_then4 = 25
    Then = 26
    Id_true2 = 27
    Id_true3 = 28
    Id_true4 = 29
    true = 30
    # while & wait share the first 'w'
    Id_w1 = 31
    Id_while2 = 32
    Id_while3 = 33
    Id_while4 = 34
    Id_while5 = 35
    While = 36
    Id_wait2 = 37
    Id_wait3 = 38
    Id_wait4 = 39
    Wait = 40
    Do = 41
    Id_do1 = 42
    Id_do2 = 43
    false = 44
    Id_false1 = 45
    Id_false2 = 46
    Id_false3 = 47
    Id_false4 = 48
    Id_false5 = 49
    Not = 50
    Id_not1 = 51
    Id_not2 = 52
    Id_not3 = 53
    Identifier = 54
    Id_identifier1 = 55
    GT = 56 
    GE = 57
    LT = 58
    LE = 59
    # = & == share the first '='
    Assignment = 60
    EQ = 61
    Plus = 62
    Minus = 63
    Star = 64
    # cobegin & coend share the 'co'
    Id_c1 = 65
    Id_c2 = 66
    Id_cobegin3 = 67
    Id_cobegin4 = 68
    Id_cobegin5 = 69
    Id_cobegin6 = 70
    Id_cobegin7 = 71
    Cobegin = 72
    Id_coend3 = 73
    Id_coend4 = 74
    Id_coend5 = 75
    Coend = 76
    SemiColon = 77
    LeftParen = 78
    RightParen = 79
    IntLiteral = 80
    # else & endwhile share the first 'e'
    Id_e1 = 81
    Id_else2 = 82
    Id_else3 = 83
    Id_else4 = 84
    Else = 85
    Id_end2 = 86
    Id_end3 = 87
    Id_endwhile4 = 88
    Id_endwhile5 = 89
    Id_endwhile6 = 90
    Id_endwhile7 = 91
    Id_endwhile8 = 92
    Endwhile = 93
    Id_endif4 = 94
    Id_endif5 = 95
    Endif = 96
