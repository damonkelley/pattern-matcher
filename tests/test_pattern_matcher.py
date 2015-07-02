import io
from os import path
from unittest.mock import Mock

import pytest

from pattern_matcher.io import Output, Input
from pattern_matcher.pattern_matcher import PathMatcher
from pattern_matcher.patterns import MultipleMatchesError

TEST_DIR = path.dirname(path.abspath(__file__))
TEST_DATA_DIR = path.join(TEST_DIR, 'test_data')


class TestPathMatcher(object):

    def test_match(self):
        with open(path.join(TEST_DATA_DIR, 'input1.txt')) as f:
            patterns, _input = Input.parse(f)
            output = Output(io.StringIO())

            pm = PathMatcher(patterns, _input, output)
            pm.match()

        matches = output.stream.getvalue()
        matches = [match for match in matches.split('\n') if match]
        no_matches = [match for match in matches if match == 'NO MATCH']

        assert len(matches) == 5
        assert len(no_matches) == 2

    def test_find_best_match_finds_match(self):
        _input = Mock(spec=Input)
        output = Mock(spec=Output)
        patterns = '*,bar\n'
        pm = PathMatcher(patterns, _input, output)

        match = pm.find_best_match('foo/bar')
        assert str(match) == '*,bar'

    def test_find_best_match_finds_no_match(self):
        _input = Mock(spec=Input)
        output = Mock(spec=Output)
        patterns = ''
        pm = PathMatcher(patterns, _input, output)

        match = pm.find_best_match('foo/bar')
        assert match == 'NO MATCH'

    def test_find_best_match_gets_exception(self):
        _input = Mock(spec=Input)
        output = Mock(spec=Output)
        patterns = 'foo,bar\nfoo,bar\n'
        pm = PathMatcher(patterns, _input, output)

        with pytest.raises(MultipleMatchesError):
            pm.find_best_match('foo/bar')
