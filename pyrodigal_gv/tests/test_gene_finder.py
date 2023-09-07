import io
import unittest

import pyrodigal
import pyrodigal_gv
from pyrodigal.tests import fasta

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


class TestViralGeneFinder(unittest.TestCase):
    
    def test_topaz_genome(self):
        gene_finder = pyrodigal_gv.ViralGeneFinder(meta=True)
        with resource_files(__package__).joinpath("phage_Topaz.fna").open("r") as f:
            record = next(fasta.parse(f))
            genes = gene_finder.find_genes(record.seq)
        self.assertIs(genes.metagenomic_bin, pyrodigal_gv.METAGENOMIC_BINS[55])
        with resource_files(__package__).joinpath("phage_Topaz.faa").open("r") as f:
            for gene, protein in zip(genes, fasta.parse(f)):
                self.assertEqual(gene.translate(), protein.seq)

    def test_agate_genome(self):
        gene_finder = pyrodigal_gv.ViralGeneFinder(meta=True)
        with resource_files(__package__).joinpath("phage_Agate.fna").open("r") as f:
            record = next(fasta.parse(f))
            genes = gene_finder.find_genes(record.seq)
        self.assertIs(genes.metagenomic_bin, pyrodigal_gv.METAGENOMIC_BINS[54])
        with resource_files(__package__).joinpath("phage_Agate.faa").open("r") as f:
            for gene, protein in zip(genes, fasta.parse(f)):
                self.assertEqual(gene.translate(), protein.seq)
