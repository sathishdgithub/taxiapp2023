#!/usr/bin/env bash

echo "Copying env specific values ..."
env="prod"
env_file="../../env/taxi/"$env"/settings.py"
cp $env_file tproject/settings.py

# Setup AWS Profile 'valv-ecr' which should have credentials to push to ECR
echo "switching to valv prod context ..."
export AWS_PROFILE=valv-ecr

echo "Logging in to ECR ..."
$(aws ecr get-login --no-include-email --region ap-south-1)

echo "Building Docker Image 'taxiapp' ..."
docker build -t taxiapp:latest .

echo "Tagging current build to 'taxiapp:latest' ..."
docker tag taxiapp:latest 145084937341.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

echo "Pushing Image to ECR repository ..."
docker push 145084937341.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

echo "Restoring local env values ..."
git checkout -- tproject/settings.py
