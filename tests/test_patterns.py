import pytest

from pattern_matcher import patterns


class TestNode(object):

    def test_is_wildcard_is_true(self):
        n = patterns.Node('*')
        assert n.is_wildcard()

    def test_is_wildcard_is_false(self):
        n = patterns.Node('foo')
        assert not n.is_wildcard()

    def test_to_string(self):
        n = patterns.Node('foo')
        assert str(n) == 'foo'


class TestPattern(object):

    def test_has_wildcard_is_true(self):
        pattern = ('foo', '*', 'bar')
        p = patterns.Pattern(pattern)
        assert p.has_wildcard()

    def test_has_wildcard_is_false(self):
        pattern = ('foo', 'bar', 'baz')
        p = patterns.Pattern(pattern)
        assert not p.has_wildcard()

    def test_to_string(self):
        pattern = ('foo', 'bar', 'baz')
        p = patterns.Pattern(pattern)
        assert str(p) == 'foo,bar,baz'

    @pytest.mark.parametrize('pattern,expected', [
        (('foo', 'bar', 'baz'), 0),
        (('foo', '*', 'bar'), 1),
        (('*', '*', '*', '*', '*', '*'), 6)
    ])
    def test_num_wildcards_initialized(self, pattern, expected):
        p = patterns.Pattern(pattern)
        assert p.num_wildcards == expected

    @pytest.mark.parametrize('pattern1,pattern2', [
        (('foo', 'bar', '*'), ('foo', '*', 'baz')),
        (('foo', '*', 'baz'), ('*', 'bar', 'baz')),
        (('foo', '*', '*'), ('*', 'bar', '*')),
        (('*', 'bar', '*', '*', 'foo'), ('*', '*', '*', 'qux', 'foo')),
        (('foo', '*', '*', '*', 'foo'), ('*', 'bar', '*', '*', 'foo')),
    ])
    def test_scoring(self, pattern1, pattern2):
        p1 = patterns.Pattern(pattern1)
        p2 = patterns.Pattern(pattern2)
        assert p1.score < p2.score


class TestPatterns(object):
    def test_min_wildcards_initialized_correctly(self):
        raw_patterns = [('*', 'bar', '*')]
        p = patterns.Patterns(raw_patterns)
        assert p.min_wildcards == 2
