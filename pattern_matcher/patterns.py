class Node(object):
    """The object representation of a pattern node."""
    WILDCARD = '*'

    def __init__(self, value):
        self.value = value

    def is_wildcard(self):
        """True if the Node's value matches the wildcard."""
        return self.value == self.WILDCARD

    def __str__(self):
        return self.value

    def __repr__(self):
        return '<Node: \'{0}\'>'.format(str(self))


class Pattern(object):
    """The object representation of a pattern.

    Most importantly, this objects calculates and stores the number of
    wildcards contained in the pattern, and scores the wildcards based
    on the position in the pattern.

    When comparing Patterns, the first comparison is based on the number
    of wildcards.  The Pattern with the fewer number of wildcards will always
    win.  In the case of a tie, the score is used to break it.  A Pattern that
    has more rightmost wildcards will always have a lower score.
    """
    def __init__(self, nodes):
        # Score of the pattern based on the index of it's wildcards.
        self.score = 0
        self.num_wildcards = 0
        self.nodes = [Node(node) for node in nodes]
        self.length = len(self.nodes)
        self.__calculate()

    def __calculate(self):
        """Calculate the number of wildcards score for the Pattern."""
        for index, node in enumerate(self.nodes):
            if node.is_wildcard():
                self.num_wildcards += 1

                # Scoring the pattern in this manner means that the pattern with
                # the most rightmost wildcards will always have a lower score.
                self.score += self.length / float(index + 1 + self.length)

    def has_wildcard(self):
        """True if the Pattern has at least one wildcard."""
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
        self.__configure(patterns)

    def __configure(self, patterns):
        for pattern in patterns:
            # Create a new Pattern instance and add it to self.
            p = Pattern(pattern)
            self.patterns.append(p)

            # If there is not yet a min_wildcard value, or if the current Pattern
            # has a lower number of wildcards than the current min, then we
            # want to set min_wildcards to the lower value.
            if not self.has_min_wildcards() or p.num_wildcards < self.min_wildcards:
                self.min_wildcards = p.num_wildcards

            # If there is not yet a min_score value, or if the current Pattern
            # has a lower number score than the current min, then we
            # want to set min_score to the lower value.
            if not self.has_min_score() or p.score < self.min_score:
                self.min_score = p.score

    def has_min_score(self):
        """True if min_score is not None."""
        return self.min_score is not None

    def has_min_wildcards(self):
        """True if min_wilcards is not None."""
        return self.min_wildcards is not None

    def get_best_patterns(self):
        # Filter the patterns to get only the Pattern objects that have the
        # least number of wildcards.
        patterns = [p for p in self.patterns if p.num_wildcards == self.min_wildcards]

        # If multiple Pattern objects are returned, then we need to rate the
        # matches by score and return those patterns.
        if len(patterns) != 1:
            return [p for p in patterns if p.score == self.min_score]

        return patterns
