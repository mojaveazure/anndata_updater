#!/usr/bin/env python3

"""Update AnnData objects to work across multiple tools

Update AnnData objects to be compatible with multiple toolkits and ecosystems.
In particular, this tool targets compatiblity with Azimuth.

``anndata_updater`` can also be called directly on an H5AD file to update it;
basic usage is as follows

::

    python3 -m anndata_updater

Arguments for ``anndata_updater``:

Args:
    -i|--input: input H5AD file
    -o|--output: optional name for updated H5AD file
    -v|--verbosity: verbosity level, choose from debug, info, warning, error,
        critical; defaults to info
    --version: show program's version number and exits
"""

__version__: str = '0.0.1'

import logging

from typing import List

import anndata

from anndata import AnnData
from scipy.sparse import csc_matrix

__all__: List[str] = [
    'update_anndata',
]

def update_anndata(adata: AnnData) -> AnnData:
    """update_anndata

    Args:
        adata: An AnnData object

    Returns:
        An updated AnnData object
    """
    #   Update adata.X
    if isinstance(adata.X, csc_matrix):
        logging.info("Updating adata.X to a csr matrix")
        adata.X = adata.X.tocsr()
    else:
        logging.debug("adata.X is not a csc_matrix")
    #   Update adata.raw.X
    if adata.raw:
        if isinstance(adata.raw.X, csc_matrix):
            logging.info("Updating adata.raw.X to a csr matrix")
            adata.raw.X = adata.raw.X.tocsr()
        else:
            logging.debug("adata.raw.X is not a csc_matrix")
    else:
        logging.debug("No adata.raw")
    return adata
