__author__ = "Ning Yuan"

import re
from snakemake.shell import shell

assert len(snakemake.output) == 1
assert len(snakemake.input) == 1
assert f"{snakemake.input}.tbi" == str(snakemake.output)

shell(f"tabix {snakemake.input}")
