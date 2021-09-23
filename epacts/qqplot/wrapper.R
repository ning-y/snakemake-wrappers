suppressPackageStartupMessages({
  library(tidyverse)
  library(latex2exp)})

results <- read_tsv(snakemake@input[[1]]) %>%
  transmute(observed=-log10(PVALUE))

plot <- ggplot(results, aes(sample=observed)) +
  stat_qq(distribution=qunif) +
  stat_qq_line(distribution=qunif) +
  xlab(TeX("Expected $\\log_{10}(p)$")) +
  ylab(TeX("Observed $\\log_{10}(p)$"))
ggsave(snakemake@output[[1]], plot)
