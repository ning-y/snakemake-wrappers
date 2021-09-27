__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert hasattr(snakemake.input, "bed")
assert hasattr(snakemake.input, "genome")
assert hasattr(snakemake.params, "pad_by")

writer = "gzip" if re.search("\.gz$", snakemake.output[0]) else "cat"

# In the awk script, the first set of double braces escapes this f-string expansion,
# and the second set of double braces escape Snakemake's f-string expansion.
shell(f"""
    bedtools slop \
            -i {snakemake.input.bed} \
            -g {snakemake.input.genome} \
            -b {snakemake.params.pad_by} | \
        {writer} > {snakemake.output}
""")
