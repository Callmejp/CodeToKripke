# Translate the concurrent program to the Kripke Structure
![Build Status](https://travis-ci.com/Callmejp/CodeToKripke.svg?branch=master)
## version 1.0.0

In the first version, we only consider the single program without concurrence. And `If` and `While` won't be nested inside each other.

### IMP language

1. Aexp: a=n|X|a+a|a-a|a*a, n$\in$[0, 2]
2. Bexp: b=true|false|a=a|a<=a|not b|b and b|b or b
3. Com: c=|X=a|a;b|if b then c else c|while b do c

### Specification

Here `a`, `b` and `c` indicates the variables, expressions and sentences.

### Result

```
//Input: imp.txt
```

```
//Output:
*********************Label Program***************************
L1: a = 1
L2: b = a
L3: if (a<=b) then
L4: c = a + b
else
L5: d = c - b
endif
L6: while (true) do
L8: f = 0
L10: g = f + e
else
L11: h = g * 2
*********************Label Formula***************************
pc = L1 ^ pc' = L2 ^ a' = 1
pc = L2 ^ pc' = L3 ^ b' = a
pc = L3 ^ pc' = L4 ^ (a<=b)
pc = L3 ^ pc' = L5 ^ ¬(a<=b)
pc = L4 ^ pc' = L6 ^ c' = a + b
pc = L5 ^ pc' = L6 ^ d' = c - b
pc = L6 ^ pc' = L7 ^ (true)
pc = L6 ^ pc' = L9 ^ ¬(true)
pc = L9 ^ pc' = L10 ^ (notf)
pc = L9 ^ pc' = L11 ^ ¬(notf)
pc = L10 ^ pc' = L12 ^ g' = f + e
pc = L11 ^ pc' = L12 ^ h' = g * 2
```

## Thanks the course in the [极客时间](https://time.geekbang.org/column/intro/100034101)