__author__ = "Ning Yuan"

import os.path, re
from snakemake.shell import shell

release_build = os.path.basename(os.path.dirname(snakemake.input.db))
release = release_build.split("_")[0]
build = release_build.split("_")[1]
species = os.path.basename(os.path.dirname(os.path.dirname(snakemake.input.db)))

# The vep-path command subst. accounts for Ensembl VEP in conda
shell(
    f"""
    vcf2maf.pl \
        --input-vcf {snakemake.input.vcf} \
        --species {species} \
        --ncbi-build {build} \
        --cache-version {release} \
        --ref-fasta {snakemake.input.fa} \
        --vep-path $(which vep | xargs dirname) \
        --output-maf {snakemake.output[0]}
    """)
