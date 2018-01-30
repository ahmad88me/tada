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

    def add_v(self, title, parents):
        if title in self.cache:
            # node = self.find_v(title)
            # print "%s already in the graph" % node.title
            print "%s already in the graph" % title
            return
        else:
            node = Node(title=title)
            print "%s new to the graph" % node.title
        self.cache.append(title)
        if parents == [] and node not in self.roots:
            # if node.title == 'http://www.w3.org/2002/07/owl#Thing':  # forcing thing root just to test the overall algo.
            #     self.roots.append(node)
            self.roots.append(node)
        else:
            parents = [self.find_v(p) for p in parents]
            # # just temp
            # parents = [p for p in parents if p is not None]
            node.parents += parents
            node.parents = list(set(node.parents))
            for pnode in parents:
                pnode.childs.append(node)
                pnode.childs = list(set(pnode.childs))
        # return node

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

    def set_path_specificity(self):
        # for n in self.roots:
        #     n.path_specificity = 1

        # for n in self.roots:
        #     self.set_path_specificity_for_node(n)
        for n in self.get_leaves_from_graph():
            self.set_path_specificity_for_node(n)

    # def set_path_specificity_for_node(self, node):
    #     #print 'pspec node: %s' % node.title
    #     if node.path_specificity != -1 and node.parents != []:
    #         return
    #     if node.parents == []:
    #         #print 'pspec node %s is parent' % node.title
    #         node.path_specificity = 1
    #     else:
    #         #print 'pspec node %s is not parent with specscore: %g' % (node.title, node.specificity_score)
    #         node.path_specificity = min([p.path_specificity for p in node.parents]) * node.specificity_score
    #
    #     for child in node.childs:
    #         self.set_path_specificity_for_node(child)

    def set_path_specificity_for_node(self, node):  # solve the bug #2
        if node.path_specificity == -1:
            if node.parents == []:
                node.path_specificity = 1
            else:
                node.path_specificity = min([self.set_path_specificity_for_node(p) for p in node.parents]) * node.specificity_score
        return node.path_specificity

        #
        #
        # if node.path_specificity != -1 and node.parents != []: # node path specificity is computed and it is not a root
        #     return node.path_specificity
        # if node.parents == []:  # root node
        #     node.path_specificity = 1
        # else:
        #     node.path_specificity = min([self.set_path_specificity_for_node(p) for p in node.parents]) * node.specificity_score
        # # compute path specificity for its children
        # for child in node.childs:
        #     self.set_path_specificity_for_node(child)
        # return node.path_specificity

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

    # see iteration 8
    # def set_nodes_subjects_counts(self, d, leaves):
    #     for leaf in leaves:
    #         if leaf.title not in d:
    #             leaf.num_of_subjects = 0
    #             raise Exception("just for reporting and it is not an error")
    #         else:
    #             leaf.num_of_subjects = d[leaf.title]
    #
    #     for n in self.roots:
    #         self.set_subjects_count_for_node(n, d)
    #
    # def set_subjects_count_for_node(self, node, d):
    #     if node.num_of_subjects != -1:  # it is already set
    #         return
    #     else:
    #         node.num_of_subjects = 0
    #         for child in node.childs:
    #             self.set_subjects_count_for_node(child, d)
    #             print "node: %s has num of subjects %s and child %s has num of subjects %s" % (
    #             node.title, str(node.num_of_subjects), child.title, str(child.num_of_subjects))
    #             print "node: %s and child %s " % (type(node.num_of_subjects), type(child.num_of_subjects))
    #             node.num_of_subjects += child.num_of_subjects

    def set_specificity_score(self):
        for n in self.roots:
            self.compute_specificity_for_node(n)

    def compute_specificity_for_node(self, node):
        if node.specificity_score != -1:  # if specificity score is computed
            return

        if node.parents == []:
            node.specificity_score = 1
        else:
            # see iteration 9
            # parents_num_subjects = []
            # for parent in node.parents:
            #     if parent.num_of_subjects > 0:
            #         parents_num_subjects.append(parent.num_of_subjects)
            #     else:
            #         raise Exception("num of subjects should not be zero as in iteration 8 for each type we also count the sub types")
            # if len(parents_num_subjects) == 0:  # will not be reached do to the previous exception but I'm keeping it just in case that sub types are counted due to a future change. But as for now, this should not be reached
            #     node.specificity_score = 1
            #     raise Exception("parent num of subject is zero, which should not happen")
            # else:
            #     node.specificity_score = node.num_of_subjects * 1.0 / sum(parents_num_subjects) * 1.0 / len(parents_num_subjects)
            node.specificity_score = node.num_of_subjects * 1.0 / max([p.num_of_subjects for p in node.parents])

        for child in node.childs:
            self.compute_specificity_for_node(child)

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
