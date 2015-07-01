from .io import InputManager, OutputManager
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
        match = self.patterns.get_best_pattern()

        if not match:
            return self.NO_MATCH

        return str(match)


class PathMatcher(object):
    """Matches a Path to the Path Pattern."""

    def __init__(self, input, output):
        self.input = InputManager(input)
        self.output = OutputManager(output)

    def match(self):
        for path in self.input.stream:
            matcher = Matcher(self.input.patterns, path.strip())
            self.output.writeln(matcher.match())
