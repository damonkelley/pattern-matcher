import re


class RegexFactory(object):
    """Generates a regex pattern."""
    WORD_GROUP = '({0}|\*)'
    SEP = '/'

    def _generate_pattern(self, path):
        """Generates a regex pattern."""
        # Split the path up into a list using the forward slash as a
        # delimiter.
        words = (word for word in path.split(self.SEP) if word)

        # Compose a list of regular expression groups for each word in
        # the path.
        patterns = (self.WORD_GROUP.format(re.escape(word)) for word in words)

        # Implode the list into a single regex pattern that will match
        # the path pattern format.
        return '^{0}$'.format(('\,').join(patterns))

    @classmethod
    def create(cls, path):
        rf = cls()
        pattern = rf._generate_pattern(path)
        return re.compile(pattern, re.ASCII | re.MULTILINE)
