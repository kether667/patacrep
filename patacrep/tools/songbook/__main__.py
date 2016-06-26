"""Perform operations on songbook."""

import argparse
import logging
import os
import shutil
import sys
import textwrap

from patacrep import errors
from patacrep.songbook import open_songbook

LOGGER = logging.getLogger("patatools.songbook")

def filename(name):
    """Check that argument is an existing, readable file name.

    Return the argument for convenience.
    """
    if os.path.isfile(name) and os.access(name, os.R_OK):
        return name
    raise argparse.ArgumentTypeError("Cannot read file '{}'.".format(name))

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="patatools songbook",
        description="Operations related to a songbook.",
        formatter_class=argparse.RawTextHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        description="",
        dest="command",
        )
    subparsers.required = True

    clean = subparsers.add_parser(
        "clean_cache",
        description="Clean the caches related to a songbook.",
        help="Delete cache.",
        )
    clean.add_argument(
        'songbook',
        metavar="SONGBOOK",
        help=textwrap.dedent("""Songbook file to be used to look for cache path."""),
        type=filename,
        )
    clean.set_defaults(command=do_clean)

    return parser

def do_clean(namespace):
    """Execute the `patatools songbook clean_cache` command."""
    for datadir in open_songbook(namespace.songbook)['_datadir']:
        cachedir = os.path.join(datadir, ".cache")
        LOGGER.info("Deleting cache directory '{}'...".format(cachedir))
        if os.path.isdir(cachedir):
            shutil.rmtree(cachedir)

def main(args):
    """Main function: run from command line."""
    options = commandline_parser().parse_args(args[1:])
    try:
        options.command(options)
    except errors.SongbookError as error:
        LOGGER.error(str(error))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
