#! /usr/bin/env python

import sys
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pattern-matcher',
    version='0.1.0',
    author='Damon Kelley',
    author_email='damon.kelley@gmail.com',
    url='https://github.com/damonkelley/pattern-matching-paths',
    license='MIT',
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    description='Matching paths to patterns.',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': ['pattern-matcher=pattern_matcher:main']
    }
)
