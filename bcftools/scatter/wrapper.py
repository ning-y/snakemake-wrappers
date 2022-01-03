__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert len(snakemake.output) == 1
assert hasattr(snakemake.params, "output_type")
assert hasattr(snakemake.params, "variants_per_chunk")

shell(
    f"""
    bcftools +scatter \
        --output-type {snakemake.params.output_type} \
        --nsites-per-chunk {snakemake.params.variants_per_chunk} \
        --output {snakemake.output} \
        {snakemake.input}
    """)
