import logging
import sys

from .regex import RegexFactory
from .patterns import Patterns, MultipleMatchesError


logging.basicConfig(stream=sys.stderr, format='[%(levelname)s] %(message)s')


class PathMatcher(object):
    """Matches paths to patterns.

    The path is a string composed of a series of character groupings
    seperated by a forward slash (/) (e.g. foo/bar)

    A pattern is a also a string composed of a series of character groupings,
    but the groups are delimited by a comma. (e.g. foo,bar)
    """
    NO_MATCH = 'NO MATCH'

    def __init__(self, patterns, _input, output):
        """Initialize the PathMatcher instance.

        Parameters:
            patterns: a string of patterns delimited by newlines.
            _input: an instance of pattern_matcher.io.Input
            output: an instance of pattern_matcher.io.Output
        """
        self.patterns = patterns
        self.input = _input
        self.output = output

    def match(self):
        """Get a single match for each path in the file and write it to
        the output stream.
        """
        for path in self.input.stream:
            path = path.strip()
            try:
                match = self.find_best_match(path)
                self.output.write(match)

            except MultipleMatchesError:
                logging.error('Unable to match {0} to a single pattern. '
                              'Multiple matches found.'.format(path))

    def find_best_match(self, path):
        """Find and return the single best matching pattern for a path.

        Returns 'NO MATCH' if no pattern is found.
        """
        re = RegexFactory.create(path)
        matches = Patterns(re.findall(self.patterns))

        match = matches.get_best_pattern()

        if not match:
            return self.NO_MATCH

        return str(match)
