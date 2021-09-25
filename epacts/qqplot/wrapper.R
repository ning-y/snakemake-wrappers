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

# Calculate the genomic inflaction factor, \lambda_{GC}
observed_median_chisq <- median(results$observed_p) %>% qchisq(., 1)
expected_median_chisq <- qchisq(0.5, 1)
genomic_inflation_factor <- observed_median_chisq / expected_median_chisq
annotations <- tibble(
  label=TeX(
    sprintf("Genomic inflation factor $\\lambda_{\\mathrm{GC}} = %s$",
            formatC(genomic_inflation_factor, digits=2, format="f")),
    output="character"),
  # Top-left corner
  x=-Inf, y=Inf,
  # Negative hjust direction moves text right, positive vjust is text down
  hjust=-0.1, vjust=2)

plot <- ggplot(results, aes(x=expected_logp, y=observed_logp)) +
  geom_point() +
  geom_abline(aes(intercept=0, slope=1)) +
  geom_text(
    data=annotations, parse=TRUE,
    mapping=aes(x=x, y=y, hjust=hjust, vjust=vjust, label=label)) +
  xlab(TeX("Expected $-\\log_{10}(p)$")) +
  ylab(TeX("Observed $-\\log_{10}(p)$"))
ggsave(snakemake@output[[1]], plot)
