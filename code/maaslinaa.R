library(Maaslin2)

# Define file paths
input_data <- "../results/aa.tsv"
input_metadata <- "../results/fulltimemeta.tsv"
output_directory <- "../results/aachange"

# Read metadata safely
if (is.character(input_metadata) && file.exists(input_metadata)) {
    df_input_metadata <-
	data.frame(data.table::fread(
	    input_metadata, header = TRUE, sep = "\t"),
		row.names = 1)
    if (nrow(metadata) == 1) {
	df_input_metadata <- read.table(input_metadata,
	    header = TRUE,
	    row.names = 1)
    }
} else if (is.data.frame(input_metadata)) {
    if (!tibble::has_rownames(input_metadata)) {
      stop("If supplying input_metadata as a data frame, it must have appropriate rownames!")
    }
    df_input_metadata <- as.data.frame(input_metadata) # in case it's a tibble or something
} else {
  stop("input_metadata is neither a file nor a data frame!")
} 

# Check structure to verify correct loading
print(dim(df_input_metadata))
print(colnames(df_input_metadata))

# Ensure column names are valid
if (!("timepoint" %in% colnames(df_input_metadata)) | !("Feeds_by_Randomization" %in% colnames(df_input_metadata))) {
    stop("Missing expected columns in metadata file.")
}

# Create interaction term dynamically
df_input_metadata$timepoint_Feeds <- paste(df_input_metadata$timepoint, df_input_metadata$Feeds_by_Randomization, sep = "_")

# Run Maaslin2 with the interaction term
fit_data <- Maaslin2(
  input_data = input_data, 
  input_metadata = df_input_metadata, 
  output = output_directory, 
  fixed_effects = c("timepoint", "Recovery", "Feeds_by_Randomization", "timepoint_Feeds"),
  random_effects = c("ID"),
  reference = c("Recovery,Healthy", "Feeds_by_Randomization,Local RUSF (A)")
)
