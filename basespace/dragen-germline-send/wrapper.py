__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import os, re
from snakemake.shell import shell

assert len(snakemake.input) > 0
assert hasattr(snakemake.output, "id_project")
assert hasattr(snakemake.output, "id_biosample")
assert hasattr(snakemake.output, "id_appsession")
assert hasattr(snakemake.params, "DRAGEN_VERSION")
assert hasattr(snakemake.params, "HT_REF")

name_project = f"dragen-germline-for-{snakemake.wildcards.sample}"
name_biosample = snakemake.wildcards.sample

# See: https://unix.stackexchange.com/a/229051/285080.
# sponge prevents SIGPIPE from curl, which would mark this job failed.
# "|| true" would fix it too, but I'm afraid it would mask real errors.
shell(f"""
    bs project create --name={name_project} --terse > {snakemake.output.id_project}

    bs upload dataset --project $(cat {snakemake.output.id_project}) \
        --allow-invalid-readnames \
        --biosample-name {name_biosample} {snakemake.input}

    # Query for ID of the just-uploaded biosamples, because bs upload dataset does
    # not return them. The loop is necessary, because it may take a few seconds
    # before just-uploaded biosamples show up in the query results.
    touch {snakemake.output.id_biosample}
    while [[ ! -s {snakemake.output.id_biosample} ]]; do
        bs list biosamples \
            --project-id $(cat {snakemake.output.id_project}) \
            --filter-field BioSampleName --filter-term {snakemake.wildcards.sample} \
            --terse > {snakemake.output.id_biosample}; done

    # Biosamples with multiple FASTQ datasets need to be "unlocked"
    bs biosample unlock $(cat {snakemake.output.id_biosample}) || true

    bs launch application \
        --name "DRAGEN Germline" --app-version {snakemake.params.DRAGEN_VERSION} \
        -o project-id:$(cat {snakemake.output.id_project}) \
        -o input_list.sample-id:$(cat {snakemake.output.id_biosample}) \
        -o ht-ref:{snakemake.params.HT_REF} \
        -o output_format:BAM \
        --terse > {snakemake.output.id_appsession}
""")
