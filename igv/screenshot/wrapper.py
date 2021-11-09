__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import os, re
from snakemake.shell import shell

assert len(snakemake.output) == 2
assert len(snakemake.input) == 3
assert len(snakemake.params) == 4
assert hasattr(snakemake.output, "png")
assert hasattr(snakemake.output, "batch")
assert hasattr(snakemake.input, "igv")
assert hasattr(snakemake.input, "bam")
assert hasattr(snakemake.input, "bai")
assert hasattr(snakemake.params, "genome")
assert hasattr(snakemake.params, "chrom")
assert hasattr(snakemake.params, "pos_from")
assert hasattr(snakemake.params, "pos_to")

snapshot_directory = os.path.dirname(snakemake.output.png)
snapshot_filename = os.path.basename(snakemake.output.png)

# setSleepInterval: I think a delay is necessary, bcos some operations seem async.
# mxaPanelHeight -1:  "capture the exact area visible on the screen"
batch = f"""setSleepInterval 500
load {snakemake.input.bam}
snapshotDirectory {snapshot_directory}

genome {snakemake.params.genome}
goto {snakemake.params.chrom}:{snakemake.params.pos_from}-{snakemake.params.pos_to}

squish
sort QUALITY
maxPanelHeight -1

snapshot {snapshot_filename}
exit
"""
with open(snakemake.output.batch, "w") as f: f.write(batch)

# See: https://unix.stackexchange.com/a/229051/285080.
# sponge prevents SIGPIPE from curl, which would mark this job failed.
# "|| true" would fix it too, but I'm afraid it would mask real errors.
shell(f"""
    xvfb-run --auto-servernum --server-args="-screen 0 3200x2400x24" \
        {snakemake.input.igv}/igv.sh -b {snakemake.output.batch}""")
