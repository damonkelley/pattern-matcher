import sys

from . import io
from .pattern_matcher import PathMatcher


def main():
    patterns, input = io.Input.parse(sys.stdin)
    output = io.Output(sys.stdout)
    pm = PathMatcher(patterns, input, output)

    pm.match()
