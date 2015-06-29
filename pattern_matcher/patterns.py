class Node(object):
    WILDCARD = '*'

    def __init__(self, value):
        self.value = value

    def is_wildcard(self):
        return self.value == self.WILDCARD

    def __str__(self):
        return self.value

    def __repr__(self):
        return '<Node: \'{0}\'>'.format(str(self))


class Pattern(object):
    def __init__(self, nodes):
        self.score = 0
        self.num_wildcards = 0
        self.nodes = [Node(node) for node in nodes]
        self.length = len(self.nodes)
        self.__score_pattern()

    def __score_pattern(self):
        for index, node in enumerate(self.nodes):
            if node.is_wildcard():
                self.num_wildcards += 1
                self.score += self.length / float(index + 2)

    def has_wildcard(self):
        return self.num_wildcards > 0

    def __str__(self):
        return ','.join([str(node) for node in self.nodes])

    def __repr__(self):
        return '<Pattern: \'{0}\'>'.format(str(self))


class Patterns(object):
    def __init__(self, patterns):
        self.min_wildcards = None
        self.min_score = None
        self.patterns = []
        self.__add_patterns(patterns)

    def __add_patterns(self, patterns):
        for pattern in patterns:
            p = Pattern(pattern)
            self.patterns.append(p)
            self._update_min_wildcards(p)
            self._update_min_score(p)

    def _update_min_wildcards(self, p):
        if self.min_wildcards is None or p.num_wildcards < self.min_wildcards:
            self.min_wildcards = p.num_wildcards

    def _update_min_score(self, p):
        if self.min_score is None or p.score < self.min_score:
            self.min_score = p.score

    def get_best_patterns(self):
        patterns = [p for p in self.patterns if p.num_wildcards == self.min_wildcards]

        if len(patterns) > 1:
            return [p for p in patterns if p.score == self.min_score]

        return patterns.pop()
