from .regex import RegexFactory
from .patterns import Patterns


class Matcher(object):
    NO_MATCH = 'NO MATCH'

    def __init__(self, raw_patterns, path, re_factory=RegexFactory):
        self.raw_patterns = raw_patterns
        self.path = path
        self.re = re_factory().create(self.path)
        self.patterns = Patterns(self.re.findall(self.raw_patterns))

    def match(self):
        matches = self.patterns.get_best_patterns()

        if len(matches) != 1:
            return self.NO_MATCH

        return str(matches.pop())


class PathMatcher(object):
    """Matches a Path to the Path Pattern."""

    def __init__(self, input, output):
        self.input = InputManager(input)
        self.output = OutputManager(output)
        self.matcher = Matcher

    def match(self):
        for path in self.input.stream:
            matcher = self.Matcher(path.strip())
            print(matcher.match())
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
