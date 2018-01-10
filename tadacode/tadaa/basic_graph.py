class Node:

    def __init__(self):
        self.__init__('default')

    def __init__(self, title):
        self.title = title
        self.parents = []
        self.childs = []

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return self.title


class BasicGraph:

    def __init__(self):
        self.roots = []
        self.cache = []  # this is used to check whether an item is in the graph or not

    def add_v(self, title, parents):
        if title in self.cache:
            node = self.find_v(title)
            print "%s already in the graph" % node.title
        else:
            node = Node(title=title)
            print "%s new to the graph" % node.title
        self.cache.append(title)
        if parents == [] and node not in self.roots:
            self.roots.append(node)
        else:
            parents = [self.find_v(p) for p in parents]
            node.parents += parents
            node.parents = list(set(node.parents))
            for pnode in parents:
                pnode.childs.append(node)
                pnode.childs = list(set(pnode.childs))
        return node

    def find_v(self, title):
        for node in self.roots:
            target_node = self.find_v_node(title=title, node=node)
            if target_node:
                return target_node
        print "%s is not found" % title
        return None

    def find_v_node(self, title, node):
        if title == node.title:
            return node
        for n in node.childs:
            target_node = self.find_v_node(title, n)
            if target_node:
                return target_node
        return None

    def draw(self):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')
        for n in self.cache:
            dot.node(clean(n), clean(n))
        edges = {}
        for n in self.roots:
            if n not in edges:
                edges[n.title] = []
        for n in self.roots:
            edges = self.connect_node(node=n, edges=edges)
        for n in edges.keys():
            for v in edges[n]:
                dot.edge(clean(n), clean(v))
        dot.render('graph.gv', view=True)

    def connect_node(self, node, edges):
        for child in node.childs:
            if node.title not in edges:
                edges[node.title] = []
            if child.title not in edges[node.title]:
                edges[node.title].append(child.title)
            edges = self.connect_node(child, edges)
        return edges


def clean(s):
    return s.replace("http://", "")

if __name__ == '__main__':
    g = BasicGraph()
    n = g.add_v(title="grand", parents=[])
    n2 = g.add_v(title="grand Mother", parents=[])
    g.add_v(title="pA", parents=[n.title, n2.title])
    g.add_v(title="pB", parents=[n.title])
    g.add_v(title="C1", parents=["pA"])
    g.draw()
