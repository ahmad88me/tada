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
        self.depth = -1

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
        for n in self.cache:
            node = self.index[n]
            if node.parents == [] and len(node.childs) > 0:
                self.roots.append(node)
        self.roots = list(set(self.roots))

    def remove_lonely_nodes(self):
        removed_titles = []
        for n in self.cache:
            node = self.index[n]
            if node.parents == node.childs == []:
                del self.index[n]
                self.cache.remove(n)
                removed_titles.append(n)
        return removed_titles

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

    def draw(self, file_name='graph.gv'):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')
        for n in self.cache:
            dot.node(clean(n))
        print "draw nodes"
        for n in self.cache:
            node = self.index[n]
            for ch in node.childs:
                dot.edge(clean(n), clean(ch.title))
        dot.render(file_name, view=True)

    # def draw_with_scores(self, multi=False):
    #     if not multi:
    #         print "not multi"
    #         from graphviz import Digraph
    #         dot = Digraph(comment='The Round Table')
    #         for n in self.cache:
    #             node = self.find_v(n)
    #             dot.node(clean_with_score(node))
    #
    #         for n in self.cache:
    #             node = self.index[n]
    #             for ch in node.childs:
    #                 dot.edge(clean_with_score(node), clean_with_score(ch))
    #
    #         dot.render('graph.gv', view=True)
    #     else:
    #         print "multi"
    #         self.draw_with_score_separate()
    #
    # def draw_with_score_separate(self):
    #     for idx, r in enumerate(self.roots):
    #         self.draw_score_for_root(r, "%d_graph.gv"%idx)
    #     # self.draw_score_for_root(self.roots[0], "1_graph.gv")

    def draw_score_for_root(self, root, file_name):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')
        nodes = self.get_all_child_nodes(root, [])
        if len(nodes) <= 3:
            return
        for n in nodes:
            dot.node(clean_with_score(n))

        for n in nodes:
            for ch in n.childs:
                dot.edge(clean_with_score(n), clean_with_score(ch))

        dot.render(file_name, view=True)

    def get_all_child_nodes(self, node, visited):
        """
        called by draw_score_for_root
        :param node:
        :param visited:
        :return:
        """
        if node in visited:
            print "cycle node: %s" % node.title
            return visited
        visited_local = visited[:] + [node]

        for ch in node.childs:
            visited_local = self.get_all_child_nodes(ch, visited_local)
        return visited_local

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


# def clean_with_score(n):
#     return "%s cove(%g) num(%d) depth(%d) pspec(%f) score(%f)" % (
#         clean(n.title), n.coverage_score, n.num_of_subjects, n.depth, n.path_specificity, n.score)


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
