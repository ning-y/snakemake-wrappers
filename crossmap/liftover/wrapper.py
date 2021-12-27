__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 2
assert hasattr(snakemake.output, "passes")
assert hasattr(snakemake.output, "fails")
assert len(snakemake.input) == 3
assert hasattr(snakemake.input, "vcf")
assert hasattr(snakemake.input, "chain")
assert hasattr(snakemake.input, "ref")

shell(f"""
    CrossMap.py vcf {snakemake.input.chain} {snakemake.input.vcf} {snakemake.input.ref} {snakemake.output.passes}
""")
