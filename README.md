# FlaskApp

This is a simple Flask application with a `/create` endpoint that accepts JSON via POST requests.

---

## Running the App

to check if complies first
mypy app.py

1. Activate your virtual environment:

```bash
source venv/bin/activate
./run.sh


curl -X POST http://127.0.0.1:5000/create \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "age": 17}'

# Using data.json a

curl -X POST http://127.0.0.1:5000/create \
     -H "Content-Type: application/json" \
     -d @data.json


curl -X POST http://localhost/create \
     -H "Content-Type: application/json" \
     -d @data.json


curl -X POST http://localhost/users      -H "Content-Type: application/json"      -d '{"name": "Alice"}'
{
  "status": "ok",
  "user": {
    "id": 17,
    "name": "Alice"
  }

curl -X GET http://localhost/users/1

if you want to run this with docker:
runflaskdocker this alias. 

to run via load balancer: 

flaskdev : this alias for what is doing with docker run and using nginx :

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


run the app: 
```
flaskdev
```

to run db only via docker : docker-compose up -d db

or you have to run : 

docker run -d \
  -p 80:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  --name nginx-lb \
  nginx

  or docker-compose up -d

To shut down 
```
docker-compose down
```






