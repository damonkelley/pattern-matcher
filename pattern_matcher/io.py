class InputManager(object):
    """Manages the input to the matcher."""
    def __init__(self, stream):
        self.num_patterns = None
        self.num_paths = None
        self.patterns = ''
        self.stream = stream
        self.__parse()

    def __parse(self):
        """Parse the input source.

        This function will iterate through the file and perform the
        following operations in order:
            1. Get the number of patterns.
            2. Copy the patterns to self.patterns, one by one.
            3. Get the number of paths.
            4. Stop reading the input source, leaving off where
               the paths begin.
        """
        for line in self.stream:
            is_heading = self.is_heading(line)

            # Store the heading that indicates the number of patterns.
            if is_heading and not self.has_num_patterns():
                self.num_patterns = int(line.strip())

            # Store of the heading that indicates the number of paths.  This
            # will not happen until we get the number of patterns.  We will
            # then stop reading the file since we have arrived at the paths.
            elif is_heading and not self.has_num_paths():
                self.num_paths = int(line.strip())
                break

            # If the line is not a heading, that means it is a pattern.
            else:
                self.patterns = self.patterns + line

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


class OutputManager(object):
    """Manages the output of the matcher."""
    def __init__(self, stream):
        self.stream = stream

    def writeln(self, text):
        text = text.strip() + '\n'
        self.stream.write(text)
