__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import os, re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert re.match("^[A-z0-9]+_[A-z0-9]+\.txt", snakemake.output[0])

buildver = re.search("^[A-z0-9]+(?=_)", snakemake.output[0]).group(0)
table = re.search("(?<=_)[A-z0-9]+", snakemake.output[0]).group(0)

dir = os.path.dirname(snakemake.output[0])
if dir == "": dir = "."

shell(f"annotate_variation.pl --downdb --webfrom annovar --buildver {buildver} {table} {dir}")
