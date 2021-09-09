__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None
samples = ",".join(snakemake.params.samples)

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    bcftools view -O{output_type} --samples {samples} \
        {snakemake.input} > {snakemake.output}
    """)
