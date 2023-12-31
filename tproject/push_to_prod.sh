#!/usr/bin/env bash

echo "Copying env specific values ..."
env="prod"
env_file="../../env/taxi/"$env"/settings.py"
cp $env_file tproject/settings.py

# Setup AWS Profile 'valv-ecr' which should have credentials to push to ECR
echo "switching to valv prod context ..."
export AWS_PROFILE=valv-ecr

echo "Logging in to ECR ..."
/usr/local/bin/aws ecr get-login-password --region ap-south-1 | docker login -u AWS 239293386318.dkr.ecr.ap-south-1.amazonaws.com --password-stdin

echo "Building Docker Image 'taxiapp' ..."
docker build --no-cache -t taxiapp:latest .

echo "Tagging current build to 'taxiapp:latest' ..."
docker tag taxiapp:latest 239293386318.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

echo "Pushing Image to ECR repository ..."
docker push 239293386318.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

echo "Restoring local env values ..."
git checkout -- tproject/settings.py
