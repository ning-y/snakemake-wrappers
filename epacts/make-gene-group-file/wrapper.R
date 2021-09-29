suppressPackageStartupMessages({
  library(vcfR)
  library(tidyverse)
  library(assertthat)})

assert_that(!is.null(snakemake@params[["info"]]))

vcf <- read.vcfR(snakemake@input[[1]])
tb <- as_tibble(getFIX(vcf)) %>%
  mutate(genes=extract.info(vcf, snakemake@params[["info"]])) %>%
  transmute(
    key=str_glue("{CHROM}:{POS}_{REF}/{ALT}"),
    # \x3b encodes ";", but vcfR reads it literally as R-style \\x3b
    genes=str_split(genes, "\\\\x3b"))

markers <- list()

for (i in 1:nrow(tb)) {
  key <- tb %>% pull(key) %>% nth(i)
  genes <- tb %>% pull(genes) %>% nth(i) %>% unlist()
  for (gene in genes) {
    if (is.null(markers[[gene]])) markers[[gene]] <- key
    else markers[[gene]] <- c(markers[[gene]], key)
  }
}

min_variants <- ifelse(
  is.null(snakemake@params[["min_variants"]]),
  -Inf, snakemake@params[["min_variants"]])

lines <- names(markers) %>%
  keep(function(xs) length(xs) >= min_variants) %>%
  sapply(function(gene) paste0(c(gene, markers[[gene]]), collapse="\t"))

write_lines(lines, snakemake@output[[1]])
