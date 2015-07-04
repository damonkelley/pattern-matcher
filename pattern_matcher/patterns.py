class Node(object):
    """A single node from a pattern.

    Here, a node is defined as one character or group characters that
    is a member of a comma seperated pattern. For example, given the
    pattern,

        foo,*,bar

    `foo` would be the first node of the pattern.
    """
    WILDCARD = '*'

    def __init__(self, value):
        """Initialze a Node instance.

        Parameters:
            value: the string form of the node.
        """
        self.value = value

    def is_wildcard(self):
        """True if the Node's value matches the wildcard."""
        return self.value == self.WILDCARD

    def __str__(self):
        return self.value

    def __repr__(self):
        return '<Node: \'{0}\'>'.format(str(self))


class Pattern(object):
    """A single pattern.

    A pattern is a comma separated list of nodes. The string
    representation of a pattern is:

        foo,*,bar

    Most importantly, this object calculates and stores the number of
    wildcards contained in the pattern, and scores the wildcards based
    on the position in the pattern.
    """

    def __init__(self, nodes):
        """Initialize a Pattern instance.

        Parameters:
            nodes: an iterable where each element is a string
                   representation of a node.
        """
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


class MultipleMatchesError(Exception):
    pass


class Patterns(object):
    """A collection of patterns.

    This object is knowledgable about its member Pattern objects, and will get
    the best matching Pattern via the `get_best_pattern` method.

    In order to find the best matching Pattern, the first step is to idenfify
    Pattern object(s) that have the lowest number of wildcards.  The Pattern
    with the fewer number of wildcards will always win.  In the case of a
    tie, the score is used to break it.  A Pattern that has more rightmost
    wildcards will always have a lower score.
    """

    def __init__(self, patterns):
        """Initialize a Patterns instance.

        Parameters:
            patterns: a list/tuple of pattern tuples.
                        [('foo', 'bar'), ('*', 'bar')]
        """
        self.min_wildcards = None
        self.min_score = None
        self.patterns = []
        self.__configure(patterns)

    def __configure(self, patterns):
        """Add the patterns to the instance and calculate the lowest
        number of wildcards and the lowest score from the list of member
        Pattern objects.
        """
        for pattern in patterns:
            p = Pattern(pattern)
            self.patterns.append(p)

            # Determine the lowest number of wildcards.
            if not self.has_min_wildcards() or p.num_wildcards < self.min_wildcards:
                self.min_wildcards = p.num_wildcards

            # Determine the lowest Pattern score.
            if not self.has_min_score() or p.score < self.min_score:
                self.min_score = p.score

    def has_min_score(self):
        """True if min_score is not None."""
        return self.min_score is not None

    def has_min_wildcards(self):
        """True if min_wilcards is not None."""
        return self.min_wildcards is not None

    def get_best_pattern(self):
        """Get the best pattern based on the number of wildcards and score.

        Returns the best member Pattern instance or None

        The best pattern is the Pattern object that has the lowest number
        of wildcards.  If multiple Patterns share the lowest number of
        wildcards, then the tie is broken based on the lowest score.
        """
        # Filter out patterns that do not have the lowest number of wildcards.
        patterns = [p for p in self.patterns if p.num_wildcards == self.min_wildcards]

        # If multiple patterns are returned after the initial filter, do an
        # additional filter to get the pattern with the lowest score.
        if len(patterns) > 1:
            patterns = [p for p in patterns if p.score == self.min_score]

        # After filtering twice, if there are still multiple patterns, raise
        # an exception.
        if len(patterns) > 1:
            raise MultipleMatchesError('More than one pattern match the minimum score')

        if not patterns:
            return None

        return patterns.pop()
