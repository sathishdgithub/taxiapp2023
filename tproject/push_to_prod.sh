echo "switching to valv prod context ..."
export AWS_PROFILE=valv-ecr

echo "Logging in to ECR ..."
$(aws ecr get-login --no-include-email --region ap-south-1)

echo "Building Docker Image 'taxiapp' ..."
docker build -t taxiapp .

echo "Tagging current build to 'taxiapp:latest' ..."
docker tag taxiapp:latest 145084937341.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

echo "Pushing Image to ECR repository ..."
docker push 145084937341.dkr.ecr.ap-south-1.amazonaws.com/taxiapp:latest

