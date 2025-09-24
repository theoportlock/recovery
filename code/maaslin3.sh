#!/usr/bin/env bash
set -euo pipefail

CONFIG_TSV="${1:-conf/timedatasets.tsv}"
INPUT_DIR=$2
OUTPUT_DIR=$4

if [[ ! -f "$CONFIG_TSV" ]]; then
  echo "Error: TSV config file not found: $CONFIG_TSV" >&2
  exit 1
fi

# Skip header line and read tab-separated fields into variables
tail -n +2 "$CONFIG_TSV" | while IFS=$'\t' read -r \
    name metadata formula reference \
    cores small_random_effects normalization transform \
    augment standardize max_significance max_pngs \
    min_abundance min_prevalence
do
  echo ">>> Running MaAsLin3 for dataset: $name"
  echo $INPUT_DIR/$name

  docker run \
    -v "$(pwd)":/work \
    -w /work \
    maaslin3-cli \
    $INPUT_DIR/$name.tsv \
    $metadata \
    $OUTPUT_DIR/$name \
    --formula="$formula" \
    --reference="$reference" \
    --cores "$cores" \
    --small_random_effects "$small_random_effects" \
    --normalization="$normalization" \
    --transform="$transform" \
    --augment "$augment" \
    --standardize "$standardize" \
    --max_significance "$max_significance" \
    --max_pngs "$max_pngs" \
    --min_abundance "$min_abundance" \
    --min_prevalence "$min_prevalence"

  echo ">>> Finished dataset: $name"
  echo
done

