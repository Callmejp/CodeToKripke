# from graphviz import Digraph

# dot = Digraph(name="MyPicture", comment="the test", format="png")

# dot.node(name='a', label='Ming', color='green')
# dot.node(name='b', label='Hong', color='yellow')
# dot.node(name='c', label='Dong')

# dot.edge('a', 'b', label="ab\na-b", color='red')
# dot.edges(['cb', 'ac', 'aa'])




# # dot.view(filename="mypicture", directory="D:\MyTest")

# dot.render(filename='MyPicture', directory="D:\MyTest",view=True)

# "b >= 2"
# d = {"b": 2}
n1 = {"a": 0, "b": 0, "d": 0, "pc0": "L1", "pc1": "L8", "node": 1}

n2 = {"a": 0, "b": 0, "d": 0, "pc0": "L1", "pc1": "L8", "node": 2}

n1.pop("node")
n2.pop("node")

if n1 == n2:
    print('ds')