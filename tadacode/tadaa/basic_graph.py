class Node:
    def __init__(self):
        self.__init__('default')

    def __init__(self, title):
        self.title = title
        self.parents = []
        self.childs = []
        self.coverage_score = 0
        self.specificity_score = -1
        self._coverage_computed = False
        self.num_of_subjects = -1
        self.path_specificity = -1
        self.score = -1

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
        self.index = {}

    def add_v(self, title, parents):
        """
        :param title:
        :param parents: a list of parents
        :return:
        """
        if title in self.cache:
            print "%s already in the graph" % title
            return

        node = Node(title=title)
        print "%s new to the graph" % node.title
        self.index[title] = node  # title should not be previously in the index
        self.cache.append(title)
        if parents is None:
            pass
        elif parents == [] and node not in self.roots:
            self.roots.append(node)
        else:
            parents = [self.find_v(p) for p in parents]
            node.parents += parents
            node.parents = list(set(node.parents))
            for pnode in parents:
                pnode.childs.append(node)
                pnode.childs = list(set(pnode.childs))

    def add_e(self, from_title, to_title):
        parent_node = self.index[from_title]
        child_node = self.index[to_title]
        if child_node not in parent_node.childs:
            parent_node.childs.append(child_node)
        if parent_node not in child_node.parents:
            child_node.parents.append(parent_node)

    def remove_edge(self, from_node, to_node):
        from_node.childs.remove(to_node)
        to_node.parents.remove(from_node)

    def build_roots(self):
        for n in self.index:
            node = self.index[n]
            if node.parents == []:
                self.roots.append(node)
        self.roots = list(set(self.roots))

    def break_cycles(self):
        for r in self.roots:
            self.dfs_break_cycle([r])

    def dfs_break_cycle(self, visited):
        node = visited[-1]
        for ch in node.childs:
            if ch in visited:  # there is a cycle
                self.remove_edge(node, ch)
            else:
                self.dfs_break_cycle(visited=visited+[ch])

    def find_v(self, title):
        if title in self.index:
            return self.index[title]
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

    def draw_with_scores(self):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')
        for n in self.cache:
            node = self.find_v(n)
            dot.node(clean_with_score(node), clean_with_score(node))

        edges = {}
        for n in self.roots:
            if n not in edges:
                edges[n.title] = []
        for n in self.roots:
            edges = self.connect_node(node=n, edges=edges)
        for n in edges.keys():
            for v in edges[n]:
                dot.edge(clean_with_score(self.find_v(n)), clean_with_score(self.find_v(v)))
        dot.render('graph.gv', view=True)

    def connect_node(self, node, edges):
        for child in node.childs:
            if node.title not in edges:
                edges[node.title] = []
            if child.title not in edges[node.title]:
                edges[node.title].append(child.title)
            edges = self.connect_node(child, edges)
        return edges

    def get_scores(self):
        nodes = []
        for n in self.roots:
            nodes += self.get_score_for_node(n)
        nodes = list(set(nodes))
        return sorted(nodes, key=lambda node: node.score, reverse=True)

    def get_score_for_node(self, node):
        nodes = [node]
        for child in node.childs:
            nodes += self.get_score_for_node(child)
        return nodes

    def set_score_for_graph(self, coverage_weight=0.5):
        for n in self.roots:
            self.set_score_for_node(n, coverage_weight)

    def set_score_for_node(self, node, coverage_weight):
        if node.score != -1:
            return
        node.score = node.coverage_score * coverage_weight + (1-coverage_weight) * -node.path_specificity
        for child in node.childs:
            self.set_score_for_node(child, coverage_weight)

    def set_converage_score(self):
        for n in self.roots:
            print 'set coverage root: %s' % n.title
            self.compute_coverage_score_for_node(n)

    def compute_coverage_score_for_node(self, node):
        # s = node.coverage_score
        print 'enter in %s' % node.title
        if node._coverage_computed:
            return node.coverage_score
        for child in node.childs:
            node.coverage_score += self.compute_coverage_score_for_node(child)
        if len(node.childs) == 0:
            print 'leave score of %s: %g' % (node.title, node.coverage_score)
        else:
            print 'mid score of %s: %g' % (node.title, node.coverage_score)
        print 'leaving %s' % node.title
        node._coverage_computed = True
        return node.coverage_score

    def set_path_specificity(self):
        for n in self.get_leaves_from_graph():
            self.set_path_specificity_for_node(n)

    def set_path_specificity_for_node(self, node):  # solve bug #2
        if node.path_specificity == -1:
            if node.parents == []:
                node.path_specificity = 1
            else:
                node.path_specificity = min([self.set_path_specificity_for_node(p) for p in node.parents]) * node.specificity_score
        return node.path_specificity

    # iteration 8
    def set_nodes_subjects_counts(self, d):
        for n in self.roots:
            self.set_subjects_count_for_node(n, d)

    def set_subjects_count_for_node(self, node, d):
        if node.num_of_subjects != -1:  # it is already set
            return
        for child in node.childs:
            self.set_subjects_count_for_node(child, d)
        if node.title in d:
            node.num_of_subjects = int(d[node.title])
        else:
            node.num_of_subjects = 0
            raise Exception("in iteration 8 this should not happen as we are checking the childs as well")

    def set_specificity_score(self):
        for n in self.roots:
            self.compute_specificity_for_node(n)

    def compute_specificity_for_node(self, node):
        if node.specificity_score != -1:  # if specificity score is computed
            return

        if node.parents == []:
            node.specificity_score = 1
        else:
            node.specificity_score = node.num_of_subjects * 1.0 / max([p.num_of_subjects for p in node.parents])

        for child in node.childs:
            self.compute_specificity_for_node(child)

    def get_leaves_from_graph(self):
        leaves = []
        for n in self.roots:
            leaves += self.get_leaves_of_node(n)
        return list(set(leaves))

    def get_leaves_of_node(self, node):
        if node.childs == []:
            return [node]
        leaves = []
        for child in node.childs:
            leaves += self.get_leaves_of_node(child)
        return leaves


def clean_with_score(n):
    return "%s cove(%g) num(%d) spec(%g) pspec(%f) score(%f)" % (
        clean(n.title), n.coverage_score, n.num_of_subjects, n.specificity_score, n.path_specificity, n.score)


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
