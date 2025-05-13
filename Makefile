IMAGE_NAME = theoportlock/m4efad-image
TAG = latest
DOCKER_TAG = $(IMAGE_NAME):$(TAG)
SIF_NAME = m4efad_image.sif

HOST_RESULTS := $(shell realpath results)

# Default rule
all: run

# Build Docker image (side effect only; target is not a file)
docker:
	docker build -t $(DOCKER_TAG) .

# Build the Singularity image from the Docker image
$(SIF_NAME): Dockerfile requirements.txt
	docker build -t $(DOCKER_TAG) .
	singularity build $(SIF_NAME) docker-daemon://$(DOCKER_TAG)

# Run command using Apptainer
run: $(SIF_NAME)
	cmd="$(filter-out $@,$(MAKECMDGOALS))" && \
	apptainer exec \
	--bind $(HOST_RESULTS):/results:rw \
	--bind /run/media/theop/maindrive/fellowship/m4efad/recovery/code:/code:ro \
	--bind /run/media/theop/maindrive/metatoolkit/metatoolkit:/metatoolkit:ro \
	m4efad_image.sif \
	bash -c "export PATH=\$$PATH:/code:/metatoolkit/metatoolkit && $$cmd"

# Clean up artifacts
clean:
	rm -f $(SIF_NAME)
	-docker image rm $(DOCKER_TAG) 2>/dev/null || true

# This prevents make from interpreting CLI args like `python` as targets
%:
	@:
