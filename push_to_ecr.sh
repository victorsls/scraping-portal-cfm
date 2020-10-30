#!/bin/bash

ENVIRONMENT=950303149621
IMAGE_VERSION="$(date +%Y%m%d%H%M)"
echo "AWS Authentication"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ENVIRONMENT}.dkr.ecr.us-east-1.amazonaws.com

echo "Building docker image version scraping-portal-cfm:$IMAGE_VERSION"
docker build -f Dockerfile . -t scraping-portal-cfm

docker tag scraping-portal-cfm:latest ${ENVIRONMENT}.dkr.ecr.us-east-1.amazonaws.com/scraping-portal-cfm:latest
docker tag scraping-portal-cfm:latest ${ENVIRONMENT}.dkr.ecr.us-east-1.amazonaws.com/scraping-portal-cfm:$IMAGE_VERSION

echo "Pushing scraping-portal-cfm to ECR"
docker push ${ENVIRONMENT}.dkr.ecr.us-east-1.amazonaws.com/scraping-portal-cfm:$IMAGE_VERSION
docker push ${ENVIRONMENT}.dkr.ecr.us-east-1.amazonaws.com/scraping-portal-cfm:latest
