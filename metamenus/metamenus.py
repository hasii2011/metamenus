#
# metamenus vs. 0.13 (15/09/2020)
#
# Written by E. A. Tacao <mailto@tacao.com.br>, (C) 2005... 2020
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3)The name of the author may not be used to
#     endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from logging import Logger
from logging import getLogger

from metamenus import use_unidecode

from metamenus.Configuration import Configuration

# More info on 'history' and 'README.md' files.

# _sep is used internally only and is a substring that _cannot_
# appear on any of the regular menu labels.
# from metamenus.SItem import SItem

_sep = " @@@ "


def _evolve(a):
    """
    Internal use only. This will parse the menu 'tree' supplied.
    """
    from metamenus.SItem import SItem   # TODO We have a cyclical import problem

    top = SItem(a[0])
    il = 0
    cur = {il: top}

    for i in range(1, len(a)):
        params = a[i]
        level  = params[0].count(Configuration().indentation) - 1

        if level > il:
            il += 1
            # Todo fix this !!
            # noinspection PyUnboundLocalVariable
            cur[il] = new_sItem
        elif level < il:
            il = level
        new_sItem = cur[il].AddChild(SItem(params))

    return top


def _clean(s):
    """
    Internal use only. Tries to remove all accented characters from a string.
    """

    if use_unidecode:
        # noinspection PyUnresolvedReferences
        s = unidecode.unidecode("".join([x for x in s if x.isalnum()]))

    else:
        # noinspection SpellCheckingInspection
        so = "áàãâäéèêëíìîïóòõôöúùûüçýÿÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÝ"
        # noinspection SpellCheckingInspection
        sd = "áàãâäéèêëíìîïóòõôöúùûüçýÿÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÝ"

        for i, char in enumerate(so):
            if char in s:
                s = s.replace(char, sd[i])
        s = "".join([x for x in s if x.isalnum()])

    return s


class _mmPrep:
    """
    Generates a temporary file that can be read by gettext utilities in
    order to create a .po file with strings to be translated. This class is
    called when you run metamenus from the command line.

    Usage:
     1. Make sure your menus are in a separate file and that the separate
        file in question contain only your menus;

     2. From a command line, type:
          metamenus.py separate_file output_file

        where 'separate_file' is the python file containing the menu
        'trees', and 'output_file' is the python-like file generated that
        can be parsed by gettext utilities.

    To get a .po file containing the translatable strings, put the
    'output_file' in the app.fil list of translatable files and run the
    mki18n.py script. For more info please see
    <http://wiki.wxpython.org/index.cgi/Internationalization>.
    """

    def __init__(self, filename, output_file):

        #
        # For use by developers
        #
        self.logger: Logger = getLogger('metamenus')

        self.logger.info(f'Parsing {filename}.py...')

        exec(f'import {filename}')
        mod = eval(filename)

        listObjects = []
        for obj in dir(mod):
            if type(getattr(mod, obj)) == list:
                listObjects.append(obj)

        all_lines = []
        for obj in listObjects:
            gError = False
            header = ["\n# Strings for '%s':\n" % obj]
            err, lines = self.parseMenu(mod, obj)
            if not err:
                self.logger.info(f"OK: parsed '{obj}'")
                all_lines += header + lines
            else:
                err, lines = self.parseMenuBar(mod, obj)
                if not err:
                    self.logger.info(f"OK: parsed '{obj}'")
                    all_lines += header + lines
                else:
                    gError = True
            if gError:
                self.logger.warning(f"Could not parse '{obj}'")

        try:
            with open(f'{output_file}.py', "w") as f:
                f.writelines(all_lines)

            self.logger.info(f'File {output_file}.py successfully written.')

        except (ValueError, Exception) as e:
            self.logger.error(f'File {output_file}.py was NOT written.')
            self.logger.error(f'{e.strerror} {e.errno} {e.filename}')

    def form(self, lines):
        """Removes separators and breaks and adds gettext stuff."""

        new_lines = []
        for line in lines:
            if line not in ["-", "/"]:
                new_lines.append("_(" + repr(line) + ")\n")
        return new_lines

    def parseMenuBar(self, mod, obj):
        """Tries to parse a MenuBarEx object."""

        parseError: bool = False
        lines = []
        try:
            for menu in getattr(mod, obj):
                top = _evolve(menu)
                lines.append(top.GetLabelText())
                for child in top.GetChildren(True):
                    lines.append(child.GetLabelText())
        except(ValueError, Exception) as e:
            self.logger.error(f'{e}')
            parseError = True

        return parseError, self.form(lines)

    def parseMenu(self, mod, obj):
        """Tries to parse a MenuEx object."""

        parseError: bool = False
        lines = []
        try:
            top = _evolve(getattr(mod, obj))
            lines.append(top.GetLabelText())
            for child in top.GetChildren(True):
                lines.append(child.GetLabelText())
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            parseError = True

        return parseError, self.form(lines)
