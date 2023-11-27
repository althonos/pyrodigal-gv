# 🔥🦠 Pyrodigal-gv [![Stars](https://img.shields.io/github/stars/althonos/pyrodigal-gv.svg?style=social&maxAge=3600&label=Star)](https://github.com/althonos/pyrodigal-gv/stargazers)

*A [Pyrodigal](https://github.com/althonos/pyrodigal) extension to predict genes in giant viruses and viruses with alternative genetic code.*

[![Actions](https://img.shields.io/github/actions/workflow/status/althonos/pyrodigal-gv/test.yml?branch=main&logo=github&style=flat-square&maxAge=300)](https://github.com/althonos/pyrodigal-gv/actions)
[![Coverage](https://img.shields.io/codecov/c/gh/althonos/pyrodigal-gv?style=flat-square&maxAge=3600&logo=codecov)](https://codecov.io/gh/althonos/pyrodigal-gv/)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square&maxAge=2678400)](https://choosealicense.com/licenses/gpl-3.0/)
[![PyPI](https://img.shields.io/pypi/v/pyrodigal-gv.svg?style=flat-square&maxAge=3600&logo=PyPI)](https://pypi.org/project/pyrodigal-gv)
[![Bioconda](https://img.shields.io/conda/vn/bioconda/pyrodigal-gv?style=flat-square&maxAge=3600&logo=anaconda)](https://anaconda.org/bioconda/pyrodigal-gv)
[![AUR](https://img.shields.io/aur/version/python-pyrodigal-gv?logo=archlinux&style=flat-square&maxAge=3600)](https://aur.archlinux.org/packages/python-pyrodigal-gv)
[![Wheel](https://img.shields.io/pypi/wheel/pyrodigal.svg?style=flat-square&maxAge=3600)](https://pypi.org/project/pyrodigal-gv/#files)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyrodigal-gv.svg?style=flat-square&maxAge=600&logo=python)](https://pypi.org/project/pyrodigal/#files)
[![Python Implementations](https://img.shields.io/pypi/implementation/pyrodigal-gv.svg?style=flat-square&maxAge=600&label=impl)](https://pypi.org/project/pyrodigal-gv/#files)
[![Source](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=2678400&style=flat-square)](https://github.com/althonos/pyrodigal-gv/)
[![GitHub issues](https://img.shields.io/github/issues/althonos/pyrodigal-gv.svg?style=flat-square&maxAge=600)](https://github.com/althonos/pyrodigal-gv/issues)
[![Changelog](https://img.shields.io/badge/keep%20a-changelog-8A0707.svg?maxAge=2678400&style=flat-square)](https://github.com/althonos/pyrodigal-gv/blob/main/CHANGELOG.md)
[![Downloads](https://img.shields.io/pypi/dm/pyrodigal-gv?style=flat-square&color=303f9f&maxAge=86400&label=downloads)](https://pepy.tech/project/pyrodigal-gv)


## 🗺️ Overview

[Pyrodigal](https://github.com/althonos/pyrodigal) is a Python module that provides 
[Cython](https://cython.org/) bindings to [Prodigal](https://github.com/hyattpd/Prodigal/), 
an efficient gene finding method for genomes and metagenomes based on dynamic programming.

`pyrodigal-gv` is a small extension module for `pyrodigal` which distributes
additional metagenomic models for giant viruses and viruses that use
alternative genetic codes, first provided by [Antônio Camargo](https://github.com/apcamargo)
in [`prodigal-gv`](https://github.com/apcamargo/prodigal-gv). The new models
are the following:

* Acanthamoeba polyphaga mimivirus
* Paramecium bursaria Chlorella virus
* Acanthocystis turfacea Chlorella virus
* [VirSorter2](https://github.com/jiarong/VirSorter2)'s NCLDV gene model
* [Topaz](https://www.biorxiv.org/content/10.1101/2021.08.26.457843v1.full) (genetic code 15)
* [Agate](https://www.biorxiv.org/content/10.1101/2021.08.26.457843v1.full) (genetic code 15)
* Gut phages (genetic code 15)
* Gut phages (genetic code 11) × 5

## 🔧 Installing

`pyrodigal-gv` can be installed directly from [PyPI](https://pypi.org/project/pyrodigal/)
as a universal wheel that contains all required data files:
```console
$ pip install pyrodigal-gv
```

<!--
Otherwise, `pyrodigal-gv` is also available as a [Bioconda](https://bioconda.github.io/)
package:
```console
$ conda install -c bioconda pyrodigal-gv
``` -->

## 💡 Example

Just use the provided `ViralGeneFinder` class instead of the usual `GeneFinder`
from `pyrodigal`, and the new viral models will be used automatically in
*meta* mode:

```python
import Bio.SeqIO
import pyrodigal_gv

record = Bio.SeqIO.read("sequence.gbk", "genbank")

orf_finder = pyrodigal_gv.ViralGeneFinder(meta=True)
for i, pred in enumerate(orf_finder.find_genes(bytes(record.seq))):
    print(f">{record.id}_{i+1}")
    print(pred.translate())
```

`ViralGeneFinder` has an additional keyword argument, `viral_only`, which can
be set to `True` to run gene calling using only viral models.

## 🔨 Command line

`pyrodigal-gv` comes with a very simple command line similar to Prodigal and `pyrodigal`:
```console
$ pyrodigal-gv -i <input_file.fasta> -a <gene_translations.fasta> -d <gene_sequences.fasta>
```

*Contrary to `prodigal` and `pyrodigal`, the `pyrodigal-gv` script runs in **meta** mode
by default! Running in **single** mode can be done with `pyrodigal-gv -p single` but 
the results will be exactly the same as `pyrodigal`, so why would you ever do this ⁉️*


## 🔖 Citation

Pyrodigal is scientific software, with a
[published paper](https://doi.org/10.21105/joss.04296)
in the [Journal of Open-Source Software](https://joss.theoj.org/). Please
cite both [Pyrodigal](https://doi.org/10.21105/joss.04296)
and [Prodigal](https://doi.org/10.1186/1471-2105-11-119) if you are using it in
an academic work, for instance as:

> Pyrodigal (Larralde, 2022), a Python library binding to Prodigal (Hyatt *et al.*, 2010).

Detailed references are available on the [Publications page](https://pyrodigal.readthedocs.io/en/stable/publications.html) of the
[online documentation](https://pyrodigal.readthedocs.io/).


## 💭 Feedback

### ⚠️ Issue Tracker

Found a bug ? Have an enhancement request ? Head over to the [GitHub issue
tracker](https://github.com/althonos/pyrodigal-gv/issues) if you need to report
or ask something. If you are filing in on a bug, please include as much
information as you can about the issue, and try to recreate the same bug
in a simple, easily reproducible situation.

### 🏗️ Contributing

Contributions are more than welcome! See
[`CONTRIBUTING.md`](https://github.com/althonos/pyrodigal-gv/blob/main/CONTRIBUTING.md)
for more details.

## 📋 Changelog

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html)
and provides a [changelog](https://github.com/althonos/pyrodigal-gv/blob/main/CHANGELOG.md)
in the [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) format.


## ⚖️ License

This library is provided under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/).
The Prodigal code was written by [Doug Hyatt](https://github.com/hyattpd) and is distributed under the
terms of the GPLv3 as well. See `vendor/Prodigal/LICENSE` for more information.
The giant virus and alternative genetic code virus parameters were created
by [Antônio Camargo](https://github.com/apcamargo).

*This project is in no way not affiliated, sponsored, or otherwise endorsed
by the [original Prodigal authors](https://github.com/hyattpd). It was developed
by [Martin Larralde](https://github.com/althonos/) during his PhD project
at the [European Molecular Biology Laboratory](https://www.embl.de/) in
the [Zeller team](https://github.com/zellerlab).*
