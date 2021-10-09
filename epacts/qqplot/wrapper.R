suppressPackageStartupMessages({
  library(tidyverse)
  library(latex2exp)
  library(assertthat)})

invisible(assert_that(snakemake@params[["test"]] %in% c("emmaxCMC", "skato")))
col_types <- case_when(
  snakemake@params[["test"]] == "emmaxCMC" ~ "ciiciiidddddd",
  snakemake@params[["test"]] == "skato"    ~ "ccccidiiidd")
if (is.na(col_types)) col_types <- NULL  # NULL means autodetect in read_tsv

# read_tsv guesses #CHROM column to be numeric, causing parsing errors when it
# reaches X and Y, so make it explicitly character. Full list of columns:
# #CHROM, BEGIN, END, MARKER_ID, NS, FRAC_WITH_RARE, NUM_ALL_VARS,
# NUM_PASS_VARS, NUM_SING_VARS, PVALUE, STATRHO
results <- read_tsv(snakemake@input[[1]], col_types=col_types) %>%
  select(observed_p=PVALUE) %>%
  # For the genomic inflaction factor calculation, because median considers NA
  filter(!is.na(observed_p)) %>%
  arrange(observed_p) %>%
  mutate(
    expected_p=seq(from=0, to=1, length.out=n()),
    observed_logp=-log10(observed_p),
    expected_logp=-log10(expected_p))

# Calculate the genomic inflaction factor, \lambda_{GC}
observed_median_chisq <- median(results$observed_p) %>% {qchisq(1-., 1)}
expected_median_chisq <- qchisq(0.5, 1)
genomic_inflation_factor <- observed_median_chisq / expected_median_chisq

# Calculate the R^squared fit to the 1:1 line.
rsq <- results %>%
  filter(is.finite(observed_logp), is.finite(expected_logp)) %>%  # base::cor gives NaN if !is.finite
  {cor(.$observed_logp, .$expected_logp) ** 2}

plot <- ggplot(results, aes(x=expected_logp, y=observed_logp)) +
  geom_point() +
  geom_abline(aes(intercept=0, slope=1)) +
  annotate(
    "text", x=-Inf, y=Inf, hjust=-0.1, vjust=1.5, parse=TRUE,
    label=str_glue(
      "list(lambda[GC] == {lgc}, italic(R)^2 == {rsq})",
      lgc=formatC(genomic_inflation_factor, digits=3, format="f"),
      rsq=formatC(rsq, digits=3, format="f"))) +
  xlab(TeX("Expected $-\\log_{10}(p)$")) +
  ylab(TeX("Observed $-\\log_{10}(p)$"))

ggsave(snakemake@output[["img"]], plot)
write_rds(plot, snakemake@output[["rds"]])
