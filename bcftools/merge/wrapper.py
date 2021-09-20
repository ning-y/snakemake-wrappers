__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

assert len(snakemake.output) == 1
assert len(snakemake.input.targets) == len(snakemake.input.indices)
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    bcftools merge --output-type {output_type} \
        --merge none \
        {snakemake.input.targets} > {snakemake.output}
    """)
