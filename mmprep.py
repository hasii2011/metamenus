
from metamenus.metamenus import _mmprep

__author__  = "E. A. Tacao <mailto |at| tacao.com.br>"
__date__    = "15 Sep 2020, 19:27 GMT-03:00"
__version__ = "0.13"


def commandHandler():
    import sys
    import os.path
    args = sys.argv[1:]
    if len(args) == 2:
        _mmprep(*[os.path.splitext(arg)[0] for arg in args])
    else:
        print("""
    ---------------------------------------------------------------------------
    metamenus %s

    %s
    %s
    Distributed under the BSD-3-Clause LICENSE.
    ---------------------------------------------------------------------------

    Usage:
    ------

    metamenus.py menu_file output_file

    - 'menu_file' is the python file containing the menu 'trees';
    - 'output_file' is the output file generated that can be parsed by the
      gettext utilities.

    Please see metamenus.__doc__ (under the 'More about i18n' section) and
    metamenus._mmprep.__doc__ for more details.
    ---------------------------------------------------------------------------
    """ % (__version__, __author__, __date__))


if __name__ == "__main__":
    commandHandler()