__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import datetime, os, re
from snakemake.shell import shell

assert hasattr(snakemake.input, "gvcfs")
assert hasattr(snakemake.output, "id_project")
assert hasattr(snakemake.output, "ids_datasets")
assert hasattr(snakemake.output, "id_appsession")
assert hasattr(snakemake.params, "DRAGEN_VERSION")
assert hasattr(snakemake.params, "HT_REF")

name_project = f"dragen-joint-genotyping-{datetime.datetime.now().isoformat()}"

shell(f"""
    bs project create --name={name_project} --terse > {snakemake.output.id_project}

    for gvcf in {snakemake.input.gvcfs}; do
        bs upload dataset --project $(cat {snakemake.output.id_project}) --type common.files $gvcf
    done

    # Sometimes, querying for a just-uploaded dataset returns nothing, as if the
    # BaseSpace databases need time to update. To make sure the queried result
    # is up-to-date, check that it contains the expected number of dataset IDs.
    # NB: unfortunately, can be soft-locked here.
    touch {snakemake.output.ids_datasets}
    while [[ $(wc -l < {snakemake.output.ids_datasets}) != {len(snakemake.input.gvcfs)} ]]; do
        bs list dataset \
            --project-id $(cat {snakemake.output.id_project}) \
            --filter-field DataSetType.Id --filter-term common.files \
            --terse > {snakemake.output.ids_datasets}
    done

    bs launch application \
        --name "Dragen Joint Genotyping Pipeline" \
        --app-version {snakemake.params.DRAGEN_VERSION} \
        -o project-id:$(cat {snakemake.output.id_project}) \
        -o ht-ref:{snakemake.params.HT_REF} \
        -o basespace-labs-disclaimer:Accepted \
        -o jg-pipeline-mode:1 \
        -o gvcfs:$(cat {snakemake.output.ids_datasets} | paste --serial --delimiter ,) \
        --terse > {snakemake.output.id_appsession}
""")
