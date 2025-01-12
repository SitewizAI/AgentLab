docker-compose up --build

Local testing: python main.py
code /Users/ram/agentlab_results

Deploy

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 679946893962.dkr.ecr.us-east-1.amazonaws.com
docker build --platform linux/amd64 -t web-agent .
docker tag web-agent:latest 679946893962.dkr.ecr.us-east-1.amazonaws.com/web-agent:latest
docker push 679946893962.dkr.ecr.us-east-1.amazonaws.com/web-agent:latest
aws apprunner start-deployment --service-arn arn:aws:apprunner:us-east-1:679946893962:service/web-agent-service/84e494a1a2d64585993797325102600b

docker run -p 8080:8080 679946893962.dkr.ecr.us-east-1.amazonaws.com/web-agent:latest
