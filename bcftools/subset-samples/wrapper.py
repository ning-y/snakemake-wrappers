__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None
samples = ",".join(snakemake.params.samples)

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
if output_type is None: raise ValueError("Bad output extension")

if not hasattr(snakemake.params, "remove_zero_allele_counts") or snakemake.params.remove_zero_allele_counts:
    maybe_remove_ac_zero = "--exclude \"INFO/AC=0\""
else:
    maybe_remove_ac_zero = ""

shell(
    f"""
    bcftools view --samples {samples} {snakemake.input} | \
        bcftools annotate --remove INFO/AC,INFO/AN | \
        bcftools +fill-tags -- --tags AC,AN | \
        bcftools filter --output-type {output_type} {maybe_remove_ac_zero} > {snakemake.output}
    """)
