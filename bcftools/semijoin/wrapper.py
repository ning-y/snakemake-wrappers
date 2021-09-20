__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

assert len(snakemake.output) == 1
assert len(snakemake.input) == 4
if output_type is None: raise ValueError("Bad output extension")

# bcftools isec set1.vcf.gz set2.vcf.gz --nfiles =2 --write 1 | bcftools view -h | tail -n 1 | head -c 100
shell(
    f"""
    bcftools isec --output-type {output_type} \
        --collapse none --nfiles =2 --write 1 \
        {snakemake.input.subject} {snakemake.input.object} > {snakemake.output}
    """)
