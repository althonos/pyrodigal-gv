import configparser
import json
import os
import sys
import py_compile
import tempfile

import setuptools
#import packaging.tags
from setuptools import Command
from setuptools.command.sdist import sdist as _sdist
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

try:
    from setuptools.command.build import build as _build
except ImportError:
    from distutils.command.build import build as _build

try:
    import pycparser
except ImportError as err:
    pycparser = err

# --- Commands ------------------------------------------------------------------

class sdist(_sdist):
    """A `sdist` that generates a `pyproject.toml` on the fly.
    """

    def run(self):
        # build `pyproject.toml` from `setup.cfg`
        c = configparser.ConfigParser()
        c.add_section("build-system")
        c.set("build-system", "requires", str(self.distribution.setup_requires))
        c.set("build-system", 'build-backend', '"setuptools.build_meta"')
        with open("pyproject.toml", "w") as pyproject:
            c.write(pyproject)
        # run the rest of the packaging
        _sdist.run(self)


class generate_json(Command):
    
    user_options = [
        ('training=', 't', 'input file'),
        ('metagenomic=', 'm', 'input file'),
        ('output=', 'o', 'output file'),
    ]

    def initialize_options(self):
        self.training = None
        self.metagenomic = None
        self.output = None

    def finalize_options(self):
        self.ensure_filename("training")
        self.ensure_filename("metagenomic")

    def _extract_initializers(self):
        with open(self.training, "rb") as src:
            lines = []
            index = 0
            for line in src:
                if line.startswith(b"void initialize_metagenome"):
                    lines.append(line)
                    break
            for line in src:
                if line.startswith(b"void initialize_metagenome"):
                    yield b"\n".join(lines).decode()
                    lines.clear()
                    index += 1
                lines.append(line)
            yield b"\n".join(lines).decode()

    def _parse_initializers(self):
        parser = pycparser.CParser()
        for block in self._extract_initializers():
            literals = parser.parse(block).ext[0].body.block_items[0].init.exprs
            gc, trans_table, st_wt, bias, type_wt, uses_sd, rbs_wt, ups_comp, mot_wt, no_mot, gene_dc = literals
            yield {
                "gc": self._literal(gc),
                "translation_table": int(trans_table.value),
                "start_weight": self._literal(st_wt),
                "bias": [ self._literal(x) for x in bias.exprs ],
                "type_weights": [ self._literal(x) for x in type_wt.exprs ],
                "uses_sd": int(uses_sd.value),
                "rbs_weights": [self._literal(x) for x in rbs_wt.exprs],
                "upstream_compositions": [ 
                    [ self._literal(y) for y in x.exprs ] 
                    for x in ups_comp.exprs
                ],
                "motif_weights": [
                    [ [ self._literal(z) for z in y.exprs] for y in x.exprs ]
                    for x in mot_wt.exprs
                ],
                "missing_motif_weight": self._literal(no_mot),
                "coding_statistics": [ self._literal(x) for x in gene_dc.exprs ]
            }

    def _extract_descriptions(self):
        with open(self.metagenomic, "rb") as src:
            lines = []
            for line in src:
                if line.startswith(b"void initialize_metagenomic_bins"):
                    lines.append(line)
                    break
            lines.extend(src)
        return b"\n".join(lines).decode()

    def _parse_descriptions(self):
        parser = pycparser.CParser()
        function = parser.parse(self._extract_descriptions())
        body = function.ext[0].body
        for call in body.block_items:
            if call.name.name != "sprintf":
                continue
            yield {
                "template": call.args.exprs[1].value.strip('"'), 
                "index": int(call.args.exprs[2].value), 
                "name": call.args.exprs[3].value.strip('"'),
                "kingdom": call.args.exprs[4].value.strip('"'),
                "gc": float(call.args.exprs[5].value)
            }

    def _literal(self, node):
        if isinstance(node, pycparser.c_ast.Constant):
            return float(node.value)
        elif isinstance(node, pycparser.c_ast.UnaryOp):
            if node.op == "-":
                return -self._literal(node.expr)
        raise NotImplementedError(node)

    def run(self):
        if isinstance(pycparser, ImportError):
            raise RuntimeError("`pycparser` is required to run the `generate_json` command") from pycparser
        parser = pycparser.CParser()
        descriptions = self._parse_descriptions()
        training_infos = self._parse_initializers()
        data = []
        for tinf, desc in zip(training_infos, descriptions):
            description = desc["template"] % (desc["index"], desc["name"], desc["kingdom"], desc["gc"], tinf["translation_table"], int(tinf["uses_sd"]))
            entry = dict(description=description, training_info=tinf)
            data.append(entry)
            print("converted training info for {!r}".format(description), file=sys.stderr)
        with open(self.output, "w") as dst:
            json.dump(data, dst)


# class build(_build):

#     def run(self):
#         json_file = os.path.join("pyrodigal_gv", "meta.json")
#         python_file = os.path.join(self.build_lib, "pyrodigal_gv", "meta.py")
#         bytecode_file = os.path.join(self.build_lib, "pyrodigal_gv", "meta.pyc")

#         with open(os.path.join("pyrodigal_gv", "meta.json")) as f:
#             data = json.load(f)

#         output_file = os.path.join(self.build_lib, "pyrodigal_gv", "meta.tmp")
#         self.mkpath(os.path.dirname(output_file))
#         with tempfile.NamedTemporaryFile(mode="r+", dir=self.build_lib, suffix=".py") as dst:
#             print("import pyrodigal", file=dst)
#             print("METAGENOMIC_BINS = pyrodigal.MetagenomicBins((", file=dst)
#             for entry in data:
#                 print("pyrodigal.MetagenomicBin(", file=dst)
#                 print("description={!r},".format(entry["description"]), file=dst)
#                 print("training_info=pyrodigal.TrainingInfo(**{})".format(json.dumps(entry["training_info"])), file=dst)
#                 print("),", file=dst)
#             print("))", file=dst)
#             print("METAGENOMIC_BINS_VIRAL = pyrodigal.MetagenomicBins(", file=dst)
#             print("[b for b in METAGENOMIC_BINS if b.description.split('|')[2] == 'V'])", file=dst)
#             dst.flush()
#             py_compile.compile(dst.name, bytecode_file)

#         _build.run(self)
#         if os.path.exists(python_file):
#             os.remove(python_file)


# class bdist_wheel(_bdist_wheel):
    
#     def initialize_options(self):
#         _bdist_wheel.initialize_options(self)
#         self.python_tag = "{}{}".format(packaging.tags.interpreter_name(), packaging.tags.interpreter_version())


# --- Setup ---------------------------------------------------------------------

setuptools.setup(
    cmdclass={
        "sdist": sdist,
        "generate_json": generate_json,
        # "build": build,
        # "bdist_wheel": bdist_wheel,
    }
)
