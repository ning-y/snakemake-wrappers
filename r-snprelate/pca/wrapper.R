suppressPackageStartupMessages({
  library(readr)
  library(SNPRelate)})

write_rds(
  snpgdsPCA(snpgdsOpen(snpgdsVCF2GDS(
      snakemake@input[[1]],
      snakemake@output[["gds"]])),
      num.thread=snakemake@threads[[1]]),
  snakemake@output[["rds"]])
