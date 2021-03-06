__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None
should_force = hasattr(snakemake.params, "force") and snakemake.params

assert len(snakemake.output) == 1
assert len(snakemake.input) == 3
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    bcftools norm \
        --multiallelics - \
        --fasta-ref {snakemake.input.fa} \
        {"--force" if should_force else ""} \
        {snakemake.input.vcf} | \
    bcftools filter --output-type {output_type} \
        --exclude 'ALT="*"' > {snakemake.output}
    """)
