from .regex import RegexFactory
from .patterns import Patterns


class Matcher(object):
    NO_MATCH = 'NO MATCH'

    def __init__(self, raw_patterns, path, re_factory=RegexFactory):
        self.raw_patterns = raw_patterns
        self.path = path
        self.re = re_factory().create(self.path)
        self.patterns = Patterns(self.re.findall(self.raw_patterns))

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
