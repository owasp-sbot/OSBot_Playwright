# Variables
REGISTRY_ID="470426667096"
IMAGE_REPOSITORY="$REGISTRY_ID.dkr.ecr.eu-west-2.amazonaws.com"
IMAGE_NAME="osbot_playwright"
TAG="latest"
LOCAL_PORT="8888"
CONTAINER_PORT="8000"

# Build the Docker image
docker build -t $IMAGE_REPOSITORY/$IMAGE_NAME:$TAG .

# Run the Docker container
docker run --rm -it -p $LOCAL_PORT:$CONTAINER_PORT $IMAGE_REPOSITORY/$IMAGE_NAME:$TAG
#docker run --rm -it -v $(pwd):/var/task -p $LOCAL_PORT:$CONTAINER_PORT $IMAGE_REPOSITORY/$IMAGE_NAME:$TAG

# Example of another run command with the same image but different name and tag
#docker run --rm -it -p $LOCAL_PORT:$CONTAINER_PORT $IMAGE_REPOSITORY/docker_playwright:$TAG
