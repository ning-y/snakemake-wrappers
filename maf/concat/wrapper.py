__author__ = "Ning Yuan"

from snakemake.shell import shell

MAF_HEADER_REGEX = "^#|^Hugo_Symbol"

assert len(snakemake.input) >= 1
assert len(snakemake.output) == 1

shell(
    f"""
    egrep "{MAF_HEADER_REGEX}" {snakemake.input[0]} | head -n 2 > {snakemake.output[0]}
    for maf in {snakemake.input}; do
        egrep --invert-match "{MAF_HEADER_REGEX}" >> {snakemake.output[0]}
    """)
