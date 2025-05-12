IMAGE_NAME = theoportlock/m4efad-image
TAG = latest
SIF_NAME = m4efad_image.sif

SCRIPT ?= code/format_surveillance.py
ARGS ?= --input /data/input.tsv --output /results/output.tsv

.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

.PHONY: singularity-build
singularity-build: docker-build
	singularity build $(SIF_NAME) docker-daemon://$(IMAGE_NAME):$(TAG)

.PHONY: run
run:
	singularity exec \
		--bind $(PWD)/data:/data \
		--bind $(PWD)/results:/results \
		$(SIF_NAME) \
		python $(SCRIPT) $(ARGS)

.PHONY: clean
clean:
	rm -f $(SIF_NAME)

