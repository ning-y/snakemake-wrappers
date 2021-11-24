__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import os, re
from snakemake.shell import shell

assert hasattr(snakemake.output, "to_download")
assert hasattr(snakemake.output, "id_dataset")
assert hasattr(snakemake.input, "id_project")
assert hasattr(snakemake.input, "id_appsession")

should_delete_project = snakemake.params.delete_project \
    if hasattr(snakemake.params, "delete_project") else True
possibly_delete_project = f"bs project delete --id $(cat {snakemake.input.id_project})" \
    if should_delete_project else ""

shell(f"""
    bs appsession await $(cat {snakemake.input.id_appsession}) > /dev/null
    bs datasets list --project-id $(cat {snakemake.input.id_project}) \
        --is-type illumina.dragen.complete.v0.3.1 \
        --filter-field Name --filter-term {snakemake.wildcards.sample} \
        --terse > {snakemake.output.id_dataset}

    for f in {snakemake.output.to_download}; do
        bs download dataset --id $(cat {snakemake.output.id_dataset}) \
            --exclude "*" --include $(basename $f) --output $(dirname $f)
    done

    {possibly_delete_project}
""")
