import re


class RegexFactory(object):
    """Generates a regex pattern."""
    WORD_GROUP = '({0}|\*)'
    SEP = '/'

    def _generate_pattern(self, path):
        """Generates a regex pattern."""
        # Split the path up into a list using the forward slash as a
        # delimiter.
        words = (word for word in path.split(self.SEP) if word)

        # Compose a list of regular expression groups for each word in
        # the path.
        patterns = (self.WORD_GROUP.format(re.escape(word)) for word in words)

        # Implode the list into a single regex pattern that will match
        # the path pattern format.
        return '^{0}$'.format(('\,').join(patterns))

    def new(self, path):
        pattern = self._generate_pattern(path)
        return re.compile(pattern, re.ASCII | re.MULTILINE)


class Matcher(object):
    def __init__(self, patterns, re_factory=RegexFactory):
        self.patterns
        self.re_factory = re_factory

    def _find_matches(self, path):
        regex = self.re_factory.new(path)
        return regex.findall(self.patterns)

    def _get_best_match(self, matches):
        pass

    def match(self, path):
        """Matches a path to a path pattern."""
        matches = self._find_matches(path)
        return self._get_best_match(matches)


class PathMatcher(object):
    """Matches a Path to the Path Pattern."""

    def __init__(self, input, output):
        self.input = InputManager(input)
        self.output = OutputManager(output)
        self.matcher = Matcher()

    def match(self):
        for path in self.input.stream:
            self.matcher.match(path.strip())
        # send to stdout


class InputManager(object):
    """Manages the input to the matcher."""
    pass


class OutputManager(object):
    """Manages the output of the matcher."""
    pass


if __name__ == '__main__':
    import sys
    main = PathMatcher(sys.stdin, sys.stdout)
    main.match()
