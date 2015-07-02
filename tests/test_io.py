import io

import pytest

from pattern_matcher.io import Input, Output


class TestInput(object):

    def test_parse(self):
        test_data = '2\n*,*\n*,bar\n1\nfoo/bar\n'
        stream = io.StringIO(test_data)

        patterns, _input = Input.parse(stream)

        assert patterns == '*,*\n*,bar\n'
        assert _input.num_paths == 1
        assert _input.num_patterns == 2
        assert next(_input.stream) == 'foo/bar\n'

    @pytest.mark.parametrize('line,expected', [
        ('5\n', True),
        ('\t5\n', True),
        ('foo/bar/', False),
        ('/foo/bar/', False),
        ('foo,bar', False),
        ('*,*', False),
        ('0\n', True)
    ])
    def test_is_heading(self, line, expected):
        _input = Input(io.StringIO())
        assert _input.is_heading(line) is expected

    @pytest.mark.parametrize('value,expected', [
        (None, False),
        (0, True),
        (1, True),
    ])
    def test_has_num_patterns(self, value, expected):
        _input = Input(io.StringIO())
        _input.num_patterns = value
        assert _input.has_num_patterns() is expected

    @pytest.mark.parametrize('value,expected', [
        (None, False),
        (0, True),
        (1, True),
    ])
    def test_has_num_paths(self, value, expected):
        _input = Input(io.StringIO())
        _input.num_paths = value
        assert _input.has_num_paths() is expected


class TestOutput(object):

    def test_write_adds_new_line_char(self):
        stream = io.StringIO()
        output = Output(stream)
        output.write('foo,bar')
        assert stream.getvalue() == 'foo,bar\n'

    def test_write_adds_new_line_strips_extra_whitespace(self):
        stream = io.StringIO()
        output = Output(stream)
        output.write('\n\tfoo,bar\t\n')
        assert stream.getvalue() == 'foo,bar\n'
