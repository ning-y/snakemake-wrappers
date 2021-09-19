__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
if output_type is None: raise ValueError("Bad output extension")

# I would use bcftools concat, but it did not work for me.
# See: https://github.com/samtools/bcftools/issues/1580
shell(
    f"""
    bcftools norm --output-type {output_type} \
        --do-not-normalize --remove-duplicates \
        {snakemake.input} > {snakemake.output}
    """)
