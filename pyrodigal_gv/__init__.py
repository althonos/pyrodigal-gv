"""A Pyrodigal extension for giant viruses and viruses with alternative genetic code. 
"""

__version__ = "0.1.0"
__author__ = "Martin Larralde <martin.larralde@embl.de>"
__license__ = "GPLv3"

import typing
import json
import pyrodigal

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


# Parse training info from `prodigal-gv`
with resource_files(__package__).joinpath("meta.json").open("r") as f:
    METAGENOMIC_BINS = pyrodigal.MetagenomicBins([
        pyrodigal.MetagenomicBin(
            description=b["description"],
            training_info=pyrodigal.TrainingInfo(**b["training_info"]),
        )
        for b in json.load(f)
    ])
    METAGENOMIC_BINS_VIRAL = METAGENOMIC_BINS[-12:]


# Convenience subclass to run Pyrodigal in metagenomic mode using the 
# metagenomic models from `prodigal-gv` instead of stock `prodigal`.
class ViralGeneFinder(pyrodigal.OrfFinder):
    """A gene finder for viruses.
    """

    def __init__(
        self,
        training_info: typing.Optional[pyrodigal.TrainingInfo] = None,
        *,
        meta: bool = True,
        metagenomic_bins: typing.Optional[pyrodigal.MetagenomicBins]=None,
        closed: bool = False,
        mask: bool = False,
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
            closed (`bool`): Set to `True` to consider sequences ends
                *closed*, which prevents proteins from running off edges.
                Defaults to `False`.
            mask (`bool`): Prevent genes from running across regions
                containing unknown nucleotides. Defaults to `False`.
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
            min_gene=min_gene,
            min_edge_gene=min_edge_gene,
            max_overlap=max_overlap,
            backend=backend,
        )
