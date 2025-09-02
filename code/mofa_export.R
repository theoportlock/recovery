#!/usr/bin/env Rscript
library(MOFA2)
library(optparse)

option_list <- list(
  make_option(c("--model"), type="character", default=NULL),
  make_option(c("--outdir"), type="character", default="extract")
)
opt <- parse_args(OptionParser(option_list=option_list))

dir.create(opt$outdir, showWarnings=FALSE, recursive=TRUE)

# Load model
model <- load_model(opt$model)

# Save factors
factors <- get_factors(model)

# Fix row names and column names
factors_df <- as.data.frame(factors)
factors_df$sampleID <- rownames(factors_df)
rownames(factors_df) <- NULL
colnames(factors_df) <- sub("^group1\\.", "", colnames(factors_df))

# Move sampleID to first column
factors_df <- factors_df[, c("sampleID", setdiff(names(factors_df), "sampleID"))]

write.table(factors_df,
            file=file.path(opt$outdir, "sample_factors.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE)

# Save weights per view with Feature as first column
view_names <- names(model@data)  # get the views in the MOFA2 model
for (v in view_names) {
  w <- get_weights(model, views=v)
  df <- as.data.frame(w[[1]])
  df <- cbind(Feature=rownames(df), df)  # Feature as first column
  write.table(df,
              file=file.path(opt$outdir, paste0("loadings_", v, ".tsv")),
              sep="\t", quote=FALSE, row.names=FALSE)
}

