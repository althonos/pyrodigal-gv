import argparse
import sys
import typing

from pyrodigal import GeneFinder
from pyrodigal.cli import main as _main, argument_parser as _argument_parser
from . import ViralGeneFinder, __version__

def argument_parser(
    prog: str = "pyrodigal-gv",
    version: str = __version__,
) -> argparse.ArgumentParser:
    parser = _argument_parser(prog=prog, version=version)
    mode_action = next( action for action in parser._actions if action.dest == "p" )
    mode_action.default = "meta"
    return parser


def main(
    argv: typing.Optional[typing.List[str]] = None,
    stdout: typing.TextIO = sys.stdout,
    stderr: typing.TextIO = sys.stderr,
    *,
    gene_finder_factory: typing.Callable[..., GeneFinder] = ViralGeneFinder,
    argument_parser: typing.Callable[[], argparse.ArgumentParser] = argument_parser,
) -> int:
    return _main(
        argv,
        stdout=stdout,
        stderr=stderr,
        gene_finder_factory=gene_finder_factory,
        argument_parser=argument_parser
    )
