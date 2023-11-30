"""A Pyrodigal extension for improved prediction of viral genes.
"""

__version__ = "0.3.1"
__author__ = "Martin Larralde <martin.larralde@embl.de>"
__license__ = "GPLv3"

import typing
import pyrodigal

from .meta import METAGENOMIC_BINS, METAGENOMIC_BINS_VIRAL

# Expose the wrapped `prodigal-gv` version
PRODIGAL_GV_VERSION = "v2.11.0"

# Convenience subclass to run Pyrodigal in metagenomic mode using the
# metagenomic models from `prodigal-gv` instead of stock `prodigal`.
class ViralGeneFinder(pyrodigal.GeneFinder):
    """A gene finder with additional viral metagenomic models.
    """

    def __init__(
        self,
        training_info: typing.Optional[pyrodigal.TrainingInfo] = None,
        *,
        meta: bool = False,
        metagenomic_bins: typing.Optional[pyrodigal.MetagenomicBins] = None,
        closed: bool = False,
        mask: bool = False,
        min_mask: int = 50,
        min_gene: int = 90,
        min_edge_gene: int = 60,
        max_overlap: int = 60,
        backend: str = "detect",
        viral_only: bool = False,
    ):
        """Create a new viral gene finder.

        Arguments:
            training_info (`~pyrodigal.TrainingInfo`, optional): A training
                info instance to use in single mode without having to
                train first.

        Keyword Arguments:
            meta (`bool`): Set to `False` to disable metagenomic mode.
                Defaults to `True`.
            viral_only (`bool`): Set to `True` to only run on viral models
                when running the gene finder. Ignored when the gene finder
                is not in *meta* mode. Defaults to `False`.
            metagenomic_bins (`~pyrodigal.MetagenomicBins`, optional): The
                metagenomic bins to use while in *meta* mode. When `None`
                is given, use all models from ``prodigal-gv``, unless
                ``viral_only`` is set to `True`.
            closed (`bool`): Set to `True` to consider sequences ends
                *closed*, which prevents proteins from running off edges.
                Defaults to `False`.
            mask (`bool`): Prevent genes from running across regions
                containing unknown nucleotides. Defaults to `False`.
            min_mask (`int`): The minimum mask length, when region masking
                is enabled. Regions shorter than the given length will not
                be masked, which may be helpful to prevent masking of 
                single unknown nucleotides.
            min_gene (`int`): The minimum gene length. Defaults to the value
                used in Prodigal.
            min_edge_gene (`int`): The minimum edge gene length. Defaults to
                the value used in Prodigal.
            max_overlap (`int`): The maximum number of nucleotides that can
                overlap between two genes on the same strand. **This must be
                lower or equal to the minimum gene length**.
            backend (`str`): The backend implementation to use for computing
                the connection scoring pre-filter. Leave as ``"detect"`` to
                select the fastest available implementation at runtime.
                *Mostly useful for testing*.

        """
        if metagenomic_bins is None:
            metagenomic_bins = (
                METAGENOMIC_BINS_VIRAL if viral_only else METAGENOMIC_BINS
            )
        super().__init__(
            training_info,
            meta=meta,
            metagenomic_bins=metagenomic_bins,
            closed=closed,
            mask=mask,
            min_mask=min_mask,
            min_gene=min_gene,
            min_edge_gene=min_edge_gene,
            max_overlap=max_overlap,
            backend=backend,
        )
