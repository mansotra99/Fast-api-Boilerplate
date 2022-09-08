imageName=fast-api
containerName=fast-api

sudo docker build -t $imageName  . -f ./Dockerfile

echo Delete old container...
sudo docker rm -f $containerName

echo Run new container...
sudo docker run -e ENVIRONMENT=STAGING -d -p 8000:7000 --name $containerName  $imageName