class Input(object):
    """Wrapper class for the input stream."""

    def __init__(self, stream):
        """Initialize an Input instance.

        Parameters:
            stream: The file object that will be read from.
        """
        self.num_patterns = None
        self.num_paths = None
        self.stream = stream

    @classmethod
    def parse(cls, stream):
        """Parse the input source.

        Returns the raw patterns and an initialized Input instance.

        This function will iterate through the file and perform the
        following operations in order:
            1. Get the number of patterns.
            2. Copy the patterns to self.patterns, one by one.
            3. Get the number of paths.
            4. Stop reading the stream where the paths begin.
        """
        _input = cls(stream)

        patterns = ''
        for line in _input.stream:
            is_heading = _input.is_heading(line)

            # Store the heading that indicates the number of patterns.
            if is_heading and not _input.has_num_patterns():
                _input.num_patterns = int(line.strip())

            # Store the heading that indicates the number of paths.  This
            # will not happen until we get the number of patterns.  We will
            # then stop reading the file since we have arrived at the paths.
            elif is_heading and not _input.has_num_paths():
                _input.num_paths = int(line.strip())
                break

            # If the line is not a heading, that means it is a pattern.
            else:
                patterns = patterns + line

        return patterns, _input

    def is_heading(self, line):
        """True if the line is a section heading for either the patterns
        section or the paths section.
        """
        return line.strip().isdigit()

    def has_num_patterns(self):
        """True if self.num_patterns is not None."""
        return self.num_patterns is not None

    def has_num_paths(self):
        """True if self.num_paths is not None."""
        return self.num_paths is not None


class Output(object):
    """Wrapper class for the output stream."""

    def __init__(self, stream):
        """Initialize an Output instance.

        Parameters:
            stream: The file object that output it to be written to.
        """
        self.stream = stream

    def write(self, text):
        """Sanitize and write text to the stream.

        Parameters:
            text: the string to be written.
        """
        text = '{0}\n'.format(text.strip())
        self.stream.write(text)
