#!/usr/bin/env Rscript

library(optparse)
library(Maaslin2)

# Define command-line options
option_list <- list(
  make_option(c("-f", "--fixed_effects"), type = "character", help = "Fixed effects (comma-separated)"),
  make_option(c("-r", "--random_effects"), type = "character", help = "Random effects (comma-separated)"),
  make_option(c("-o", "--output"), type = "character", help = "Output directory", default = "maaslin2_output"),
  make_option(c("--reference"), type = "character", help = "Reference levels (comma-separated)")
)

# Parse options
parser <- OptionParser(usage = "%prog [options] <input_data> <input_metadata>", option_list = option_list)
args <- parse_args(parser, positional_arguments = TRUE)

# Ensure we have the required positional arguments
if (length(args$args) < 2) {
  print_help(parser)
  stop("Error: Input data and metadata files are required.")
}

# Extract positional arguments
input_data <- args$args[[1]]
input_metadata <- args$args[[2]]

# Convert comma-separated strings to vectors
fixed_effects <- unlist(strsplit(args$options$fixed_effects, ","))
random_effects <- if (!is.null(args$options$random_effects)) unlist(strsplit(args$options$random_effects, ",")) else NULL
reference <- if (!is.null(args$options$reference)) unlist(strsplit(args$options$reference, ",")) else NULL

# Run Maaslin2
Maaslin2(
  input_data = input_data,
  input_metadata = input_metadata,
  output = args$options$output,
  fixed_effects = fixed_effects,
  random_effects = random_effects,
  reference = reference
)

