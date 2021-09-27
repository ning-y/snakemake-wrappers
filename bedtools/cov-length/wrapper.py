__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1

reader = "zcat" if re.search("\.gz$", snakemake.input[0]) else "cat"

# In the awk script, the first set of double braces escapes this f-string expansion,
# and the second set of double braces escape Snakemake's f-string expansion.
shell(f"""
    {reader} {snakemake.input} | \
        bedtools merge -i - | \
        awk 'BEGIN{{{{SUM=0}}}} {{{{SUM+=$3-$2}}}} END {{{{print SUM}}}}' > \
        {snakemake.output}
""")
