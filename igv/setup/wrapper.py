__author__ = "Ning Yuan"
# Adapted from https://gist.github.com/mdshw5/1a32d1ee141aa73af421299a8d0a6e4a

import os, re
from snakemake.shell import shell

assert len(snakemake.output) == 1

igv_basename = os.path.basename(snakemake.output[0])
igv_version = re.search("(?<=IGV_)\d+\.\d+\.\d+", igv_basename).group(0)
igv_major_minor = re.search("^\d+\.\d+", igv_version).group(0)
igv_download_url = f"https://data.broadinstitute.org/igv/projects/downloads/{igv_major_minor}/IGV_{igv_version}.zip"

# See: https://unix.stackexchange.com/a/229051/285080.
# sponge prevents SIGPIPE from curl, which would mark this job failed.
# "|| true" would fix it too, but I'm afraid it would mask real errors.
shell(f"""
    curl {igv_download_url} | sponge | jar x
    chmod +x IGV_{igv_version}/igv.sh
""")
