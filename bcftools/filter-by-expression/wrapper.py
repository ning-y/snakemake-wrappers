__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

include = f"--include '{snakemake.params.include}'" \
    if hasattr(snakemake.params, "include") else ""
exclude = f"--exclude '{snakemake.params.exclude}'" \
    if hasattr(snakemake.params, "exclude") else ""

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    bcftools filter --output-type {output_type} {include} {exclude} \
        {snakemake.input} > {snakemake.output}
    """)
