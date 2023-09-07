from . import test_gene_finder

def load_tests(loader, suite, pattern):
    suite.addTests(loader.loadTestsFromModule(test_gene_finder))
    return suite