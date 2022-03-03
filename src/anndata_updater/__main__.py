#!/usr/bin/env python3

from curses import meta
import os
import sys
import time
import logging
import argparse

from typing import Any, Dict, List, Tuple

import anndata

from . import update_anndata
from . import __version__ as version

log_levels: Dict[str, int] = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def fmttime(start: float, end: float = None, n: int = 3) -> float:
    """Format a timestring for logging

    Args:
        start: Start time, in seconds
        end: End time, in seconds; defaults to time.time()
        n: Number of digits to round to; defaults to 3

    Returns:
        A time in seconds representing the difference between ``start``
        and ``end``, rounded to ``n` digits
    """
    if not end:
        end = time.time()
    return round(end - start, n)


def realpath(path: str) -> str:
    """Generate a real path

    Args:
        path: A file path

    Returns:
        The path expanded for the user and following all symlinks
    """
    return os.path.realpath(os.path.expanduser(path))


#   Create an argument parser
parser: argparse.ArgumentParser = argparse.ArgumentParser(
    add_help=False,
    prog='%(exec)s -m %(mod)s' % {
        'exec': os.path.basename(sys.executable),
        'mod': __package__
    }
)
parser.add_argument( # Input H5AD file
    '-i',
    '--input',
    dest='input',
    type=str,
    required=True,
    metavar='input.h5ad',
    help="input H5AD file"
)
parser.add_argument( # Output H5AD name
    '-o',
    '--output',
    dest='output',
    type=str,
    required=False,
    default=None,
    metavar='out.h5ad',
    help="optional name for updated H5AD file"
)
parser.add_argument( # Verbosity level
    '-v',
    '--verbosity',
    dest='verbosity',
    type=str,
    required=False,
    default='info',
    choices=log_levels,
    metavar='level',
    help="verbosity level, choose from %(choices)s; defaults to %(default)s"
)
parser.add_argument( # Version
    '--version',
    action='version',
    version=version
)
parser.add_argument( # Help action
    '-h',
    '--help',
    action=argparse._HelpAction,
    help=argparse.SUPPRESS
)

#   Parse the arguments
if not sys.argv[1:]:
    parser.print_help(file=sys.stderr)
    raise SystemExit


args: Dict[str, Any] = vars(parser.parse_args())
logging.basicConfig(
    level=log_levels.get(args['verbosity'], 'info'),
    format='%(asctime)s %(levelname)s:\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
args['input'] = realpath(path=args['input'])

if not args['output']:
    args['output'] = '%s_updated%s' % os.path.splitext(args['input'])


#   Update the H5AD file
logging.info("Reading input H5AD file %s", args['input'])
read_start: float = time.time()
adata: anndata.AnnData = anndata.read(args['input'])
logging.debug("Reading input H5AD file took %s seconds", fmttime(start=read_start))

logging.info("Updating AnnData object")
update_start: float = time.time()
adata: anndata.AnnData = update_anndata(adata=adata)
logging.debug("Updating AnnData object took %s seconds", fmttime(start=update_start))

logging.info("Writing out H5AD file to %s", args['output'])
write_start = time.time()
adata.write_h5ad(args['output'])
logging.debug("Writing H5AD file took %s seconds", fmttime(start=write_start))

logging.debug("Program took %s seconds", fmttime(start=read_start))
logging.info("Done")
