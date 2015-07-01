import pytest
import re

from pattern_matcher.regex import RegexFactory


test_paths = [
    ('foo/bar', '^(foo|\*)\,(bar|\*)$'),
    ('/foo/bar', '^(foo|\*)\,(bar|\*)$'),
    ('foo/bar/', '^(foo|\*)\,(bar|\*)$'),
    ('/foo/bar/', '^(foo|\*)\,(bar|\*)$'),
    ('/foo/bar/baz/qux', '^(foo|\*)\,(bar|\*)\,(baz|\*)\,(qux|\*)$'),
    ('/_/,/`', '^(_|\*)\,(\,|\*)\,(\`|\*)$'),
    ('\t', '^({0}|\*)$'.format(re.escape('\t')))
]


class TestRegexFactory(object):

    @pytest.mark.parametrize('path,expected', test_paths)
    def test_generate_pattern(self, path, expected):
        rf = RegexFactory()
        actual = rf._generate_pattern(path)
        # expected = '^(foo|\*)\,(bar|\*)$'
        assert actual == expected

    def test_regex_matches_path_with_whitespace(self):
        rf = RegexFactory()
        _re = rf.create('\t/\t')

        patterns = "\t,\t\n"
        assert len(_re.findall(patterns)) == 1

    def test_regex_matches_path_with_extended_ascii_chars(self):
        rf = RegexFactory()
        _re = rf.create('··‚‡Ó/‚°‡ﬂ‡ÓÏ˜˘')

        patterns = "··‚‡Ó,‚°‡ﬂ‡ÓÏ˜˘\n"
        assert len(_re.findall(patterns)) == 1

    def test_regex_matches_path_with_non_alphanumerics(self):
        rf = RegexFactory()
        _re = rf.create('<>/-/`')

        patterns = "<>,-,`\n"
        assert len(_re.findall(patterns)) == 1

    def test_regex_matches_path_with_wildcard(self):
        rf = RegexFactory()
        _re = rf.create('foo/*/baz')

        patterns = "foo,*,baz\n"
        assert len(_re.findall(patterns)) == 1

    def test_regex_matches_multiple_patterns(self):
        rf = RegexFactory()
        _re = rf.create('foo/*/baz')

        patterns = "foo,*,baz\n*,*,*\n*,*,baz\n"
        matches = _re.findall(patterns)

        assert len(matches) == 3
        assert ('foo', '*', 'baz') in matches
        assert ('*', '*', '*') in matches
        assert ('*', '*', 'baz') in matches

    def test_regex_returns_patterns_in_order(self):
        rf = RegexFactory()
        _re = rf.create('foo/*/baz')

        patterns = "foo,*,baz\n*,*,*\n*,*,baz\n"
        matches = _re.findall(patterns)

        assert len(matches) == 3
        assert matches[0] == ('foo', '*', 'baz')
        assert matches[1] == ('*', '*', '*')
        assert matches[2] == ('*', '*', 'baz')

    def test_regex_does_not_patterns_that_partially_match(self):
        rf = RegexFactory()
        _re = rf.create('foo/*/baz')

        patterns = "foo,*,baz\n*,*,*\n*,*,baz\nfoo,bar,baz,qux\n"
        matches = _re.findall(patterns)
        assert len(matches) == 3
        assert ('foo', 'bar', 'baz', 'qux') not in matches
