import sys

from . import io
from .pattern_matcher import PathMatcher


def main():
    if sys.version_info.major < 3:
        sys.exit('Python 3.x or greater is required.')

    patterns, _input = io.Input.parse(sys.stdin)
    output = io.Output(sys.stdout)
    pm = PathMatcher(patterns, _input, output)

    pm.match()
