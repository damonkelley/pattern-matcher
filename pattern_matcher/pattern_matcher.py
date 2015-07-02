from .regex import RegexFactory
from .patterns import Patterns


class PathMatcher(object):
    """Matches a Path to the Path Pattern."""
    NO_MATCH = 'NO MATCH'

    def __init__(self, patterns, input, output):
        self.patterns = patterns
        self.input = input
        self.output = output

    def match(self):
        for path in self.input.stream:
            path = path.strip()
            match = self.find_best_match(path)
            self.output.write(match)

    def find_best_match(self, path):
        re = RegexFactory.create(path)
        matches = Patterns(re.findall(self.patterns))

        match = matches.get_best_pattern()

        if not match:
            return self.NO_MATCH

        return str(match)
