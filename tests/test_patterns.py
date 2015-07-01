import pytest

from pattern_matcher import patterns

# Generic testing patterns.
# These are constructed so that the first patterns is always a better match.
test_patterns = [
    ([('foo', 'bar', '*'), ('foo', '*', 'baz')]),
    ([('foo', '*', 'baz'), ('*', 'bar', 'baz')]),
    ([('foo', '*', '*'), ('*', 'bar', '*')]),
    ([('*', 'bar', '*', '*', 'foo'), ('*', '*', '*', 'qux', 'foo')]),
    ([('foo', '*', '*', '*', 'foo'), ('*', 'bar', '*', '*', 'foo')]),
]


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

    @pytest.mark.parametrize('pattern,expected', [
        (('foo', 'bar', 'baz'), 0),
        (('foo', '*', 'bar'), (3/float(5))),
        (('foo', '*', '*'), (3/float(5) + 3/float(6))),
    ])
    def test_score_initialized(self, pattern, expected):
        p = patterns.Pattern(pattern)
        assert p.score == expected

    @pytest.mark.parametrize('pattern1,pattern2', test_patterns)
    def test_scoring(self, pattern1, pattern2):
        # pattern1, pattern2 = test_patterns
        p1 = patterns.Pattern(pattern1)
        p2 = patterns.Pattern(pattern2)
        assert p1.score < p2.score


class TestPatterns(object):
    def test_min_wildcards_initialized_correctly(self):
        test_patterns = [('*', 'bar', '*')]
        p = patterns.Patterns(test_patterns)
        assert p.min_wildcards == 2

    def test_min_wildcards_is_zero_with_no_wildcards(self):
        test_patterns = [('foo', 'bar', 'baz')]
        p = patterns.Patterns(test_patterns)
        assert p.min_wildcards == 0

    @pytest.mark.parametrize('test_patterns', test_patterns)
    def test_min_score_initialized_correctly1(self, test_patterns):
        p = patterns.Patterns(test_patterns)
        lowest_scoring_pattern = p.patterns[0]
        assert p.min_score == lowest_scoring_pattern.score

    def test_has_min_score_is_true(self):
        test_patterns = [('*', 'bar', '*')]
        p = patterns.Patterns(test_patterns)
        assert p.has_min_wildcards() is True

    def test_has_min_score_is_true_with_no_wildcards(self):
        test_patterns = [('foo', 'bar', 'baz')]
        p = patterns.Patterns(test_patterns)
        assert p.has_min_wildcards() is True

    def test_has_min_score_is_false(self):
        test_patterns = []
        p = patterns.Patterns(test_patterns)
        assert p.has_min_wildcards() is False

    def test_get_best_pattern_with_empty_list_of_input_patterns(self):
        p = patterns.Patterns([])
        match = p.get_best_pattern()
        assert match is None

    @pytest.mark.parametrize('test_patterns', test_patterns)
    def test_get_best_pattern(self, test_patterns):
        p = patterns.Patterns(test_patterns)
        lowest_scoring_pattern = p.patterns[0]
        assert p.get_best_pattern() == lowest_scoring_pattern
