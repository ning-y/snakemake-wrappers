suppressPackageStartupMessages({
  library(tidyverse)
  library(latex2exp)})

results <- read_tsv(snakemake@input[[1]]) %>%
  select(observed_p=PVALUE) %>%
  arrange(observed_p) %>%
  mutate(
    expected_p=seq(from=0, to=1, length.out=n()),
    observed_logp=-log10(observed_p),
    expected_logp=-log10(expected_p))

plot <- ggplot(results, aes(x=expected_logp, y=observed_logp)) +
  geom_point() +
  geom_abline(aes(intercept=0, slope=1)) +
  xlab(TeX("Expected $-\\log_{10}(p)$")) +
  ylab(TeX("Observed $-\\log_{10}(p)$"))
ggsave(snakemake@output[[1]], plot)
