__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
assert isinstance(snakemake.params.replace, dict)

reader = "zcat" if re.search("\.gz$", snakemake.input[0]) else "cat"
writer = "gzip" if re.search("\.gz$", snakemake.output[0]) else "cat"
editor = " | ".join([
    f'sed --expression "s/^{k}\t/{v}\t/g"' for k, v in snakemake.params.replace.items()])

shell(f"{reader} {snakemake.input} | {editor} | {writer} > {snakemake.output}")
