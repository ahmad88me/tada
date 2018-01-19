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

    def draw_with_scores(self):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')
        for n in self.cache:
            # dot.node(clean(n), clean(n))
            node = self.find_v(n)
            # dot.node(clean(node.title) + " - " + node.score, clean(node.title) + " - " + node.score)
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

    def set_converage_score(self):
        for n in self.roots:
            print 'set coverage root: %s' % n.title
            self.compute_coverage_score_for_node(n)
            # n = self.roots[0]
            # print 'set coverage root: %s' % n.title
            # self.compute_coverage_score_for_node(n)

    def compute_coverage_score_for_node(self, node):
        # s = node.coverage_score
        print 'enter in %s' % node.title
        if node._coverage_computed:
            return node.coverage_score
        for child in node.childs:
            # node.coverage_score += self.compute_coverage_score_for_node(child)
            # s += self.compute_coverage_score_for_node(child)
            node.coverage_score += self.compute_coverage_score_for_node(child)
        if len(node.childs) == 0:
            print 'leave score of %s: %g' % (node.title, node.coverage_score)
        else:
            print 'mid score of %s: %g' % (node.title, node.coverage_score)
        print 'leaving %s' % node.title
        node._coverage_computed = True
        return node.coverage_score

    # see iteration 6 and 7
    # def set_nodes_subjects_counts(self, d):
    #     for n in self.roots:
    #         self.set_subjects_count_for_node(n, d)
    #
    # def set_subjects_count_for_node(self, node, d):
    #     if node.num_of_subjects != -1:  # it is already set
    #         return
    #     for child in node.childs:
    #         self.set_subjects_count_for_node(child, d)
    #     if node.title in d:
    #         node.num_of_subjects = float(d[node.title])
    #     else:
    #         node.num_of_subjects = 0.0

    def set_nodes_subjects_counts(self, d, leaves):
        for leaf in leaves:
            if leaf.title not in d:
                leaf.num_of_subjects = 0
                raise Exception("just for reporting and it is not an error")
            else:
                leaf.num_of_subjects = d[leaf.title]

        for n in self.roots:
            self.set_subjects_count_for_node(n, d)

    def set_subjects_count_for_node(self, node, d):
        if node.num_of_subjects != -1:  # it is already set
            return
        else:
            node.num_of_subjects = 0
            for child in node.childs:
                self.set_subjects_count_for_node(child, d)
                print "node: %s has num of subjects %s and child %s has num of subjects %s" % (
                node.title, str(node.num_of_subjects), child.title, str(child.num_of_subjects))
                print "node: %s and child %s " % (type(node.num_of_subjects), type(child.num_of_subjects))
                node.num_of_subjects += child.num_of_subjects

    # def set_specificity_score(self):
    #     for n in self.roots:
    #         self.compute_specificity_for_node(n)
    #
    # def compute_specificity_for_node(self, node):
    #     if node.specificity_score != -1:  # if specificity score is computed then do not continue
    #         return
    #     if node.parents == []:
    #         node.specificity_score = 1
    #     else:
    #         parents_num_subjects = []
    #         for parent in node.parents:
    #             if parent.num_of_subjects > 0:
    #                 parents_num_subjects.append(parent.num_of_subjects)
    #         if len(parents_num_subjects) == 0:
    #             node.specificity_score = 1
    #         else:
    #             node.specificity_score = node.num_of_subjects * 1.0 / sum(parents_num_subjects) * 1.0 / len(parents_num_subjects)
    #
    #     for child in node.childs:
    #         self.compute_specificity_for_node(child)

    # def set_specificity_score(self):
    #     for n in self.roots:
    #         self.compute_specificity_for_node(n)
    #
    # def compute_specificity_for_node(self, node):
    #     if node.specificity_score != -1:  # if specificity score is computed then do not continue
    #         return
    #     if node.parents != []:  # not a root
    #         node.specificity_score = node.num_of_subjects * 1.0 / node.parents[0].num_of_subjects
    #     else:
    #         node.specificity_score = 1
    #     for child in node.childs:
    #         self.compute_specificity_for_node(child)

    # def set_specificity_score(self):
    #     leaves = self.get_leaves_from_graph()
    #     for leaf in leaves:
    #         self.compute_specifity_upwards(leaf)
    #
    # def compute_specifity_upwards(self, node):
    #     if node.parents == []:
    #         node.specificity_score = 1
    #         return
    #     parents_num_subjects = []
    #     for parent in node.parents:
    #         if parent.num_of_subjects > 0:
    #             parents_num_subjects.append(parent.num_of_subjects)
    #     node.specificity_score = node.num_of_subjects*1.0 / sum(parents_num_subjects)*1.0/len(parents_num_subjects)

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
    return "%s coverage(%g) num(%d) specificity(%g)" % (
        clean(n.title), n.coverage_score, n.num_of_subjects, n.specificity_score)


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
