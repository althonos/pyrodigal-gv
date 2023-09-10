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
    METAGENOMIC_BINS_VIRAL = pyrodigal.MetagenomicBins(
        [b for b in METAGENOMIC_BINS if b.description.split("|")[2] == "V"])
