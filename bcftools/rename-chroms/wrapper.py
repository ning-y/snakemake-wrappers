__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 2
assert hasattr(snakemake.output, "vcf")
assert hasattr(snakemake.output, "tmp")
assert hasattr(snakemake.input, "vcf")
assert str(snakemake.input.vcf)  # Must have a string representation
assert hasattr(snakemake.params, "rename")

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None
if output_type is None: raise ValueError("Bad output extension")

with open(snakemake.output.tmp, "w") as txtfile:
    lines_to_write = [f"{old}\t{new}" for old, new in snakemake.params.rename.items()]
    text_to_write = "\n".join(lines_to_write)
    txtfile.write(text_to_write)

shell(
    f"""
    bcftools annotate --output-type {output_type} \
        --rename-chrs {snakemake.output.tmp} \
        {snakemake.input} > {snakemake.output.vcf}
    """)
