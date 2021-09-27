__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

assert hasattr(snakemake.input, "vcf")
assert hasattr(snakemake.input, "tbi")
assert hasattr(snakemake.input, "bed")
assert len(snakemake.output) == 1
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    bcftools view --output-type {output_type} \
        --regions-file {snakemake.input.bed} \
        {snakemake.input.vcf} > {snakemake.output}
    """)
