__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

output_type = "z" if re.search("vcf\.gz$", snakemake.output[0]) else \
    "v" if re.search("\.vcf$", snakemake.output[0]) else None

assert len(snakemake.output) >= 1
assert len(snakemake.output) < 99  # preconditioned on 2-digit split numbering
assert len(snakemake.input) == 1
if output_type is None: raise ValueError("Bad output extension")

shell(
    f"""
    TMPDIR=$(mktemp -d)

    # Create uncompressed headers (for cat later) and records (for split).
    # split cannot "--number" using stdin.
    bcftools view --header {snakemake.input} > $TMPDIR/header
    bcftools view --no-header {snakemake.input} > $TMPDIR/source

    split --number l/{len(snakemake.output)} -d $TMPDIR/source $TMPDIR/split

    i=0
    for outfile in {snakemake.output}; do
        cat $TMPDIR/header $TMPDIR/split$(printf "%02d" $i) | \
            bcftools view --output-type {output_type} > "$outfile"
        i=$((i+1))  # cannot use i++; see https://stackoverflow.com/a/7256871/6910451
    done

    rm -r $TMPDIR
    """)
