# FlaskApp

This is a simple Flask application to be used for various backend projects I will be working on. 

Feel free to use this. I am using this base code to create different applications you will see in the appstore. The idea is that I may run only one or two EC2 or even just run server on my computer to handle some of simple apps until it gets big so I don't have to pour money. 

I am planning to add more for authentication methods like google/facebook/apple in the future.

---

## Running the App

to check if complies first
mypy run.py

1. Activate your virtual environment:

``` 
source venv/bin/activate
./run.sh

if you want to run this with docker
use this command: `runflaskdocker`

to run with load balancer with 3 pods:

flaskdev - this is alias - for running with docker on the top of nginx :

if you want to set this up as alias:

```
mkdir -p ~/bin
cp flaskdev.sh ~/bin/flaskdev
chmod +x ~/bin/flaskdev
```

Make sure ~/bin is in your PATH (usually it is in Linux/WSL/Mac):

```
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```



to run db only via docker : docker-compose up -d db

or you have to run : 

docker run -d \
  -p 80:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  --name nginx-lb \
  nginx

To shut down 
```
docker-compose down
```






