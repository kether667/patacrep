"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import os

from patacrep import files, encoding
from patacrep.latex import parse_song
from patacrep.songs import Song

class LatexSong(Song):
    """LaTeX song parser."""

    def _parse(self, __config):
        """Parse content, and return the dictinory of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            self.data = parse_song(song.read(), self.fullpath)
        self.titles = self.data['@titles']
        del self.data['@titles']
        self.language = self.data['@language']
        del self.data['@language']
        if "by" in self.data:
            self.authors = [self.data['by']]
            del self.data['by']
        else:
            self.authors = []

    def render_latex(self, output):
        """Return the code rendering the song."""
        if output is None:
            raise ValueError(output)
        path = files.path2posix(files.relpath(
            self.fullpath,
            os.path.dirname(output)
        ))
        return r'\import{{{}/}}{{{}}}'.format(os.path.dirname(path), os.path.basename(path))

SONG_PARSERS = {
    'is': LatexSong,
    'sg': LatexSong,
    }